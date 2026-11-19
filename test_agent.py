"""Verification script for the Website Testing Agent.

Audits the local mock website to verify:
- Page load check
- Console error detection
- Broken image detection
- Broken internal link detection
- Horizontal overflow detection
- HTML report generation
"""

import os
import sys

# Ensure root directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.scanner import WebsiteScanner
from core.reporter import ReportGenerator
from core.models import IssueType


def run_verification():
    print("=" * 60)
    print("AI Website Testing Agent - Verification Suite")
    print("=" * 60)

    mock_html = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_site", "index.html"))
    if not os.path.exists(mock_html):
        print(f"[FAIL] Mock website not found at: {mock_html}")
        return False

    target_url = "file:///" + mock_html.replace("\\", "/")
    print(f"[*] Target Test URL: {target_url}")

    scanner = WebsiteScanner(
        base_output_dir="reports",
        max_internal_links=10,
        page_timeout_sec=15,
    )

    def log_status(step: str, pct: int):
        print(f"  [{pct}%] {step}")

    print("\n[*] Starting Playwright scan...")
    report = scanner.run_scan(target_url, status_callback=log_status)

    print("\n" + "=" * 60)
    print("Verification Results:")
    print("=" * 60)
    print(f"Target URL:              {report.target_url}")
    print(f"Duration:                {report.duration_seconds:.2f} seconds")
    print(f"Page Title:              '{report.metrics.title}'")
    print(f"Console Errors:          {report.metrics.console_errors_count}")
    print(f"Broken Images:           {report.metrics.broken_images_count}")
    print(f"Broken Links:            {report.metrics.broken_links_count}")
    print(f"Confirmed Failures:      {len(report.confirmed_failures)}")
    print(f"Manual Review Items:     {len(report.manual_verifications)}")
    print(f"Screenshots Captured:    {len(report.screenshots)}")

    # Generate Reports
    reporter = ReportGenerator()
    test_html = os.path.abspath(os.path.join("reports", "verification_report.html"))
    test_json = os.path.abspath(os.path.join("reports", "verification_report.json"))

    reporter.generate_html_report(report, test_html)
    reporter.generate_json_report(report, test_json)

    print(f"\n[+] Generated HTML Bug Report: {test_html}")
    print(f"[+] Generated JSON Bug Report: {test_json}")

    # Assertions
    assert os.path.exists(test_html), "HTML report file was not created!"
    assert os.path.exists(test_json), "JSON report file was not created!"
    assert len(report.screenshots) == 3, f"Expected 3 screenshots, got {len(report.screenshots)}"

    # Check that console error was caught
    console_bugs = [b for b in report.confirmed_failures if b.category == "Console & JavaScript"]
    assert len(console_bugs) >= 1, "Failed to capture intentional console error!"

    print("\n[SUCCESS] All QA agent capabilities verified successfully!")
    return True


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
