# Guitar Pal Agent Notes

- Read `docs/ai/context.md` and the relevant plan under `docs/ai/plans/` before significant changes.
- When environment-specific verification, paths, browser smoke tests, or sandbox behavior matter, read the matching current-platform file from `docs/ai/env/` if one exists.
- Keep core audio logic independent from Streamlit or any other UI.
- Treat Streamlit as an adapter around reusable Python modules.
- Avoid service, client, or multi-app architecture until there is a concrete need.
- Keep generated audio, uploaded files, caches, and local environments out of version control.
