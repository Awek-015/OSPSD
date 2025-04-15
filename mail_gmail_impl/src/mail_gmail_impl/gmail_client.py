from mail_api import Client, Message, Attachment
from typing import Iterator, Optional
import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from .gmail_message import GmailMessage


class GmailClient(Client):
    """Implementation of the Client interface for Gmail."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    TOKEN_FILE = "token.json"
    CREDENTIALS_FILE = "credentials.json"

    def __init__(self, credentials_file=None, token_file=None):
        """Initialize the Gmail client.

        Args:
            credentials_file: Path to the credentials.json file
            token_file: Path to the token.json file
        """
        self.credentials_file = credentials_file or self.CREDENTIALS_FILE
        self.token_file = token_file or self.TOKEN_FILE
        self.service = self._get_gmail_service()

    def _get_gmail_service(self):
        """Create and return an authenticated Gmail API service."""
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_info(
                eval(open(self.token_file).read())
            )

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, "w") as token:
                token.write(str(creds.to_json()))

        return build("gmail", "v1", credentials=creds)

    def get_messages(self) -> Iterator[Message]:
        """Return an iterator of messages from the inbox."""
        try:
            # Get IDs of messages in the inbox
            results = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=50, labelIds=["INBOX"])
                .execute()
            )
            messages = results.get("messages", [])

            for message in messages:
                msg_id = message["id"]
                # Fetch the full message using the ID
                msg = self._get_message_by_id(msg_id)
                if msg:
                    yield msg

        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_message(self, message_id: str) -> Optional[Message]:
        """Retrieve a specific message by ID."""
        return self._get_message_by_id(message_id)

    def _get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Helper method to get a message by ID."""
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            return GmailMessage(message)
        except HttpError:
            return None

    def send_message(self, to: str, subject: str, body: str, attachments: Optional[list[Attachment]] = None) -> bool:
        """Send an email message."""
        try:
            message = MIMEMultipart()
            message["to"] = to
            message["subject"] = subject

            message.attach(MIMEText(body, "plain"))

            if attachments:
                for attachment in attachments:
                    mime_attachment = MIMEBase(
                        *attachment.content_type.split("/", 1)
                    ) if "/" in attachment.content_type else MIMEBase("application", "octet-stream")
                    
                    mime_attachment.set_payload(attachment.data)
                    
                    encoders.encode_base64(mime_attachment)
                    
                    mime_attachment.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment.filename}",
                    )
                    
                    message.attach(mime_attachment)

            # Encode the message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            # Create the message
            create_message = {"raw": encoded_message}

            # Send the message
            self.service.users().messages().send(
                userId="me", body=create_message
            ).execute()
            return True
        except Exception as error:
            print(f"An error occurred: {error}")
            return False

    def delete_message(self, message_id: str) -> bool:
        """Delete a message."""
        try:
            self.service.users().messages().trash(userId="me", id=message_id).execute()
            return True
        except HttpError:
            return False
