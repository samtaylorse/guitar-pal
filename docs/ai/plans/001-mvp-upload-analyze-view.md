# V0: Upload, Analyze, View

## Summary

Build the first playable Guitar Pal app: a local Streamlit interface for uploading a short WAV guitar clip, playing it back, viewing a waveform, and seeing basic audio metadata.

## Implementation

- Use Python with `uv` and `pyproject.toml`.
- Keep reusable audio analysis in `src/guitar_pal/audio.py`.
- Keep Streamlit upload, session, and presentation concerns in `src/guitar_pal/app.py`.
- Support WAV files only in V0.
- Reject clips longer than 30 seconds.
- Report duration, sample rate, channel count, frame count, sample width, peak amplitude, and RMS amplitude.
- Render a waveform from downsampled mono points returned by the core module.

## Architecture

- Core audio analysis must not import Streamlit or depend on a specific UI.
- Core functions should use explicit inputs and structured return values.
- UI code owns uploads and presentation; core code owns decoding, validation, metadata, and waveform preparation.
- Do not introduce an API server or multi-client architecture in V0.
- Keep generated audio, uploaded files, caches, and local environments out of version control.

## Interfaces

- Run the app: `uv run streamlit run src/guitar_pal/app.py`
- Run tests: `uv run pytest`
- Core API:
  - `analyze_wav_bytes(data: bytes, *, max_duration_seconds: float = 30.0, waveform_points: int = 2000) -> AudioAnalysis`
  - `analyze_wav_file(path: str | Path, *, max_duration_seconds: float = 30.0, waveform_points: int = 2000) -> AudioAnalysis`

## Verification

- Unit tests generate small WAV files in memory.
- Unit tests cover valid WAV analysis, metadata values, waveform output, invalid input, and clip length rejection.
- Streamlit adapter tests use `streamlit.testing.v1.AppTest` to upload a generated WAV fixture and confirm metadata and waveform sections render.
- Visual smoke verification should run Streamlit locally in a browser and capture a screenshot.
- Full browser-driven file upload can be added later if the browser automation surface supports file attachment.
