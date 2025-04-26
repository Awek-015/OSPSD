from mail_api import Attachment
import base64
import binascii
import mimetypes
import logging

# Set up logger
logger = logging.getLogger(__name__)


class GmailAttachment(Attachment):
    """Implementation of the Attachment interface for Gmail."""

    def __init__(self, attachment_part, service=None, message_id=None):
        """Initialize a Gmail attachment.

        Args:
            attachment_part: A Gmail API message part representing an attachment
            service: Gmail API service client (required for large attachments)
            message_id: The ID of the message the attachment belongs to
        """
        self._attachment_part = attachment_part
        self._filename = attachment_part.get("filename", "")
        self._mime_type = attachment_part.get("mimeType", "")
        self._data_cache = None
        self._service = service
        self._message_id = message_id

    @property
    def filename(self) -> str:
        """Return the filename of the attachment."""
        return self._filename

    @property
    def content_type(self) -> str:
        """Return the MIME content type of the attachment."""
        if not self._mime_type and self._filename:
            # Try to guess the MIME type from the filename
            guessed_type, _ = mimetypes.guess_type(self._filename)
            if guessed_type:
                return guessed_type
        return self._mime_type or "application/octet-stream"

    @property
    def data(self) -> bytes:
        """Return the binary data of the attachment."""
        if self._data_cache is not None:
            return self._data_cache

        body_data = self._attachment_part.get("body", {}).get("data", "")
        if not body_data:
            attachment_id = self._attachment_part.get("body", {}).get(
                "attachmentId", ""
            )
            if attachment_id and self._service and self._message_id:
                try:
                    attachment = (
                        self._service.users()
                        .messages()
                        .attachments()
                        .get(userId="me", messageId=self._message_id, id=attachment_id)
                        .execute()
                    )
                    body_data = attachment.get("data", "")
                except Exception as e:
                    logger.error(
                        f"Error occurred while fetching large attachments: {e}"
                    )
                    return b""
            else:
                return b""

        # Gmail API base64 encoding uses URL-safe alphabet
        try:
            # Replace URL-safe characters and add padding if needed
            body_data = body_data.replace("-", "+").replace("_", "/")
            padding_needed = len(body_data) % 4
            if padding_needed:
                body_data += "=" * (4 - padding_needed)

            self._data_cache = base64.b64decode(body_data)
            return self._data_cache
        except binascii.Error as e:
            logger.error(f"Error decoding attachment data: {e}")
            return b""
