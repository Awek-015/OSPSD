import unittest
from unittest.mock import patch, MagicMock
from mail_api import Message, Attachment, Client
from mail_gmail_impl import (
    GmailClient,
    GmailMessage,
    GmailAttachment,
    get_gmail_client,
    create_gmail_attachment,
)


class TestGmailImplementation(unittest.TestCase):
    """Test the Gmail implementation of the mail_api interfaces."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the Gmail API service
        self.mock_service_patcher = patch("mail_gmail_impl.gmail_client.build")
        self.mock_service_builder = self.mock_service_patcher.start()

        # Configure the mock service
        self.mock_service = MagicMock()
        self.mock_users = MagicMock()
        self.mock_messages = MagicMock()

        self.mock_service.users.return_value = self.mock_users
        self.mock_users.messages.return_value = self.mock_messages
        self.mock_service_builder.return_value = self.mock_service

        # Mock credentials
        self.creds_patcher = patch("mail_gmail_impl.gmail_client.Credentials")
        self.mock_creds = self.creds_patcher.start()

        # Mock os.path.exists to always return False to avoid token loading
        self.path_patcher = patch("mail_gmail_impl.gmail_client.os.path.exists")
        self.mock_path_exists = self.path_patcher.start()
        self.mock_path_exists.return_value = False

        # Mock InstalledAppFlow
        self.flow_patcher = patch("mail_gmail_impl.gmail_client.InstalledAppFlow")
        self.mock_flow = self.flow_patcher.start()

        self.mock_flow_instance = MagicMock()
        self.mock_flow.from_client_secrets_file.return_value = self.mock_flow_instance
        self.mock_flow_instance.run_local_server.return_value = MagicMock()

        # Mock open and file operations
        self.open_patcher = patch("builtins.open", unittest.mock.mock_open())
        self.mock_open = self.open_patcher.start()

    def tearDown(self):
        """Tear down test fixtures."""
        self.mock_service_patcher.stop()
        self.creds_patcher.stop()
        self.path_patcher.stop()
        self.flow_patcher.stop()
        self.open_patcher.stop()

    def test_gmail_client_implements_client_interface(self):
        """Test that GmailClient implements the Client interface."""
        client = GmailClient(credentials_file="fake_credentials.json")
        assert isinstance(client, Client)

    def test_gmail_message_implements_message_interface(self):
        """Test that GmailMessage implements the Message interface."""
        message_data = {
            "id": "msg123",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "To", "value": "recipient@example.com"},
                    {"name": "Subject", "value": "Test Subject"},
                    {"name": "Date", "value": "2023-04-01"},
                ],
                "body": {"data": ""},
            },
        }
        message = GmailMessage(message_data)
        assert isinstance(message, Message)

        # Test all properties
        assert message.id == "msg123"
        assert message.from_ == "sender@example.com"
        assert message.to == "recipient@example.com"
        assert message.subject == "Test Subject"
        assert message.date == "2023-04-01"
        assert message.body == ""

    def test_gmail_attachment_implements_attachment_interface(self):
        """Test that GmailAttachment implements the Attachment interface."""
        attachment_part = {
            "filename": "test.pdf",
            "mimeType": "application/pdf",
            "body": {"data": ""},
        }
        attachment = GmailAttachment(attachment_part)
        assert isinstance(attachment, Attachment)

        # Test all properties
        assert attachment.filename == "test.pdf"
        assert attachment.content_type == "application/pdf"
        assert attachment.data == b""

    def test_get_gmail_client_factory_function(self):
        """Test the get_gmail_client factory function."""
        client = get_gmail_client(credentials_file="fake_credentials.json")
        assert isinstance(client, Client)
        assert isinstance(client, GmailClient)

    def test_create_gmail_attachment_factory_function(self):
        """Test the create_gmail_attachment factory function."""
        attachment = create_gmail_attachment(
            "test.pdf", b"test data", "application/pdf"
        )
        assert isinstance(attachment, Attachment)
        assert isinstance(attachment, GmailAttachment)
        assert attachment.filename == "test.pdf"
        assert attachment.content_type == "application/pdf"

    @patch("mail_gmail_impl.gmail_client.base64.urlsafe_b64encode")
    def test_send_message(self, mock_b64encode):
        """Test the send_message method."""
        # Configure mocks
        mock_b64encode.return_value = b"encoded_message"
        self.mock_messages.send.return_value.execute.return_value = {"id": "msg123"}

        # Create client and send message
        client = GmailClient(credentials_file="fake_credentials.json")
        result = client.send_message("to@example.com", "Test Subject", "Test Body")

        # Verify method was called with correct parameters
        self.mock_messages.send.assert_called_once()
        call_args = self.mock_messages.send.call_args[1]
        assert call_args["userId"] == "me"
        assert "body" in call_args

        # Verify result
        assert result is True

    def test_delete_message(self):
        """Test the delete_message method."""
        # Configure mocks
        self.mock_messages.trash.return_value.execute.return_value = {"id": "msg123"}

        # Create client and delete message
        client = GmailClient(credentials_file="fake_credentials.json")
        result = client.delete_message("msg123")

        # Verify method was called with correct parameters
        self.mock_messages.trash.assert_called_once_with(userId="me", id="msg123")

        # Verify result
        assert result is True

    def test_get_messages(self):
        """Test the get_messages method."""
        # Configure mocks
        self.mock_messages.list.return_value.execute.return_value = {
            "messages": [{"id": "msg1"}, {"id": "msg2"}]
        }

        # Mock message retrieval
        def get_side_effect(userId, id, format):
            message_data = {
                "id": id,
                "payload": {
                    "headers": [
                        {"name": "From", "value": f"sender_{id}@example.com"},
                        {"name": "Subject", "value": f"Subject {id}"},
                    ]
                },
            }
            return MagicMock(execute=MagicMock(return_value=message_data))

        self.mock_messages.get.side_effect = get_side_effect

        # Create client and get messages
        client = GmailClient(credentials_file="fake_credentials.json")
        messages = list(client.get_messages())

        # Verify methods were called
        self.mock_messages.list.assert_called_once_with(
            userId="me", maxResults=50, labelIds=["INBOX"]
        )

        # Verify results
        assert len(messages) == 2
        assert all(isinstance(msg, Message) for msg in messages)
        assert messages[0].id == "msg1"
        assert messages[1].id == "msg2"


if __name__ == "__main__":
    unittest.main()
