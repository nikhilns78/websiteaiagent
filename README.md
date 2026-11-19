# 🤖 AI Website Testing Agent (Python + Playwright + Streamlit)

A beginner-friendly, autonomous Quality Assurance (QA) testing agent built in Python using **Playwright** for browser automation and **Streamlit** for an interactive dashboard.

Designed from the ground up with **strict safety protocols**, this agent performs non-destructive, read-only checks on websites you own or have explicit permission to test. **No paid AI API keys are required.**

---

## 🌟 What This Agent Does

1. **Loads Web Pages & Measures Performance**: Checks if your URL loads properly, tracks HTTP status codes (200, 404, 500), and records DOM load times.
2. **Catches JavaScript Console Errors**: Listens silently in the background for browser console errors, syntax errors, and unhandled runtime exceptions.
3. **Identifies Missing & Broken Images**: Flags broken image URLs, images that fail to render (`naturalWidth == 0`), and missing `alt` attributes for accessibility.
4. **Scans for Broken Internal Links**: Safely follows links on the same domain up to a user-defined limit, verifying HTTP status codes.
5. **Inspects Forms Safely (Strictly Read-Only)**: Checks input fields for accessible labels. **Never submits forms, never enters credentials, and never alters data.**
6. **Audits Responsive Viewports**: Automatically resizes and takes screenshots across **Desktop** (1280×800), **Tablet** (768×1024), and **Mobile** (375×667). Flags horizontal scrolling defects.
7. **Generates Professional HTML Bug Reports**: Creates self-contained, shareable HTML bug reports with:
   - Bug ID (e.g. `BUG-001`, `REV-001`)
   - Severity rating (`Critical`, `High`, `Medium`, `Low`, `Info`)
   - Step-by-step reproduction guide
   - Expected vs. Actual results
   - Embedded screenshots & diagnostic evidence
   - Clear distinction between **Confirmed Failures** and **Potential Issues (Manual Verification)**.

---

## 📂 Project Structure

```text
WebsiteTestingAgent/
│
├── core/
│   ├── __init__.py          # Core package initializer
│   ├── models.py            # Data classes for bugs, severity, and metrics
│   ├── scanner.py           # Playwright automated test engine
│   └── reporter.py          # HTML & JSON report generator
│
├── templates/
│   ├── report_template.html # Professional HTML bug report template
│   └── bug_card_partial.html# Bug card partial component
│
├── mock_site/               # Built-in offline testing sandbox
│   ├── index.html           # Test page with intentional QA defects
│   └── about.html           # Working subpage
│
├── reports/                 # Output folder for screenshots and reports
├── app.py                   # Streamlit web application
├── test_agent.py            # Automated self-verification script
├── run.bat                  # 1-Click Windows batch launcher
├── requirements.txt         # Python dependencies
└── README.md                # Documentation and setup guide
```

---

## 🛡️ Safety & Ethical Testing Rules

This agent enforces strict safety guidelines:
- **No Form Submissions**: Will never submit a form, register users, or trigger purchase workflows.
- **No Destructive Operations**: Only executes read-only `GET` navigations and headless inspection.
- **Domain Restricted**: Only follows internal links belonging to the tested domain.
- **Rate Limited**: Restricts link checks to a controlled, configurable count (default: 10 links).
- **No Auth Bypass**: Does not attempt to guess passwords or bypass login security.

---

## 🚀 Quick Start on Windows

### Method 1: One-Click Launcher (Easiest)

Simply double-click the `run.bat` file in this folder. It will:
1. Automatically create a Python virtual environment (`venv`).
2. Install all required dependencies.
3. Download the Playwright Chromium browser.
4. Launch the Streamlit dashboard in your default browser.

---

### Method 2: Manual PowerShell / Command Prompt Setup

If you prefer running commands manually, follow these steps:

#### Step 1: Open PowerShell or Command Prompt
Navigate to the project directory:
```powershell
cd d:\WebsiteTestingAgent
```

#### Step 2: Create a Virtual Environment
```powershell
py -m venv venv
```

#### Step 3: Activate the Virtual Environment
- **On PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell shows a script execution error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and try again)*
- **On Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

#### Step 4: Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Install Playwright Browser Binaries
```powershell
playwright install chromium
```

#### Step 6: Launch the Streamlit Application
```powershell
streamlit run app.py
```

The web interface will automatically open in your browser at `http://localhost:8501`.

---

## 🧪 How to Test with the Offline Demo Sandbox

You do not even need an active internet connection to test the agent! A sandbox site with intentional bugs is included in `mock_site/index.html`.

1. Launch the app (`streamlit run app.py`).
2. In the left sidebar, click **"🧪 Fill Built-in Demo Sandbox"**.
3. Click **"🚀 Start Testing"**.
4. The agent will run and find:
   - 🔴 **BUG-001**: Broken Image (`images/non_existent_banner_photo.jpg`)
   - 🔴 **BUG-002**: Uncaught JavaScript console exception
   - 🔴 **BUG-003**: Broken internal link (404 missing page)
   - 🟡 **REV-001**: Missing `alt` accessibility attribute
   - 🟡 **REV-002**: Form input missing `<label>`
   - 🟡 **REV-003**: Mobile horizontal overflow defect (width > 375px)
5. Click **"📥 Download HTML Report"** or **"🌐 Open HTML Report in Browser"** to inspect the finished report.

---

## ⚙️ Running Automated Self-Verification

You can verify the entire test engine from the command line:

```powershell
python test_agent.py
```
This runs the scanner on the mock site, verifies that all defect categories are caught, generates a test report in `reports/verification_report.html`, and verifies output integrity.

---

## ❓ Frequently Asked Questions (FAQ)

### Q1: Do I need an OpenAI API key or paid subscription?
**No.** Version 1.0 uses a rule-based QA intelligence engine that runs 100% locally on your computer with zero API costs.

### Q2: Why did an image get flagged under "Requires Review" instead of "Confirmed Failure"?
If an image loads fine but doesn't have an `alt="description"` tag, it is flagged as **Manual Verification (Accessibility)** rather than a hard failure. A broken image URL or 0-pixel rendered image is flagged as a **Confirmed Failure**.

### Q3: How do I share the HTML report with a teammate or client?
The generated HTML report embeds screenshots directly as self-contained base64 data. You can email the single `.html` file or attach it to a Jira ticket, and it will render perfectly without needing any external folders.
