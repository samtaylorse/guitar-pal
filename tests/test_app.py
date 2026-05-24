from __future__ import annotations

import unittest

from streamlit.testing.v1 import AppTest

from tests.audio_fixtures import make_wav_bytes


class StreamlitAppTests(unittest.TestCase):
    def test_uploading_wav_renders_metadata(self) -> None:
        app = AppTest.from_file("src/guitar_pal/app.py")
        app.run(timeout=10)

        app.file_uploader[0].upload(
            "sample.wav",
            make_wav_bytes(),
            mime_type="audio/wav",
        ).run(timeout=10)

        self.assertFalse(app.exception)
        page_text = "\n".join(subheader.value for subheader in app.subheader)
        page_text += "\n" + "\n".join(metric.label for metric in app.metric)
        self.assertIn("Audio metadata", page_text)
        self.assertIn("Waveform", page_text)
        self.assertIn("Duration", page_text)
        self.assertIn("Sample rate", page_text)

    def test_uploading_invalid_wav_renders_error(self) -> None:
        app = AppTest.from_file("src/guitar_pal/app.py")
        app.run(timeout=10)

        app.file_uploader[0].upload(
            "not-a-wav.wav",
            b"not wav data",
            mime_type="audio/wav",
        ).run(timeout=10)

        self.assertFalse(app.exception)
        error_text = "\n".join(error.value for error in app.error)
        self.assertIn("This file is not a readable PCM WAV file.", error_text)


if __name__ == "__main__":
    unittest.main()
