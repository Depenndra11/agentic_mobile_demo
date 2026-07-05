# Agentic Mobile Automation Demo

A LangGraph-orchestrated pipeline that uses Gemini to turn a plain-English
requirement into a full, runnable Selenium/pytest test suite — planning test
cases, inspecting the live UI, generating a Page Object, and generating
executable test scripts.

## Pipeline

```
Planner  ->  UI Inspector  ->  Page Agent  ->  Executor
```

| Step | Agent | Input | Output |
|---|---|---|---|
| 1 | `Planner` | `requirements/login_requirement.txt` | `agents/testcases.xlsx` |
| 2 | `UIInspector` | live browser session | `artifacts/screen.xml` |
| 3 | `PageAgent` | requirement + `screen.xml` | `pages/login_page.py` |
| 4 | `Executor` | requirement + page object + test cases | `tests/test_*.py` |

Each step's output feeds the next. The graph is defined in
`graph/workflow.py` using LangGraph, with state (test cases, screen XML path)
passed between nodes rather than only through side-effect files.

> **Note:** this demo currently drives Chrome with mobile emulation via
> Selenium (see `tests/conftest.py`), not a real device via Appium, even
> though `Appium-Python-Client` is listed as a dependency. Wire up an Appium
> driver if you need real-device/emulator coverage.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your key:
   ```bash
   cp .env.example .env
   ```

4. Adjust `config/config.json` if needed (target device, base URL, LLM model).

## Running

Run the full pipeline end-to-end:

```bash
python main.py
```

Or run an individual agent:

```bash
python -m agents.planner        # generate test cases -> testcases.xlsx
python -m agents.ui_inspector   # capture screen.xml (requires a running driver)
python -m agents.page_agent     # generate pages/login_page.py
python -m agents.executor       # generate tests/test_*.py from testcases.xlsx
```

Run the generated tests:

```bash
pytest tests/ -v
```

## Known limitations

- Single flow (login) is hardcoded via `requirements/login_requirement.txt`;
  extending to other flows means adding new requirement files and prompts.
- No validation step confirms generated pytest scripts are syntactically
  correct or pass before being written to `tests/`.
- Test credentials in `config/config.json` are for the public
  saucedemo.com demo site only -- do not follow this pattern for real
  credentials; use environment variables instead.
