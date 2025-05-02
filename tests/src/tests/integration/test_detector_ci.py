"""CI-friendly integration tests for SpamDetector using mocks."""

import os
import pytest
import tempfile
from unittest.mock import MagicMock
from mail_ai_spam_detector.detector import SpamDetector
from mail_api import Message

# Mark all tests in this file as CI-friendly
pytestmark = pytest.mark.ci_friendly


# Mock Gmail client class
class MockGmailClient:
    def __init__(self):
        self.mock_messages = [
            self._create_mock_message(
                "msg1", "sender@example.com", "Test Email 1", "This is a test email"
            ),
            self._create_mock_message(
                "msg2",
                "spam@example.com",
                "Make money fast!!!",
                "Click here to earn $$$",
            ),
            self._create_mock_message(
                "msg3", "friend@example.com", "Hello", "How are you doing?"
            ),
        ]

    def _create_mock_message(self, id, from_, subject, body):
        """Create a mock Message object."""
        message = MagicMock(spec=Message)
        message.id = id
        message.from_ = from_
        message.to = "user@example.com"
        message.date = "2025-04-01"
        message.subject = subject
        message.body = body
        return message

    def get_messages(self):
        """Return mock messages."""
        return self.mock_messages


# Mock AI client class
class MockAIClient:
    def __init__(self):
        self.sessions = {}

    def start_new_session(self, user_id):
        """Start a new mock session."""
        session_id = f"mock_session_{user_id}"
        self.sessions[session_id] = []
        return session_id

    def send_message(self, session_id, message):
        """Mock sending a message to AI."""
        self.sessions[session_id].append(message)

        # Simple rule-based response for testing
        # Instead of complex logic, set specific responses for our test emails
        if "Subject: Make money fast" in message:
            return {"content": "85.0"}  # High spam probability for email 2
        elif "Subject: Test Email" in message:
            return {"content": "30.0"}  # Medium spam probability for email 1
        elif "Subject: Hello" in message:
            return {"content": "5.0"}  # Low spam probability for email 3
        else:
            return {"content": "50.0"}  # Default

    def end_session(self, session_id):
        """End the mock session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        return True


@pytest.fixture
def spam_detector():
    """Create a SpamDetector with mock components."""
    mail_client = MockGmailClient()
    ai_client = MockAIClient()
    return SpamDetector(mail_client, ai_client)


def test_crawl_emails(spam_detector):
    """Test crawling emails."""
    emails = spam_detector.crawl_emails()
    assert len(emails) == 3
    assert emails[0].id == "msg1"
    assert emails[1].subject == "Make money fast!!!"


def test_analyze_email(spam_detector):
    """Test analyzing a single email."""
    emails = spam_detector.crawl_emails()

    session_id = spam_detector.ai_client.start_new_session("test_user")

    # Test email with medium probability
    pct_spam1 = spam_detector.analyze_email(session_id, emails[0])
    assert 25.0 <= pct_spam1 <= 35.0

    # Test email with high probability
    pct_spam2 = spam_detector.analyze_email(session_id, emails[1])
    assert 80.0 <= pct_spam2 <= 90.0

    # Test email with low probability
    pct_spam3 = spam_detector.analyze_email(session_id, emails[2])
    assert 0.0 <= pct_spam3 <= 10.0

    spam_detector.ai_client.end_session(session_id)


def test_detect_spam(spam_detector):
    """Test full spam detection flow and output to CSV."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        output_path = temp_file.name

    try:
        spam_detector.detect_spam(output_path)

        # Verify the CSV file exists and has the expected content
        assert os.path.exists(output_path)

        with open(output_path, "r") as f:
            content = f.read()
            # Check header
            assert "mail_id,Pct_spam" in content
            # Check all messages are included
            assert "msg1" in content
            assert "msg2" in content
            assert "msg3" in content
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_analyze_email_handles_exception(spam_detector, monkeypatch):
    """Test exception handling in analyze_email."""
    def fail_send_message(session_id, prompt):
        raise RuntimeError("Simulated AI failure")

    monkeypatch.setattr(spam_detector.ai_client, "send_message", fail_send_message)

    email = spam_detector.crawl_emails()[0]
    session_id = spam_detector.ai_client.start_new_session("test_user")
    result = spam_detector.analyze_email(session_id, email)

    assert result == 0.0
