import importlib.util
from mail_gmail_impl import GmailAttachment

if not importlib.util.find_spec("pytest_mock"):
    from unittest.mock import MagicMock

has_pytest_mock = importlib.util.find_spec("pytest_mock") is not None


def test_small_attachment_data():
    """Test handling of small attachments with inline base64-encoded data."""
    # Simulate a small attachment with base64-encoded data in the body
    attachment_part = {
        "filename": "example.txt",
        "mimeType": "text/plain",
        "body": {"data": "SGVsbG8gV29ybGQ="},  # base64 for "Hello World"
    }

    attachment = GmailAttachment(attachment_part)

    assert attachment.filename == "example.txt"
    assert attachment.content_type == "text/plain"
    assert attachment.data == b"Hello World"


if has_pytest_mock:

    def test_large_attachment_data(mocker):
        """Test handling of large attachments fetched via attachmentId and service."""
        # Create a mock Gmail service
        mock_service = mocker.MagicMock()
        mock_attachment = {
            "data": "U29tZSBsYXJnZSBmaWxlIGNvbnRlbnQ="  # base64 for "Some large file content"
        }

        # Mock the Gmail API method chain to return the fake attachment
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.return_value.execute.return_value = (
            mock_attachment
        )

        attachment_part = {
            "filename": "large_file.pdf",
            "mimeType": "application/pdf",
            "body": {"attachmentId": "att123"},
        }

        attachment = GmailAttachment(
            attachment_part=attachment_part, service=mock_service, message_id="msg999"
        )

        assert attachment.filename == "large_file.pdf"
        assert attachment.content_type == "application/pdf"
        assert attachment.data == b"Some large file content"

        # Verify that the service was called with the correct parameters
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.assert_called_once_with(
            userId="me", messageId="msg999", id="att123"
        )

else:

    def test_large_attachment_data():
        """Test handling of large attachments fetched via attachmentId and service."""
        # Create a mock Gmail service
        mock_service = MagicMock()
        mock_attachment = {
            "data": "U29tZSBsYXJnZSBmaWxlIGNvbnRlbnQ="  # base64 for "Some large file content"
        }

        # Mock the Gmail API method chain to return the fake attachment
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.return_value.execute.return_value = (
            mock_attachment
        )

        attachment_part = {
            "filename": "large_file.pdf",
            "mimeType": "application/pdf",
            "body": {"attachmentId": "att123"},
        }

        attachment = GmailAttachment(
            attachment_part=attachment_part, service=mock_service, message_id="msg999"
        )

        assert attachment.filename == "large_file.pdf"
        assert attachment.content_type == "application/pdf"
        assert attachment.data == b"Some large file content"

        # Verify that the service was called with the correct parameters
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.assert_called_once_with(
            userId="me", messageId="msg999", id="att123"
        )


def test_large_attachment_missing_service_or_id():
    """Test when service or message_id is missing: should safely return empty bytes."""
    # Attachment has attachmentId, but no service or message_id provided
    attachment_part = {
        "filename": "fail.pdf",
        "mimeType": "application/pdf",
        "body": {"attachmentId": "att999"},
    }

    attachment = GmailAttachment(attachment_part=attachment_part)
    assert attachment.data == b""  # Should return empty bytes


def test_content_type_fallback():
    """Test fallback behavior when mimeType is missing or unrecognized."""
    # Simulate an attachment with no mimeType and unknown file extension
    attachment_part = {
        "filename": "unknown.thiscannotbeamimetype",
        "body": {"data": ""},
    }

    attachment = GmailAttachment(attachment_part)
    # Should fallback to 'application/octet-stream'
    assert attachment.content_type == "application/octet-stream"
