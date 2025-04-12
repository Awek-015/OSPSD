from mail_api import Attachment
import base64
import mimetypes


class GmailAttachment(Attachment):
    """Implementation of the Attachment interface for Gmail."""

    def __init__(self, attachment_part):
        """Initialize a Gmail attachment.

        Args:
            attachment_part: A Gmail API message part representing an attachment
        """
        self._attachment_part = attachment_part
        self._filename = attachment_part.get("filename", "")
        self._mime_type = attachment_part.get("mimeType", "")
        self._data_cache = None

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
            if not attachment_id:
                return b""

            # For large attachments, we would need to fetch using attachmentId
            # This requires an API call, which would be implemented here
            # using the service client that should be passed to the constructor
            # For now, we'll return empty as the interface doesn't support fetching by ID
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
        except base64.binascii.Error:
            return b""
