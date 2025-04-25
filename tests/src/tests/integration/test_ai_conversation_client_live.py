"""Live integration tests for AIConversationClient with GeminiAPIClient."""

import os
import pytest
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

# Skip all tests if SKIP_LIVE_TESTS environment variable is set
pytestmark = pytest.mark.skipif(
    os.environ.get("SKIP_LIVE_TESTS") == "1", reason="Live integration tests skipped"
)

@pytest.fixture(scope="module")
def ai_client() -> AIConversationClient:
    """Create an AIConversationClient fixture using GeminiAPIClient."""
    # Check if GEMINI_API_KEY exists
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not found in environment (.env)")

    backend = GeminiAPIClient()
    return AIConversationClient(api_client=backend)

def test_connection(ai_client: AIConversationClient) -> None:
    """Test that AI client can be initialized and start a session."""
    user_id = "integration_test_user"
    session_id = ai_client.start_new_session(user_id)
    assert isinstance(session_id, str)
    assert session_id.startswith("sess_")

@pytest.mark.xfail(reason="Requires manual verification of AI model response")
def test_send_and_receive_message(ai_client: AIConversationClient) -> None:
    """Test sending a message and receiving a response."""
    user_id = "integration_test_user"
    session_id = ai_client.start_new_session(user_id)

    response = ai_client.send_message(session_id, "Hello AI!")
    assert isinstance(response, dict)
    assert response.get("role") == "assistant"
    assert isinstance(response.get("content"), str)

@pytest.mark.xfail(reason="Requires manual verification of chat history retrieval")
def test_chat_history(ai_client: AIConversationClient) -> None:
    """Test retrieving chat history after sending messages."""
    user_id = "integration_test_user"
    session_id = ai_client.start_new_session(user_id)

    ai_client.send_message(session_id, "First message")
    ai_client.send_message(session_id, "Second message")

    history = ai_client.get_chat_history(session_id)
    assert isinstance(history, list)
    assert len(history) >= 4  # system prompt (optional) + 2 user + 2 assistant messages
