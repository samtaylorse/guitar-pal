from __future__ import annotations

import pandas as pd
import streamlit as st

from guitar_pal.audio import AudioAnalysis, AudioValidationError, analyze_wav_bytes


# V0 simplification: keep uploads short so analysis and chart rendering stay responsive.
MAX_DURATION_SECONDS = 30.0


def main() -> None:
    st.set_page_config(page_title="Guitar Pal", page_icon="GP", layout="wide")
    _apply_component_styles()

    st.title("Guitar Pal")
    st.caption("Upload a short WAV guitar clip and inspect the shape of the recording.")

    uploaded_file = st.file_uploader("WAV clip", type=["wav"], accept_multiple_files=False)
    if uploaded_file is None:
        _render_empty_state()
        return

    audio_bytes = uploaded_file.getvalue()
    st.audio(audio_bytes, format="audio/wav")

    try:
        analysis = analyze_wav_bytes(
            audio_bytes,
            max_duration_seconds=MAX_DURATION_SECONDS,
        )
    except AudioValidationError as exc:
        st.error(str(exc))
        return

    _render_metadata(analysis)
    _render_waveform(analysis)


def _render_empty_state() -> None:
    st.info("Choose a WAV file to show playback, waveform, and recording stats.")

    columns = st.columns(3)
    columns[0].markdown("**Format**  \nWAV only")
    columns[1].markdown(f"**Maximum length**  \n{MAX_DURATION_SECONDS:.0f} seconds")
    columns[2].markdown("**Best signal**  \nShort, clean guitar takes")


def _render_metadata(analysis: AudioAnalysis) -> None:
    metadata = analysis.metadata
    columns = st.columns(4)
    columns[0].metric("Duration", f"{metadata.duration_seconds:.2f}s")
    columns[1].metric("Sample rate", f"{metadata.sample_rate_hz:,} Hz")
    columns[2].metric("Channels", str(metadata.channels))
    columns[3].metric("Peak", f"{metadata.peak_amplitude:.3f}")

    st.subheader("Audio metadata")
    st.dataframe(
        pd.DataFrame(
            [
                ("Duration", f"{metadata.duration_seconds:.3f} seconds"),
                ("Sample rate", f"{metadata.sample_rate_hz:,} Hz"),
                ("Channels", str(metadata.channels)),
                ("Frame count", f"{metadata.frame_count:,}"),
                ("Sample width", f"{metadata.sample_width_bytes} bytes"),
                ("Peak amplitude", f"{metadata.peak_amplitude:.6f}"),
                ("RMS amplitude", f"{metadata.rms_amplitude:.6f}"),
            ],
            columns=["Metric", "Value"],
        ),
        hide_index=True,
        width="stretch",
    )


def _render_waveform(analysis: AudioAnalysis) -> None:
    st.subheader("Waveform")
    waveform = pd.DataFrame(
        {
            "Time (s)": [point.time_seconds for point in analysis.waveform],
            "Amplitude": [point.amplitude for point in analysis.waveform],
        }
    ).set_index("Time (s)")
    st.line_chart(waveform, height=320)


def _apply_component_styles() -> None:
    st.html(
        """
        <style>
        [data-testid="stMetric"] {
            background: #fffaf0;
            border: 1px solid #ded4c3;
            border-radius: 8px;
            padding: 0.75rem 1rem;
        }
        [data-testid="stFileUploader"] section {
            background: #fffaf0;
            border-color: #b7a98f;
            border-radius: 8px;
            box-shadow: 0 10px 24px rgba(31, 37, 35, 0.08);
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #7a8d65;
        }
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] small {
            color: #1f2523 !important;
        }
        [data-testid="stFileUploader"] button {
            background: #1f2523;
            color: #fffaf0 !important;
            border-color: #1f2523;
            border-radius: 8px;
        }
        [data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploader"] button:focus {
            background: #313936;
            border-color: #313936;
            color: #fffaf0 !important;
        }
        [data-testid="stFileUploader"] button *,
        [data-testid="stFileUploader"] button:hover *,
        [data-testid="stFileUploader"] button:focus * {
            color: #fffaf0 !important;
        }
        [data-testid="stAlert"] {
            border-radius: 8px;
        }
        </style>
        """
    )


if __name__ == "__main__":
    main()
