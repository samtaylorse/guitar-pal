from __future__ import annotations

from io import BytesIO
import math
import struct
import wave


def make_wav_bytes(
    *,
    duration_seconds: float = 1.0,
    sample_rate: int = 8_000,
    frequency: float = 440.0,
    amplitude: float = 0.5,
    channels: int = 1,
) -> bytes:
    frame_count = int(duration_seconds * sample_rate)
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        for frame_index in range(frame_count):
            sample = int(
                amplitude
                * 32767
                * math.sin(2 * math.pi * frequency * frame_index / sample_rate)
            )
            for _ in range(channels):
                frames.extend(struct.pack("<h", sample))
        wav.writeframes(bytes(frames))

    return buffer.getvalue()
