# Guitar Pal Context

Guitar Pal is a personal music software project for exploring recorded guitar audio and practicing AI-driven development.

The current architecture direction is a reusable Python audio-analysis core wrapped by a small Streamlit UI. Core modules should use explicit inputs and structured outputs so they can be reused later by another app shell, CLI, service, or desktop wrapper.

## Local Verification

Prefer sandbox-local verification for routine checks. Do not request elevated
permissions just to run normal tests or app smoke checks when the project
virtual environment can run them.

Use the active project Python executable for common verification:

```bash
<PYTHON> -m pytest
<PYTHON> -m streamlit run src/guitar_pal/app.py
```

On POSIX-style environments such as macOS, Linux, or WSL, `<PYTHON>` is usually
`.venv/bin/python`.

Reserve elevated `uv` access for dependency or toolchain operations that need
it, such as `uv sync`, `uv add`, or `uv lock`.

For Streamlit visual smoke tests in Codex, prefer launching Streamlit as a child
process inside the Browser automation step, wait for
`http://localhost:<port>` to respond, navigate the built-in Browser to that URL,
and wait for the `load` state. Do not use `networkidle` with the built-in
Browser runtime because it is not supported there.

Read the matching current-platform file from `docs/ai/env/`, if one exists, when
platform-specific commands, paths, sandbox behavior, or Browser smoke-test
behavior matter.
