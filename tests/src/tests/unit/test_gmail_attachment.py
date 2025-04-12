import unittest
from unittest.mock import MagicMock
from mail_gmail_impl import GmailAttachment


class TestGmailAttachment(unittest.TestCase):
    """Unit tests for the GmailAttachment class."""

    def test_small_attachment_data(self):
        """Test handling of small attachments with inline base64-encoded data."""
        # Simulate a small attachment with base64-encoded data in the body
        attachment_part = {
            "filename": "example.txt",
            "mimeType": "text/plain",
            "body": {
                "data": "SGVsbG8gV29ybGQ="  # base64 for "Hello World"
            },
        }

        attachment = GmailAttachment(attachment_part)

        assert attachment.filename == "example.txt"
        assert attachment.content_type == "text/plain"
        assert attachment.data == b"Hello World"

    def test_large_attachment_data(self):
        """Test handling of large attachments fetched via attachmentId and service."""
        # Create a mock Gmail service
        mock_service = MagicMock()
        mock_attachment = {
            "data": "U29tZSBsYXJnZSBmaWxlIGNvbnRlbnQ="  # base64 for "Some large file content"
        }

        # Mock the Gmail API method chain to return the fake attachment
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.return_value.execute.return_value = mock_attachment

        attachment_part = {
            "filename": "large_file.pdf",
            "mimeType": "application/pdf",
            "body": {
                "attachmentId": "att123"
            },
        }

        attachment = GmailAttachment(
            attachment_part=attachment_part,
            service=mock_service,
            message_id="msg999"
        )

        assert attachment.filename == "large_file.pdf"
        assert attachment.content_type == "application/pdf"
        assert attachment.data == b"Some large file content"

        # Verify that the service was called with the correct parameters
        mock_service.users.return_value.messages.return_value.attachments.return_value.get.assert_called_once_with(
            userId="me",
            messageId="msg999",
            id="att123"
        )

    def test_large_attachment_missing_service_or_id(self):
        """Test when service or message_id is missing: should safely return empty bytes."""
        # Attachment has attachmentId, but no service or message_id provided
        attachment_part = {
            "filename": "fail.pdf",
            "mimeType": "application/pdf",
            "body": {
                "attachmentId": "att999"
            },
        }

        attachment = GmailAttachment(attachment_part=attachment_part)
        assert attachment.data == b""  # Should return empty bytes

    def test_content_type_fallback(self):
        """Test fallback behavior when mimeType is missing or unrecognized."""
        from unittest.mock import patch

        attachment_part = {
            "filename": "unknown.abc",
            "body": {"data": ""},
        }

        with patch("mimetypes.guess_type", return_value=(None, None)):
            attachment = GmailAttachment(attachment_part)

        assert attachment.content_type == "application/octet-stream"


if __name__ == "__main__":
    unittest.main()
