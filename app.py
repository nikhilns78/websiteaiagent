"""Streamlit Web Application for AI Website Testing Agent.

Provides a clean, beginner-friendly UI to run automated Playwright QA scans,
inspect defects, review screenshots, and export professional HTML bug reports.
"""

import os
import sys
import webbrowser
from datetime import datetime
import streamlit as st

# Ensure core package is in Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.scanner import WebsiteScanner
from core.reporter import ReportGenerator
from core.models import IssueType, Severity


# Page configuration
st.set_page_config(
    page_title="AI Website Testing Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-confirmed {
        background-color: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-review {
        background-color: #f59e0b;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .report-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Test Settings")
        st.info("🛡️ **Safety Protocol Active**\n\nStrictly read-only checks. The agent will never submit forms, purchase, or modify data.")

        max_links = st.slider(
            "Max Internal Links to Audit",
            min_value=1,
            max_value=30,
            value=10,
            help="Limits link crawl depth to keep testing fast and server-friendly.",
        )

        page_timeout = st.slider(
            "Page Timeout (seconds)",
            min_value=5,
            max_value=60,
            value=20,
            help="Maximum time to wait for initial page response.",
        )

        st.markdown("---")
        st.markdown("### 📱 Viewports Included")
        st.markdown("- 🖥️ **Desktop** (1280 × 800)")
        st.markdown("- 📱 **Tablet** (768 × 1024)")
        st.markdown("- 📲 **Mobile** (375 × 667)")

        st.markdown("---")
        mock_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_site", "index.html"))
        mock_url = "file:///" + mock_path.replace("\\", "/")

        if st.button("🧪 Fill Built-in Demo Sandbox"):
            st.session_state["target_url_input"] = mock_url

    # Main Area
    st.title("🤖 AI Website Testing Agent")
    st.caption("Automated QA Engineer powered by Playwright & Python &bull; Beginner-friendly defect audit")

    st.markdown("""
    > **How it works:** Enter a website URL below and click **Start Testing**. The automated agent will inspect page loading,
    > test for broken links, detect missing or broken images, capture JavaScript console errors, evaluate responsive layouts,
    > and compile a professional QA Bug Report.
    """)

    # URL Input Box
    default_url = st.session_state.get("target_url_input", "https://example.com")
    target_url = st.text_input(
        "Website URL to Audit:",
        value=default_url,
        placeholder="https://yourwebsite.com or file:///...",
        help="Enter any public website you have permission to test, or click 'Fill Built-in Demo Sandbox' in the sidebar.",
    )

    col_btn, col_hint = st.columns([1, 4])
    with col_btn:
        start_btn = st.button("🚀 Start Testing", type="primary", use_container_width=True)
    with col_hint:
        st.caption("🔒 *Safe mode:* Never clicks submit buttons or fills sensitive credentials.")

    if start_btn:
        if not target_url.strip():
            st.error("Please enter a valid URL to begin testing.")
            return

        # Execution Progress Container
        st.write("---")
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(msg: str, pct: int):
            progress_bar.progress(pct)
            status_text.markdown(f"**Step [{pct}%]:** {msg}")

        scanner = WebsiteScanner(
            base_output_dir="reports",
            max_internal_links=max_links,
            page_timeout_sec=page_timeout,
        )

        with st.spinner("Automated agent is testing the website..."):
            try:
                report = scanner.run_scan(target_url, status_callback=update_progress)
                st.session_state["latest_report"] = report

                # Generate reports
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                reporter = ReportGenerator()
                html_path = os.path.abspath(os.path.join("reports", f"bug_report_{timestamp}.html"))
                json_path = os.path.abspath(os.path.join("reports", f"bug_report_{timestamp}.json"))

                reporter.generate_html_report(report, html_path)
                reporter.generate_json_report(report, json_path)

                st.session_state["latest_html_report"] = html_path
                st.session_state["latest_json_report"] = json_path

                progress_bar.progress(100)
                status_text.success("✅ Audit completed! Review your QA results below.")
            except Exception as e:
                st.error(f"An unexpected error occurred during execution: {str(e)}")
                return

    # Display Results if available
    if "latest_report" in st.session_state:
        report = st.session_state["latest_report"]
        html_report_path = st.session_state.get("latest_html_report", "")

        st.write("---")
        st.subheader("📋 Executive QA Summary")

        # Top metric cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label="🔴 Confirmed Failures",
                value=len(report.confirmed_failures),
                delta=None if len(report.confirmed_failures) == 0 else f"{len(report.confirmed_failures)} Bugs",
                delta_color="inverse",
            )
        with m2:
            st.metric(
                label="🟡 Manual Verification",
                value=len(report.manual_verifications),
                delta=None,
            )
        with m3:
            st.metric(
                label="⚡ Page Load Time",
                value=f"{report.metrics.load_time_ms:.0f} ms",
            )
        with m4:
            st.metric(
                label="🔗 Links Audited",
                value=report.metrics.internal_links_checked,
            )

        # Download & Browser View Action Row
        c_open, c_dl_html, c_dl_json = st.columns([1, 1, 1])
        with c_open:
            if html_report_path and os.path.exists(html_report_path):
                if st.button("🌐 Open HTML Report in Browser", use_container_width=True):
                    webbrowser.open(f"file:///{html_report_path}")
        with c_dl_html:
            if html_report_path and os.path.exists(html_report_path):
                with open(html_report_path, "r", encoding="utf-8") as f:
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=f.read(),
                        file_name=os.path.basename(html_report_path),
                        mime="text/html",
                        use_container_width=True,
                    )
        with c_dl_json:
            json_report_path = st.session_state.get("latest_json_report", "")
            if json_report_path and os.path.exists(json_report_path):
                with open(json_report_path, "r", encoding="utf-8") as f:
                    st.download_button(
                        label="📄 Download JSON Data",
                        data=f.read(),
                        file_name=os.path.basename(json_report_path),
                        mime="application/json",
                        use_container_width=True,
                    )

        # Tabs for Findings
        tab_confirmed, tab_manual, tab_screens, tab_metrics = st.tabs([
            f"🔴 Confirmed Failures ({len(report.confirmed_failures)})",
            f"🟡 Potential Issues / Manual Review ({len(report.manual_verifications)})",
            f"📸 Responsive Snapshots ({len(report.screenshots)})",
            "📊 Full Audit Data",
        ])

        with tab_confirmed:
            if not report.confirmed_failures:
                st.success("🎉 Zero confirmed failures found! All critical tests passed.")
            else:
                st.write("These are definite technical bugs detected by the testing agent:")
                for item in report.confirmed_failures:
                    with st.expander(f"**[{item.bug_id}] {item.title}** &bull; Severity: `{item.severity.value}`"):
                        st.markdown(f"**Category:** `{item.category}` &nbsp;|&nbsp; **URL:** {item.url}")
                        st.markdown("**Steps to Reproduce:**")
                        for step in item.steps_to_reproduce:
                            st.markdown(f"- {step}")
                        c_exp, c_act = st.columns(2)
                        with c_exp:
                            st.info(f"**Expected Result:**\n\n{item.expected_result}")
                        with c_act:
                            st.error(f"**Actual Result:**\n\n{item.actual_result}")
                        if item.evidence:
                            st.code(item.evidence, language="text")

        with tab_manual:
            if not report.manual_verifications:
                st.success("✨ Zero warnings flagged for manual review.")
            else:
                st.write("These items follow heuristic rules (accessibility, SEO, horizontal overflow) and should be manually inspected:")
                for item in report.manual_verifications:
                    with st.expander(f"**[{item.bug_id}] {item.title}** &bull; Severity: `{item.severity.value}`"):
                        st.markdown(f"**Category:** `{item.category}` &nbsp;|&nbsp; **URL:** {item.url}")
                        st.markdown("**Verification Steps:**")
                        for step in item.steps_to_reproduce:
                            st.markdown(f"- {step}")
                        c_exp, c_act = st.columns(2)
                        with c_exp:
                            st.info(f"**Best Practice / Expected:**\n\n{item.expected_result}")
                        with c_act:
                            st.warning(f"**Observed State:**\n\n{item.actual_result}")
                        if item.evidence:
                            st.caption(f"Evidence: {item.evidence}")

        with tab_screens:
            st.write("Automated multi-device responsive captures:")
            sc_cols = st.columns(len(report.screenshots))
            for idx, shot in enumerate(report.screenshots):
                with sc_cols[idx]:
                    st.subheader(f"{shot.viewport_name} ({shot.width}x{shot.height})")
                    if shot.has_horizontal_overflow:
                        st.error("⚠️ Horizontal Scroll Defect Detected")
                    else:
                        st.success("✅ Layout Clean")
                    if os.path.exists(shot.filepath):
                        st.image(shot.filepath, caption=f"{shot.viewport_name} Viewport", use_container_width=True)

        with tab_metrics:
            st.json(report.to_dict()["metrics"])


if __name__ == "__main__":
    main()
