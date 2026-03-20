# app.py
# Flask web application for the CMM Dashboard.
# Replaces Streamlit with a portable web framework
# that packages cleanly with PyInstaller.

import sys
import os
import tempfile

from flask import Flask, render_template, request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from parser import load_report
from evaluator import evaluate_report
from trend import load_runs, is_trending, get_all_feature_names
from capability import capability_from_runs
from visualizer import (
    deviation_bar_chart,
    tolerance_usage_chart,
    summary_donut,
    feature_type_breakdown,
    trend_line_chart,
    stability_chart,
    pass_rate_trend_chart,
    capability_chart,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max upload

@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def chart_html(fig) -> str:
    """Converts a Plotly figure to an HTML div string."""
    return fig.to_html(full_html=False, include_plotlyjs=False)


# ── Single Report Route ───────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def single_report():
    context = {"mode": "single"}

    if request.method == "POST":
        file = request.files.get("report_file")

        if file and file.filename:
            # Read settings from form
            warning_threshold = float(request.form.get("warning_threshold", 75))
            status_filter     = request.form.get("status_filter", "all")
            show_donut        = request.form.get("show_donut") == "1"
            show_type         = request.form.get("show_type") == "1"
            show_dev          = request.form.get("show_dev") == "1"
            show_usage        = request.form.get("show_usage") == "1"

            # Custom colors
            custom_colors = {
                "pass":    request.form.get("color_pass",    "#00C896"),
                "fail":    request.form.get("color_fail",    "#FF4C4C"),
                "warning": request.form.get("color_warning", "#FFA500"),
            }

            # Save to temp file
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix
            ) as tmp:
                file.save(tmp.name)
                tmp_path = tmp.name

            try:
                report  = load_report(tmp_path)
                results = evaluate_report(report, warning_threshold)

                # Apply status filter
                if status_filter == "fail":
                    results = [r for r in results if not r.is_pass]
                elif status_filter == "warning":
                    results = [r for r in results if r.severity == "WARNING"]
                elif status_filter == "pass":
                    results = [r for r in results if r.is_pass]

                total    = len(results)
                passes   = sum(1 for r in results if r.is_pass)
                fails    = total - passes
                warnings = sum(1 for r in results if r.severity == "WARNING")
                rate     = round(passes / total * 100) if total > 0 else 0

                context.update({
                    "results":    results,
                    "total":      total,
                    "passes":     passes,
                    "fails":      fails,
                    "warnings":   warnings,
                    "pass_rate":  rate,
                    "donut_chart":  chart_html(summary_donut(results, custom_colors))
                                    if show_donut else "",
                    "type_chart":   chart_html(feature_type_breakdown(results, custom_colors))
                                    if show_type else "",
                    "dev_chart":    chart_html(deviation_bar_chart(results, custom_colors))
                                    if show_dev else "",
                    "usage_chart":  chart_html(tolerance_usage_chart(results, custom_colors))
                                    if show_usage else "",
                    "show_donut":   show_donut,
                    "show_type":    show_type,
                    "show_dev":     show_dev,
                    "show_usage":   show_usage,
                    "warning_threshold": warning_threshold,
                    "status_filter": status_filter,
                })

            except Exception as e:
                context["error"] = str(e)
            finally:
                os.unlink(tmp_path)


# ── Multi-Run Trend Route ─────────────────────────────────────────

@app.route("/trend", methods=["GET", "POST"])
def trend():
    context = {"mode": "trend"}

    if request.method == "POST":
        files = request.files.getlist("report_files")

        if len(files) < 2:
            context["error"] = "Please upload at least two files."
            return render_template("trend.html", **context)

        tmp_paths = []
        try:
            for f in files:
                suffix = os.path.splitext(f.filename)[1]
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix
                ) as tmp:
                    f.save(tmp.name)
                    tmp_paths.append((tmp.name, f.filename))

            # Sort by original filename
            tmp_paths.sort(key=lambda x: x[1])
            paths = [p[0] for p in tmp_paths]

            runs          = load_runs(paths)
            feature_names = get_all_feature_names(runs)
            trending      = [n for n in feature_names
                             if is_trending(runs, n)]
            cap_results   = capability_from_runs(runs)

            # Fix run names to show original filenames
            for i, run in enumerate(runs):
                run.filename = tmp_paths[i][1]

            context.update({
                "runs":           runs,
                "total_runs":     len(runs),
                "total_features": len(feature_names),
                "trending_count": len(trending),
                "trending_names": trending,
                "cap_results":    cap_results,
                "trend_chart":    chart_html(trend_line_chart(runs)),
                "stability_chart": chart_html(stability_chart(runs)),
                "pass_rate_chart": chart_html(pass_rate_trend_chart(runs)),
                "cap_chart":      chart_html(capability_chart(cap_results))
                                  if cap_results else "",
            })

        except Exception as e:
            context["error"] = str(e)
        finally:
            for path, _ in tmp_paths:
                try:
                    os.unlink(path)
                except Exception:
                    pass

    return render_template("trend.html", **context)


# ── Run the App ───────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)