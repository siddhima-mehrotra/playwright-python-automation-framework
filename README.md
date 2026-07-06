# 🎭 Playwright Python Automation Framework

> Enterprise-grade UI & API test automation framework built with Playwright + Python  
> Designed for scalability, maintainability, and CI/CD integration

---

## 👩‍💻 About This Framework

This framework was designed and built from the ground up to support end-to-end test automation for enterprise web applications. It follows industry best practices including the **Page Object Model (POM)**, **modular architecture**, **data-driven testing**, and **parallel execution** — all integrated into a fully automated **GitHub Actions CI/CD pipeline**.

**Key highlights:**
- ✅ 150+ REST API test scenarios
- ✅ 120+ UI automation scenarios
- ✅ 70% reduction in regression execution time (1.5 days → 5–6 hours)
- ✅ Parallel execution across multiple browsers
- ✅ Zero manual trigger needed — fully CI/CD integrated

---

## 🏗️ Framework Architecture

```
playwright-python-automation-framework/
│
├── tests/
│   ├── ui/                        # UI test scenarios
│   │   ├── test_login.py
│   │   ├── test_dashboard.py
│   │   └── test_user_management.py
│   └── api/                       # API test scenarios
│       ├── test_users_api.py
│       ├── test_posts_api.py
│       └── test_schema_validation.py
│
├── pages/                         # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
│
├── utils/                         # Reusable utilities
│   ├── api_client.py
│   ├── logger.py
│   ├── retry.py
│   └── screenshot_helper.py
│
├── test-data/                     # Test data files
│   └── users.json
│
├── reports/                       # HTML test reports (auto-generated)
│
├── .github/
│   └── workflows/
│       └── playwright-ci.yml      # GitHub Actions CI/CD pipeline
│
├── conftest.py                    # Fixtures, hooks, browser setup
├── pytest.ini                     # Pytest configuration
├── .env.example                   # Environment config template
├── requirements.txt               # Python dependencies
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Test Framework | Playwright + Pytest |
| Language | Python 3.11+ |
| API Testing | Playwright API Request Context |
| Design Pattern | Page Object Model (POM) |
| CI/CD | GitHub Actions |
| Reporting | Pytest-HTML |
| Config Management | python-dotenv (.env) |
| Logging | Python logging module |
| Data-Driven | JSON-based test data |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/siddhima-mehrotra/playwright-python-automation-framework.git
cd playwright-python-automation-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Environment Setup

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your values
BASE_URL=https://your-app-url.com
API_BASE_URL=https://api.your-app.com
TEST_USERNAME=your_test_user
TEST_PASSWORD=your_test_password
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run only UI tests
pytest tests/ui/ -v

# Run only API tests
pytest tests/api/ -v

# Run in parallel (4 workers)
pytest -n 4

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run specific test
pytest tests/ui/test_login.py -v

# Run by tag
pytest -m "smoke" -v
pytest -m "regression" -v
```

---

## 🔁 CI/CD Pipeline

Tests run automatically on:
- Every **push** to `main` or `develop`
- Every **pull request**
- **Scheduled** daily at 6:00 AM UTC

The pipeline:
1. Sets up Python environment
2. Installs dependencies and Playwright browsers
3. Runs full test suite in parallel
4. Publishes HTML report as artifact
5. Notifies on failure

---

## 📊 Reporting

HTML reports are auto-generated after every run and published as GitHub Actions artifacts. Download from the **Actions** tab → select the latest run → **Artifacts**.

---

## 🧱 Framework Features

| Feature | Implementation |
|---|---|
| Page Object Model | `pages/` directory |
| Fixtures & Hooks | `conftest.py` |
| Retry on failure | `utils/retry.py` |
| Screenshot on failure | `utils/screenshot_helper.py` |
| Structured logging | `utils/logger.py` |
| Parallel execution | `pytest-xdist` |
| Multi-environment | `.env` config |
| Data-driven tests | JSON test data |
| API + UI coverage | Separate test suites |

---

## 👩‍🔬 Author

**Siddhima Mehrotra**  
Senior QA Automation Engineer | 8 Years Experience  
Playwright · Python · GitHub Actions · REST API Testing  

🔗 [LinkedIn](https://linkedin.com/in/siddhima-mehrotra-708a2a133)  
📧 siddhimamehrotra12@gmail.com

---

## 📄 License

MIT License — feel free to use this framework as a reference or starting point.
