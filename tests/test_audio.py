from __future__ import annotations

import unittest

from guitar_pal.audio import AudioValidationError, analyze_wav_bytes

from tests.audio_fixtures import make_wav_bytes


class AnalyzeWavBytesTests(unittest.TestCase):
    def test_valid_wav_returns_metadata_and_waveform(self) -> None:
        analysis = analyze_wav_bytes(make_wav_bytes(), waveform_points=100)

        self.assertAlmostEqual(analysis.metadata.duration_seconds, 1.0)
        self.assertEqual(analysis.metadata.sample_rate_hz, 8_000)
        self.assertEqual(analysis.metadata.channels, 1)
        self.assertEqual(analysis.metadata.frame_count, 8_000)
        self.assertEqual(analysis.metadata.sample_width_bytes, 2)
        self.assertGreater(analysis.metadata.peak_amplitude, 0.49)
        self.assertGreater(analysis.metadata.rms_amplitude, 0.30)
        self.assertEqual(len(analysis.waveform), 100)

    def test_stereo_wav_reports_channel_count(self) -> None:
        analysis = analyze_wav_bytes(make_wav_bytes(channels=2), waveform_points=25)

        self.assertEqual(analysis.metadata.channels, 2)
        self.assertEqual(len(analysis.waveform), 25)

    def test_invalid_input_is_rejected(self) -> None:
        with self.assertRaises(AudioValidationError):
            analyze_wav_bytes(b"not a wav")

    def test_empty_input_is_rejected(self) -> None:
        with self.assertRaises(AudioValidationError):
            analyze_wav_bytes(b"")

    def test_oversized_clip_is_rejected(self) -> None:
        audio = make_wav_bytes(duration_seconds=31.0, sample_rate=10, frequency=1.0)

        with self.assertRaises(AudioValidationError):
            analyze_wav_bytes(audio, max_duration_seconds=30.0)


if __name__ == "__main__":
    unittest.main()
