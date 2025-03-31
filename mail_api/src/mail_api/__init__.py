from typing import Iterator, Protocol, Optional, runtime_checkable


@runtime_checkable
class Message(Protocol):
    """A Mail Message."""

    @property
    def id(self) -> str:
        """Return the id of the message."""
        raise NotImplementedError()

    @property
    def from_(self) -> str:
        """Return the sender of the message."""
        raise NotImplementedError()

    @property
    def to(self) -> str:
        """Return the recipient of the message."""
        raise NotImplementedError()

    @property
    def date(self) -> str:
        """Return the date of the message."""
        raise NotImplementedError()

    @property
    def subject(self) -> str:
        """Return the subject of the message."""
        raise NotImplementedError()

    @property
    def body(self) -> str:
        """Return the body of the message."""
        raise NotImplementedError()


@runtime_checkable
class Attachment(Protocol):
    """An email attachment."""

    @property
    def filename(self) -> str:
        """Return the filename of the attachment."""
        raise NotImplementedError()

    @property
    def content_type(self) -> str:
        """Return the MIME content type of the attachment."""
        raise NotImplementedError()

    @property
    def data(self) -> bytes:
        """Return the binary data of the attachment."""
        raise NotImplementedError()


@runtime_checkable
class Client(Protocol):
    """A Mail Client used to interact with email services."""

    def get_messages(self) -> Iterator[Message]:
        """Return an iterator of messages from the inbox."""
        raise NotImplementedError()

    def get_message(self, message_id: str) -> Optional[Message]:
        """Retrieve a specific message by ID.

        Args:
            message_id: The unique identifier of the message

        Returns:
            The message if found, None otherwise
        """
        raise NotImplementedError()

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """Send an email message.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content

        Returns:
            True if message was sent successfully, False otherwise
        """
        raise NotImplementedError()

    def delete_message(self, message_id: str) -> bool:
        """Delete a message.

        Args:
            message_id: The unique identifier of the message to delete

        Returns:
            True if the message was successfully deleted, False otherwise
        """
        raise NotImplementedError()


def get_client() -> Client:
    """Return an instance of a Mail Client."""
    raise NotImplementedError()


def create_attachment(
    filename: str, data: bytes, content_type: Optional[str] = None
) -> Attachment:
    """Create an email attachment.

    Args:
        filename: Name of the attachment file
        data: Binary content of the attachment
        content_type: MIME type of the content (will be guessed if not provided)

    Returns:
        An Attachment object
    """
    raise NotImplementedError()
