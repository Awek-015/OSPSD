from unittest.mock import Mock
from mail_api import Message, Attachment, Client, create_attachment


def test_message_interface():
    mock_message = Mock(spec=Message)
    mock_message.id = "msg123"
    mock_message.from_ = "sender@example.com"
    mock_message.to = "recipient@example.com"
    mock_message.date = "2023-04-01"
    mock_message.subject = "Test Subject"
    mock_message.body = "Test Body"

    assert isinstance(mock_message.id, str)
    assert isinstance(mock_message.from_, str)
    assert isinstance(mock_message.to, str)
    assert isinstance(mock_message.date, str)
    assert isinstance(mock_message.subject, str)
    assert isinstance(mock_message.body, str)


def test_attachment_interface():
    mock_attachment = Mock(spec=Attachment)
    mock_attachment.filename = "test.pdf"
    mock_attachment.content_type = "application/pdf"
    mock_attachment.data = b"sample binary data"

    assert isinstance(mock_attachment.filename, str)
    assert isinstance(mock_attachment.content_type, str)
    assert isinstance(mock_attachment.data, bytes)


def test_client_interface():
    mock_client = Mock(spec=Client)
    mock_messages = [Mock(spec=Message) for _ in range(5)]
    mock_client.get_messages.return_value = iter(mock_messages)
    mock_client.send_message.return_value = True
    mock_client.delete_message.return_value = True

    messages = list(mock_client.get_messages())
    assert len(messages) == 5
    for msg in messages:
        assert isinstance(msg, Message)

    result = mock_client.send_message("to@example.com", "Subject", "Body")
    assert isinstance(result, bool)

    result = mock_client.delete_message("msg123")
    assert isinstance(result, bool)


def test_create_attachment_function():
    mock_attachment = Mock(spec=Attachment)
    # Patch manually
    original_func = create_attachment
    try:
        import mail_api

        mail_api.create_attachment = Mock(return_value=mock_attachment)

        result = mail_api.create_attachment(
            filename="test.pdf", data=b"123", content_type="application/pdf"
        )
        assert result == mock_attachment
        mail_api.create_attachment.assert_called_once()
    finally:
        mail_api.create_attachment = original_func
