# Gmail Mail Client Implementation

This package implements the `mail_api` interfaces for interacting with Gmail.

## Features

- Gmail-specific implementation of the `mail_api` interfaces
- Authentication using OAuth 2.0
- Reading Gmail inbox messages
- Sending simple text emails
- Deleting emails
- Supporting email attachments

## Installation

```bash
pip install -e .
```

## Setup

1. Set up a Google Cloud Project and enable the Gmail API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 Client ID credentials
   - Download the credentials file as `credentials.json`

2. Place the `credentials.json` file in your working directory or specify its location when initializing the client.

## Usage

```python
from mail_gmail_impl import get_gmail_client

# Create a Gmail client (first time will open browser for auth)
client = get_gmail_client()

# Read messages from inbox
for message in client.get_messages():
    print(f"From: {message.from_}")
    print(f"Subject: {message.subject}")
    print(f"Body: {message.body}")
    print("-" * 50)

# Send a message
client.send_message(
    to="recipient@example.com",
    subject="Hello from Gmail API",
    body="This is a test message sent via the Gmail API."
)

# Create an attachment
with open("document.pdf", "rb") as file:
    data = file.read()
    
from mail_gmail_impl import create_gmail_attachment
attachment = create_gmail_attachment("document.pdf", data)
print(f"Attachment filename: {attachment.filename}")
print(f"Attachment content type: {attachment.content_type}")
```

## Authentication

The first time you run the client, it will prompt you to authorize access to your Gmail account through a browser. After authorization, a token will be saved to `token.json` for future use.

## Limitations

- CC/BCC functionality is not supported
- Complex message filtering is not implemented
- The implementation assumes valid credentials are provided
