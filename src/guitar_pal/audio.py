from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import math
import wave


DEFAULT_MAX_DURATION_SECONDS = 30.0
DEFAULT_WAVEFORM_POINTS = 2_000


class AudioValidationError(ValueError):
    """Raised when uploaded audio cannot be analyzed by the WAV pipeline."""


@dataclass(frozen=True)
class AudioMetadata:
    duration_seconds: float
    sample_rate_hz: int
    channels: int
    frame_count: int
    sample_width_bytes: int
    peak_amplitude: float
    rms_amplitude: float


@dataclass(frozen=True)
class WaveformPoint:
    time_seconds: float
    amplitude: float


@dataclass(frozen=True)
class AudioAnalysis:
    metadata: AudioMetadata
    waveform: list[WaveformPoint]


def analyze_wav_file(
    path: str | Path,
    *,
    max_duration_seconds: float = DEFAULT_MAX_DURATION_SECONDS,
    waveform_points: int = DEFAULT_WAVEFORM_POINTS,
) -> AudioAnalysis:
    return analyze_wav_bytes(
        Path(path).read_bytes(),
        max_duration_seconds=max_duration_seconds,
        waveform_points=waveform_points,
    )


def analyze_wav_bytes(
    data: bytes,
    *,
    max_duration_seconds: float = DEFAULT_MAX_DURATION_SECONDS,
    waveform_points: int = DEFAULT_WAVEFORM_POINTS,
) -> AudioAnalysis:
    if not data:
        raise AudioValidationError("Upload a non-empty WAV file.")

    try:
        with wave.open(BytesIO(data), "rb") as wav:
            channels = wav.getnchannels()
            sample_rate = wav.getframerate()
            frame_count = wav.getnframes()
            sample_width = wav.getsampwidth()
            raw_frames = wav.readframes(frame_count)
    except (EOFError, wave.Error) as exc:
        raise AudioValidationError("This file is not a readable PCM WAV file.") from exc

    if channels <= 0 or sample_rate <= 0:
        raise AudioValidationError("This WAV file has invalid channel or sample-rate metadata.")

    duration_seconds = frame_count / sample_rate
    if duration_seconds > max_duration_seconds:
        raise AudioValidationError(
            f"Clip is {duration_seconds:.1f}s long. Max clip duration is "
            f"{max_duration_seconds:.0f}s."
        )

    if sample_width not in {1, 2, 3, 4}:
        raise AudioValidationError(
            f"Unsupported WAV sample width: {sample_width} bytes per sample."
        )

    point_count = max(1, min(waveform_points, frame_count or 1))
    bucket_sums = [0.0] * point_count
    bucket_counts = [0] * point_count
    peak = 0.0
    square_sum = 0.0
    sample_count = 0

    frame_width = channels * sample_width
    for frame_index in range(frame_count):
        frame_offset = frame_index * frame_width
        mono_sum = 0.0

        for channel in range(channels):
            sample_offset = frame_offset + channel * sample_width
            amplitude = _decode_pcm_sample(
                raw_frames[sample_offset : sample_offset + sample_width],
                sample_width,
            )
            mono_sum += amplitude
            peak = max(peak, abs(amplitude))
            square_sum += amplitude * amplitude
            sample_count += 1

        mono_amplitude = mono_sum / channels
        bucket_index = min(point_count - 1, frame_index * point_count // max(frame_count, 1))
        bucket_sums[bucket_index] += mono_amplitude
        bucket_counts[bucket_index] += 1

    rms = math.sqrt(square_sum / sample_count) if sample_count else 0.0
    waveform = [
        WaveformPoint(
            time_seconds=(index / max(point_count - 1, 1)) * duration_seconds,
            amplitude=bucket_sums[index] / bucket_counts[index]
            if bucket_counts[index]
            else 0.0,
        )
        for index in range(point_count)
    ]

    return AudioAnalysis(
        metadata=AudioMetadata(
            duration_seconds=duration_seconds,
            sample_rate_hz=sample_rate,
            channels=channels,
            frame_count=frame_count,
            sample_width_bytes=sample_width,
            peak_amplitude=peak,
            rms_amplitude=rms,
        ),
        waveform=waveform,
    )


def _decode_pcm_sample(sample: bytes, sample_width: int) -> float:
    if sample_width == 1:
        return (sample[0] - 128) / 128.0

    value = int.from_bytes(sample, byteorder="little", signed=True)
    max_amplitude = float(2 ** (8 * sample_width - 1))
    return max(-1.0, min(1.0, value / max_amplitude))
