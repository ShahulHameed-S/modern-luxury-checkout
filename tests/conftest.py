import http.server
import os
import socket
import threading
import pytest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = WORKSPACE_ROOT / "evidence"
SCREENSHOTS_DIR = EVIDENCE_DIR / "screenshots"

# Ensure directories exist
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def find_free_port():
    """Find an available port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class QuietSimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Quiet HTTP handler that serves files without spamming test stdout."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_ROOT), **kwargs)

    def log_message(self, format, *args):
        # Suppress standard access logging in test run
        pass


@pytest.fixture(scope="session")
def live_server():
    """Starts an ephemeral HTTP server in a background daemon thread for testing."""
    port = find_free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietSimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    
    server_url = f"http://127.0.0.1:{port}"
    yield server_url
    server.shutdown()
    server.server_close()


@pytest.fixture
def clean_page(page, live_server):
    """
    Provides a clean, isolated browser page navigated to the application.
    Guarantees clean application state before each test execution.
    """
    page.goto(f"{live_server}/index.html")
    # Wait for DOM content to be fully loaded and initialized
    page.wait_for_selector("#checkout-view", state="visible")
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures screenshots automatically whenever an automated test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if test has access to 'page' or 'clean_page' fixture
        page = item.funcargs.get("page") or item.funcargs.get("clean_page")
        if page:
            safe_name = item.name.replace("[", "_").replace("]", "_").replace("/", "_")
            screenshot_path = SCREENSHOTS_DIR / f"failure_{safe_name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"\n[Test Failure Screenshot captured: {screenshot_path}]")
            except Exception as e:
                print(f"\n[Failed to capture failure screenshot: {e}]")
