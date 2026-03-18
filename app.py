import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from parser import load_report
from evaluator import evaluate_report
from trend import load_runs, is_trending, get_all_feature_names
from visualizer import (
    deviation_bar_chart,
    tolerance_usage_chart,
    summary_donut,
    feature_type_breakdown,
    trend_line_chart,
    stability_chart,
    pass_rate_trend_chart,
)
from capability import capability_from_runs, capability_from_report
from visualizer import capability_chart

# --- Page Config ---
st.set_page_config(
    page_title="CMM Dashboard",
    page_icon="📐",
    layout="wide",
)

st.markdown("# 📐 CMM Dashboard")
st.markdown("---")

# --- Mode Toggle ---
mode = st.radio(
    "Select Mode",
    ["Single Report", "Multi-Run Trend Analysis"],
    horizontal=True,
)

st.markdown("---")


# ── SINGLE REPORT MODE ────────────────────────────────────────────────────────

if mode == "Single Report":

    uploaded_file = st.file_uploader(
        "Upload MODUS CSV Report",
        type=["csv"],
    )

    if uploaded_file is None:
        st.info("Upload a CSV file to see your dashboard.")
        st.stop()

    tmp_path = f"tmp_{uploaded_file.name}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        report  = load_report(tmp_path)
        results = evaluate_report(report)
    except Exception as e:
        st.error(f"Failed to parse report: {e}")
        st.stop()

    # Stat cards
    total    = len(results)
    passes   = sum(1 for r in results if r.is_pass)
    fails    = total - passes
    warnings = sum(1 for r in results if r.severity == "WARNING")
    rate     = passes / total * 100 if total > 0 else 0

    st.markdown("### Inspection Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Features", total)
    c2.metric("Passed",         passes)
    c3.metric("Failed",         fails)
    c4.metric("Warnings",       warnings)
    c5.metric("Pass Rate",      f"{rate:.0f}%")

    # Charts
    st.markdown("### Overview")
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(summary_donut(results), width='stretch')
    with col_right:
        st.plotly_chart(feature_type_breakdown(results), width='stretch')

    st.markdown("### Feature Detail")
    st.plotly_chart(deviation_bar_chart(results), width='stretch')

    st.markdown("### Tolerance Consumption")
    st.plotly_chart(tolerance_usage_chart(results), width='stretch')

    # --- Raw Data Table ---
    st.markdown("### Raw Data")

    import pandas as pd

    table = pd.DataFrame([{
        "Feature":       r.feature_name,
        "Type":          r.feature_type,
        "Condition":     r.material_condition,
        "Deviation":     r.deviation,
        "Stated Tol":    r.upper_tolerance,
        "Bonus":         round(r.bonus_tolerance, 4) if r.has_bonus else "-",
        "Effective Tol": round(r.effective_upper, 4),
        "Tol Used %":    round(r.percent_used, 1),
        "Status":        r.status,
        "Severity":      r.severity,
    } for r in results])

    st.dataframe(table, hide_index=True)


# ── MULTI-RUN TREND MODE ──────────────────────────────────────────────────────

else:

    uploaded_files = st.file_uploader(
        "Upload Multiple MODUS CSV Reports",
        type=["csv"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("Upload two or more CSV files to see trend analysis.")
        st.stop()

    if len(uploaded_files) < 2:
        st.warning("Please upload at least two files to compare trends.")
        st.stop()

    # Save all uploaded files temporarily
    tmp_paths = []
    for uf in uploaded_files:
        tmp_path = f"tmp_{uf.name}"
        with open(tmp_path, "wb") as f:
            f.write(uf.read())
        tmp_paths.append(tmp_path)

    try:
        runs = load_runs(tmp_paths)
    except Exception as e:
        st.error(f"Failed to load runs: {e}")
        st.stop()

    # Summary stats
    st.markdown("### Trend Summary")
    feature_names = get_all_feature_names(runs)
    trending      = [n for n in feature_names if is_trending(runs, n)]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Runs",        len(runs))
    c2.metric("Features Tracked",  len(feature_names))
    c3.metric("Trending Features", len(trending))

    # Trending warning
    if trending:
        st.warning(f"⚠ Trending toward failure: {', '.join(trending)}")

    # Charts
    st.markdown("### Deviation Trend")
    st.plotly_chart(trend_line_chart(runs), width='stretch')

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### Feature Stability")
        st.plotly_chart(stability_chart(runs), width='stretch')
    with col_right:
        st.markdown("### Pass Rate by Run")
        st.plotly_chart(pass_rate_trend_chart(runs), width='stretch')

    # --- Capability ---
    st.markdown("### Process Capability")
    from capability import capability_from_runs
    cap_results = capability_from_runs(runs)
    if cap_results:
        st.plotly_chart(capability_chart(cap_results), width='stretch')

        cap_table = pd.DataFrame([{
            "Feature":  r.feature_name,
            "Type":     r.feature_type,
            "n":        r.sample_count,
            "Mean Dev": round(r.mean, 4),
            "Std Dev":  round(r.std_dev, 4),
            "Cp":       r.cp,
            "Cpk":      r.cpk,
            "Rating":   r.rating,
        } for r in cap_results])
        st.dataframe(cap_table, hide_index=True)