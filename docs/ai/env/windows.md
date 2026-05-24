# Windows Notes

Use this file only when developing or verifying from Windows.

## Verification

If the project virtual environment exists, use
`.\.venv\Scripts\python.exe` as `<PYTHON>` for the shared verification commands
in `docs/ai/context.md`.

Windows process launching and path resolution can differ from POSIX shells. For
local Streamlit smoke tests, prefer an attached server process that can be
stopped after verification, then open the app at `http://localhost:<port>`.
