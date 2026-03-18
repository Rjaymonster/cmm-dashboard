import plotly.graph_objects as go
from evaluator import EvaluationResult

# Central color palette - keeps all charts visually consistent
COLORS = {
    "pass":       "#00C896",
    "fail":       "#FF4C4C",
    "warning":    "#FFA500",
    "nominal":    "#4A90D9",
    "background": "#0F1117",
    "surface":    "#1A1D27",
    "text":       "#E8EAF0",
    "subtext":    "#7B8099",
    "grid":       "rgba(255,255,255,0.06)"
}

def _severity_color(severity: str) -> str:
    """Return the right color for a given severity level."""
    return {
        "OK": COLORS["pass"],
        "WARNING": COLORS["warning"],
        "FAIL": COLORS["fail"],
    }.get(severity, COLORS["subtext"])

def deviation_bar_chart(results: list) -> go.Figure:
    """
    Horizontal bar chart showing deviation per feature.
    Colored by severity. Tolerance limits shown as markers.    
    """
    names =      [r.feature_name for r in results]
    deviations = [r.deviation for r in results]
    colors =     [_severity_color(r.severity) for r in results]
    upper_tols = [r.upper_tolerance for r in results]
    lower_tols = [r.lower_tolerance for r in results]

    fig = go.Figure()

    #Deviation bars
    fig.add_trace(go.Bar(
        name="Deviation",
        x=deviations,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{d:+.4f}" for d in deviations],
        textposition="outside",
    ))

    # Upper tolerance markers
    fig.add_trace(go.Scattergl(
        name="Upper Tol",
        x=upper_tols,
        y=names,
        mode="markers",
        marker=dict(symbol="line-ns", size=16, color=COLORS["nominal"],
                    line=dict(width=2, color=COLORS["nominal"])),
    ))

    # Lower tolerance markers
    fig.add_trace(go.Scattergl(
        name="Lower Tol",
        x=lower_tols,
        y=names,
        mode="markers",
        marker=dict(symbol="line-ns",size=16, color=COLORS["nominal"],
                    line=dict(width=2, color=COLORS["nominal"])),
    ))

    fig.update_layout(
        title="Feature Deviation vs Tolerance",
        xaxis=dict(title="deviaiton", zeroline=True,
                    zerolinecolor=COLORS["subtext"],
                    gridcolor=COLORS["grid"],
                    color=COLORS["text"]),
        yaxis=dict(gridcolor=COLORS["grid"], color=COLORS["text"]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=400,
        margin=dict(l=20, r=80, t=60, b=40),
    )
    
    return fig

def tolerance_usage_chart(results: list) -> go.Figure:
    """
    Shows what percentage of the tolerance band each feature consumes.
    Flags features near or over the limit even if passing.
    """
    names   =[r.feature_name for r in results]
    pct_used=[min(r.percent_used, 150) for r in results]
    colors  =[_severity_color(r.severity) for r in results]

    fig = go.Figure(go.Bar(
        x=pct_used,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{r.percent_used:.1f}%" for r in results],
        textposition="outside",
    ))

    # 75% warning line
    fig.add_vline(x=75, line_dash="dash", line_color=COLORS["warning"],
                  annotation_text="75% Warning",
                  annotation_font_color=COLORS["warning"])
    
    # 100% fail line
    fig.add_vline(x=100, line_dash="dash", line_color=COLORS["fail"],
                 annotation_text="100% Limit",
                 annotation_font_color=COLORS["fail"])
    
    fig.update_layout(
        title="Tolerance Band Usage per Feature",
        xaxis=dict(title="% of Tolerance Used", range=[0,160],
                   gridcolor=COLORS["grid"], color=COLORS["text"]),
        yaxis=dict(gridcolor=COLORS["grid"], color=COLORS["text"]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=400,
        margin=dict(l=20, r=80, t=60, b=40),
    )

    return fig

def summary_donut(results: list) -> go.Figure:
    """
    Donut chart summarizing OK / Warning /Fail counts.
    """
    ok_count        =sum(1 for r in results if r.severity == "OK")
    warning_count   =sum(1 for r in results if r.severity == "WARNING")
    fail_count      =sum(1 for r in results if r.severity == "FAIL")

    total       = len(results)
    pass_rate   = ((ok_count + warning_count)/ total * 100) if total > 0 else 0

    fig = go.Figure(go.Pie(
        labels=["OK", "Warning", "Fail"],
        values=[ok_count, warning_count, fail_count],
        hole=0.6,
        marker=dict(colors=[
            COLORS["pass"],
            COLORS["warning"],
            COLORS["fail"],
        ]),
        textinfo="label+value",
        textfont=dict(size=14),
    ))

    fig.update_layout(
        title="inspection Summary",
        annotations=[dict(
            text=f"<b>{pass_rate:.0f}%</b><br>Pass Rate",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False,
            font=dict(color=COLORS["text"]),
        )],
        paper_bgcolor=COLORS["background"],
        font=dict(color=COLORS["text"]),
        height=380,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig

def feature_type_breakdown(results: list) -> go.Figure:
    """
    Groups features by type and shows pass/fail counts.
    Helps spot systemic issues by feature type.
    """
    from collections import defaultdict

    type_data = defaultdict(lambda: {"PASS": 0, "FAIL": 0})
    for r in results:
        type_data[r.feature_type][r.status] += 1

    types       = list(type_data.keys())
    pass_counts = [type_data[t]["PASS"] for t in types]
    fail_counts = [type_data[t]["FAIL"] for t in types]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Pass",
        x=types,
        y=pass_counts,
        marker_color=COLORS["pass"],
    ))

    fig.add_trace(go.Bar(
        name="Fail",
        x=types,
        y=fail_counts,
        marker_color=COLORS["fail"],
    ))

    fig.update_layout(
        title="Pass/Fail by Feature Type",
        barmode="group",
        xaxis=dict(gridcolor=COLORS["grid"], color=COLORS["text"]),
        yaxis=dict(title="Count", gridcolor=COLORS["grid"],
                   color=COLORS["text"], dtick=1),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=380,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig

def save_dashboard(results: list, output_path: str = "dashboard.html") -> None:
    """
    Combines all four charts into a single HTML file.
    Open it in any browser - no server needed.
    """
    donut_html  = summary_donut(results).to_html(
        full_html=False, include_plotlyjs="cdn")
    type_html   = feature_type_breakdown(results).to_html(
        full_html=False, include_plotlyjs=False)
    dev_html    = deviation_bar_chart(results).to_html(
        full_html=False, include_plotlyjs=False)
    usage_html  = tolerance_usage_chart(results).to_html(
        full_html=False, include_plotlyjs=False)
    
    passes      = sum(1 for r in results if r.is_pass)
    fails       = len(results) - passes
    warnings    = sum(1 for r in results if r.severity == "WARNING")
    rate        = passes / len(results) * 100 if results else 0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
  <title>CMM Dashboard</title>
  <style>
    body {{
      background: #0F1117;
      color: #E8EAF0;
      font-family: sans-serif;
      padding: 2rem;
    }}
    h1 {{ color: #00C896; margin-bottom: 0; }}
    p  {{ color: #7B8099; margin-top: 0.3rem; }}
    .stats {{
      display: flex;
      gap: 1rem;
      margin: 1.5rem 0;
    }}
    .card {{
      background: #1A1D27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 10px;
      padding: 1rem 1.5rem;
      min-width: 120px;
    }}
    .label {{ font-size: 0.75rem; color: #7B8099; text-transform: uppercase; }}
    .value {{ font-size: 1.8rem; font-weight: bold; margin-top: 0.2rem; }}
    .green {{ color: #00C896; }}
    .red   {{ color: #FF4C4C; }}
    .amber {{ color: #FFA500; }}
    .blue  {{ color: #4A90D9; }}
    .grid  {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    .full  {{ margin-top: 1rem; }}
  </style>
</head>
<body>
  <h1>CMM DASHBOARD</h1>
  <p>MODUS Inspection Report Analysis</p>

  <div class="stats">
    <div class="card">
      <div class="label">Total</div>
      <div class="value blue">{len(results)}</div>
    </div>
    <div class="card">
      <div class="label">Passed</div>
      <div class="value green">{passes}</div>
    </div>
    <div class="card">
      <div class="label">Failed</div>
      <div class="value red">{fails}</div>
    </div>
    <div class="card">
      <div class="label">Warnings</div>
      <div class="value amber">{warnings}</div>
    </div>
    <div class="card">
      <div class="label">Pass Rate</div>
      <div class="value {'green' if rate >= 80 else 'amber'}">{rate:.0f}%</div>
    </div>
  </div>

  <div class="grid">
    {donut_html}
    {type_html}
  </div>

  <div class="full">{dev_html}</div>
  <div class="full">{usage_html}</div>

</body>
</html>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard saved to: {output_path}")
    
    
def trend_line_chart(runs: list) -> go.Figure:
    """
    Line chart showing deviation per feature across runs.
    One line per feature, x axis is run number.
    """
    from trend import get_all_feature_names, get_feature_trend, is_trending

    feature_names = get_all_feature_names(runs)
    run_names     = [r.run_name for r in runs]

    fig = go.Figure()

    for name in feature_names:
        trend    = get_feature_trend(runs, name)
        trending = is_trending(runs, name)

        # Get the tolerance limits from the first run
        upper_tol = None
        for result in runs[0].results:
            if result.feature_name == name:
                upper_tol = result.upper_tolerance
                break

        # Dashed line if trending, solid if stable
        dash  = "dash" if trending else "solid"
        label = f"{name} ⚠ TRENDING" if trending else name

        fig.add_trace(go.Scatter(
            name=label,
            x=run_names,
            y=trend,
            mode="lines+markers",
            line=dict(dash=dash, width=2),
        ))

        # Add tolerance limit line for reference
        if upper_tol is not None:
            fig.add_hline(
                y=upper_tol,
                line_dash="dot",
                line_color=COLORS["fail"],
                opacity=0.3,
            )

    fig.update_layout(
        title="Feature Deviation Trend Across Runs",
        xaxis=dict(title="Run", gridcolor=COLORS["grid"],
                   color=COLORS["text"]),
        yaxis=dict(title="Deviation", gridcolor=COLORS["grid"],
                   color=COLORS["text"]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=450,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig


def stability_chart(runs: list) -> go.Figure:
    """
    Ranks features by how much their deviation varies across runs.
    Higher bar = less stable = more concerning.
    """
    from trend import get_feature_stability, is_trending

    stability     = get_feature_stability(runs)
    names         = [s[0] for s in stability]
    variances     = [s[1] for s in stability]
    colors        = [
        COLORS["fail"] if is_trending(runs, n) else COLORS["warning"] if v > 0.00005 else COLORS["pass"]
        for n, v in stability
    ]

    fig = go.Figure(go.Bar(
        x=names,
        y=variances,
        marker_color=colors,
        text=[f"{v:.6f}" for v in variances],
        textposition="outside",
    ))

    fig.update_layout(
        title="Feature Stability (Deviation Variance Across Runs)",
        xaxis=dict(title="Feature", gridcolor=COLORS["grid"],
                   color=COLORS["text"]),
        yaxis=dict(title="Variance", gridcolor=COLORS["grid"],
                   color=COLORS["text"]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig

def pass_rate_trend_chart(runs: list) -> go.Figure:
    """
    Bar chart showing pass rate per run.
    Makes it easy to spot which runs had the most failures.
    """
    run_names  = [r.run_name for r in runs]
    pass_rates = [r.pass_rate for r in runs]
    colors     = [
        COLORS["pass"] if r >= 80 else
        COLORS["warning"] if r >= 60 else
        COLORS["fail"]
        for r in pass_rates
    ]

    fig = go.Figure(go.Bar(
        x=run_names,
        y=pass_rates,
        marker_color=colors,
        text=[f"{r:.0f}%" for r in pass_rates],
        textposition="outside",
    ))

    # 80% reference line
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color=COLORS["warning"],
        annotation_text="80% Target",
        annotation_font_color=COLORS["warning"],
    )

    fig.update_layout(
        title="Pass Rate Across Runs",
        xaxis=dict(title="Run", gridcolor=COLORS["grid"],
                   color=COLORS["text"]),
        yaxis=dict(title="Pass Rate %", range=[0, 110],
                   gridcolor=COLORS["grid"], color=COLORS["text"]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig

def capability_chart(cap_results: list) -> go.Figure:
    """
    Bar chart showing Cpk per feature colored by rating.
    Reference lines at 1.0, 1.33, and 1.67.
    """
    names  = [r.feature_name for r in cap_results]
    cpk    = [r.cpk for r in cap_results]
    cp     = [r.cp for r in cap_results]
    colors = [r.color for r in cap_results]

    fig = go.Figure()

    # Cp bars
    fig.add_trace(go.Bar(
        name="Cp",
        x=names,
        y=cp,
        marker_color="rgba(74, 144, 217, 0.4)",
        marker_line_width=0,
    ))

    # Cpk bars
    fig.add_trace(go.Bar(
        name="Cpk",
        x=names,
        y=cpk,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:.3f}" for v in cpk],
        textposition="outside",
    ))

    # Reference lines
    fig.add_hline(y=1.67, line_dash="dash", line_color=COLORS["pass"],
                  annotation_text="1.67 Excellent",
                  annotation_font_color=COLORS["pass"])

    fig.add_hline(y=1.33, line_dash="dash", line_color=COLORS["nominal"],
                  annotation_text="1.33 Capable",
                  annotation_font_color=COLORS["nominal"])

    fig.add_hline(y=1.00, line_dash="dash", line_color=COLORS["warning"],
                  annotation_text="1.00 Marginal",
                  annotation_font_color=COLORS["warning"])

    fig.update_layout(
        title="Process Capability (Cp / Cpk) by Feature",
        barmode="group",
        xaxis=dict(gridcolor=COLORS["grid"], color=COLORS["text"]),
        yaxis=dict(title="Index Value", gridcolor=COLORS["grid"],
                   color=COLORS["text"], range=[0, max(cp) * 1.2]),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(color=COLORS["text"]),
        legend=dict(bgcolor=COLORS["surface"]),
        height=450,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig