# Guitar Pal

A small local app for exploring recorded guitar audio.

V0 supports uploading a short WAV clip, playing it back, viewing a waveform, and
showing basic audio metadata.

## Setup

Install Python and `uv`, then run:

```bash
uv sync --extra dev
uv run streamlit run src/guitar_pal/app.py
```

Run tests:

```bash
uv run pytest
```

AI development context starts in `AGENTS.md` and `docs/ai/context.md`.
