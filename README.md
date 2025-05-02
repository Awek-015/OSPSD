# Gmail Mail Client Interface

## Overview

This project provides a standardized API for interacting with Gmail email services. It is organized into modular components with a focus on clean interface design and implementation separation:

- **mail_api**: Defines abstract interfaces for email clients and messages
- **mail_gmail_impl**: Gmail-specific implementation of the `mail_api` interfaces
- **mail_ai_spam_detector**: AI-powered spam detection service
- **ai_conversation_client**: AI conversation capabilities
- **tests**: Contains both unit tests using mocking and integration tests for real-world validation

## Project Scope

### Core Functionalities

- Read Gmail inbox messages
- Send emails (with and without attachments)
- Delete emails
- Access standard message fields (sender, recipient, subject, body, etc.)
- Support for email attachments
- AI-powered spam detection

### In Scope

- Basic email operations (read, send, delete)
- Gmail-specific client implementation
- Interface abstraction and dependency injection
- Comprehensive testing (unit and integration)
- Attachment handling
- Logging and error handling

### Out of Scope

- CC/BCC functionality
- Complex message filtering
- Authentication flow customization (uses standard OAuth)
- Multi-provider support (currently Gmail only)
- Folder/label management

## Interfaces

### `Message` Interface

```python
class Message(Protocol):
    @property
    def id(self) -> str: ...
    @property
    def from_(self) -> str: ...
    @property
    def to(self) -> str: ...
    @property
    def date(self) -> str: ...
    @property
    def subject(self) -> str: ...
    @property
    def body(self) -> str: ...
```

### `Attachment` Interface

```python
class Attachment(Protocol):
    @property
    def filename(self) -> str: ...
    @property
    def content_type(self) -> str: ...
    @property
    def data(self) -> bytes: ...
```

### `Client` Interface

```python
class Client(Protocol):
    def get_messages(self) -> Iterator[Message]: ...
    def get_message(self, message_id: str) -> Optional[Message]: ...
    def send_message(self, to: str, subject: str, body: str, 
                     attachments: Optional[list[Attachment]] = None) -> bool: ...
    def delete_message(self, message_id: str) -> bool: ...
```

### Factory Functions

```python
def get_client() -> Client: ...
def create_attachment(filename: str, data: bytes, content_type: Optional[str] = None) -> Attachment: ...
```

## Implementation: Gmail Client

The Gmail implementation provides a concrete implementation of the abstract interfaces defined in `mail_api`.

### Authentication

The Gmail client uses OAuth 2.0 for authentication:
1. The first time you run the client, it will prompt you to authorize access to your Gmail account through a browser
2. After authorization, a token will be saved to `token.json` for future use

### Setup

1. Set up a Google Cloud Project and enable the Gmail API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 Client ID credentials
   - Download the credentials file as `credentials.json`

2. Place the `credentials.json` file in your working directory or specify its location when initializing the client.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) as a modern Python package manager.

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install
```

## Usage Examples

### Basic Email Operations

```python
# Import the Gmail implementation
from mail_gmail_impl import get_gmail_client

# Create a Gmail client
client = get_gmail_client()

# Read messages from inbox
for message in client.get_messages():
    print(f"ID: {message.id}")
    print(f"From: {message.from_}")
    print(f"To: {message.to}")
    print(f"Date: {message.date}")
    print(f"Subject: {message.subject}")
    print(f"Body: {message.body}")
    print("-" * 50)

# Get a specific message
message = client.get_message("message_id_here")
if message:
    print(f"Subject: {message.subject}")

# Delete a message
success = client.delete_message("message_id_here")
print(f"Message deleted: {success}")
```

### Sending Emails with Attachments

```python
from mail_gmail_impl import get_gmail_client, create_gmail_attachment

# Create a Gmail client
client = get_gmail_client()

# Simple email without attachments
client.send_message(
    to="recipient@example.com",
    subject="Hello from Gmail API",
    body="This is a test message sent via the Gmail API."
)

# Email with attachments
with open("document.pdf", "rb") as file:
    data = file.read()
    attachment = create_gmail_attachment("document.pdf", data)

client.send_message(
    to="recipient@example.com",
    subject="Email with attachment",
    body="Please find the attached document.",
    attachments=[attachment]
)
```

### AI Spam Detection

```python
from mail_gmail_impl import get_gmail_client
from mail_ai_spam_detector import SpamDetector

# Create a Gmail client
client = get_gmail_client()

# Create a spam detector
detector = SpamDetector()

# Process messages and check for spam
for message in client.get_messages():
    is_spam = detector.is_spam(message)
    if is_spam:
        print(f"Spam detected: {message.subject}")
    else:
        print(f"Not spam: {message.subject}")
```

## Logging

The library uses Python's standard logging module. You can configure the logging level and handlers in your application:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to logging.DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('gmail_api.log')  # File output
    ]
)
```

## Testing

The project includes both unit tests (using mocking) and integration tests (using real credentials):

```bash
# Run all tests
pytest tests/src/tests

# Run only unit tests
pytest tests/src/tests/unit

# Run only integration tests
pytest tests/src/tests/integration
```

### Unit Test Example

```python
from unittest.mock import Mock
from mail_api import Message, Client

def test_client_interface():
    # Create mock message and client
    mock_message = Mock(spec=Message)
    mock_message.id.return_value = "msg123"
    mock_message.subject.return_value = "Test Subject"
    
    mock_client = Mock(spec=Client)
    mock_client.get_messages.return_value = iter([mock_message] * 5)
    
    # Verify behavior
    messages = list(mock_client.get_messages())
    assert len(messages) == 5
    assert messages[0].id == "msg123"
```

## Development Workflow

1. Clone this repository
2. Create a new branch for your feature or bugfix
3. Implement changes and write tests
4. Run tests to ensure everything works as expected
5. Commit changes and create a Pull Request

## Project Structure

- **mail_api/**: Core interfaces and protocols
- **mail_gmail_impl/**: Gmail implementation of mail_api interfaces
- **mail_ai_spam_detector/**: AI-powered spam detection
- **ai_conversation_client/**: AI conversation capabilities
- **tests/**: Unit and integration tests

## License

This project is licensed under the [Apache License 2.0](LICENSE).
