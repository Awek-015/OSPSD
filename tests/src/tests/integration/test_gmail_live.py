"""Live integration tests for Gmail client implementation."""

import pytest
import os
from mail_api import Message, Client
from mail_gmail_impl import get_gmail_client

# Skip all tests if SKIP_LIVE_TESTS environment variable is set
pytestmark = pytest.mark.skipif(
    os.environ.get("SKIP_LIVE_TESTS") == "1", reason="Live integration tests skipped"
)


@pytest.fixture(scope="module")
def gmail_client():
    """Create a Gmail client fixture for tests."""
    # Will be skipped if no credentials are available
    if not os.path.exists("credentials.json"):
        pytest.skip("credentials.json not found")

    return get_gmail_client()


def test_gmail_client_connection(gmail_client):
    """Test that the Gmail client can connect to the service."""
    assert isinstance(gmail_client, Client)
    # Accessing the service attribute verifies client initialization
    assert hasattr(gmail_client, "service")


def test_get_messages(gmail_client):
    """Test retrieving messages from Gmail."""
    # Get first 5 messages
    messages = list(gmail_client.get_messages())[:5]

    # We don't assert any specific number as inbox may be empty
    for message in messages:
        assert isinstance(message, Message)
        assert isinstance(message.id, str)
        assert isinstance(message.subject, str)
        assert isinstance(message.from_, str)
        assert isinstance(message.to, str)
        assert isinstance(message.date, str)
        assert isinstance(message.body, str)


@pytest.mark.xfail(reason="Requires manual verification")
def test_send_message(gmail_client):
    """Test sending a message (requires verification).

    This test is marked as xfail since it requires manual verification.
    """
    # Get user email for testing (can be configured via env var)
    test_email = "hz3575@nyu.edu"
    if not test_email:
        pytest.skip("TEST_EMAIL environment variable not set")

    # Send test email
    result = gmail_client.send_message(
        to=test_email,
        subject="Integration Test - Gmail API",
        body="This is an automated integration test. Please ignore.",
    )

    assert result is True
