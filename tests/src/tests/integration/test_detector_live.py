"""Live integration tests for SpamDetector."""

import os
import pytest
import pathlib
from datetime import datetime
from mail_ai_spam_detector.detector import SpamDetector
from mail_gmail_impl import get_gmail_client
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

# Skip all tests if SKIP_LIVE_TESTS environment variable is set
pytestmark = pytest.mark.skipif(
    os.environ.get("SKIP_LIVE_TESTS") == "1", reason="Live integration tests skipped"
)

@pytest.fixture(scope="module")
def spam_detector() -> SpamDetector:
    """Create a SpamDetector fixture."""
    if not os.path.exists("credentials.json"):
        pytest.skip("credentials.json not found")
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not found in .env")

    mail_client = get_gmail_client()
    ai_client = AIConversationClient(GeminiAPIClient())
    return SpamDetector(mail_client, ai_client)

def test_crawl_emails(spam_detector: SpamDetector) -> None:
    """Test crawling emails."""
    emails = spam_detector.crawl_emails(max_count=3)
    assert isinstance(emails, list)

@pytest.mark.xfail(reason="Requires AI live interaction to determine spam probability")
def test_analyze_email(spam_detector: SpamDetector) -> None:
    """Test analyzing a single email."""
    emails = spam_detector.crawl_emails(max_count=1)
    if not emails:
        pytest.skip("No emails found to analyze.")

    session_id = spam_detector.ai_client.start_new_session("test_analyze")
    pct_spam = spam_detector.analyze_email(session_id, emails[0])
    spam_detector.ai_client.end_session(session_id)

    assert 0.0 <= pct_spam <= 100.0

@pytest.mark.xfail(reason="Requires manual verification of CSV output")
def test_detect_spam(spam_detector: SpamDetector) -> None:
    """Test full spam detection flow and output to CSV with timestamped filename."""
    output_dir = pathlib.Path(__file__).resolve().parents[4] / "integration-results"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_csv = output_dir / f"output_{timestamp}.csv"

    spam_detector.detect_spam(str(output_csv), max_emails=3)

    assert output_csv.exists()
