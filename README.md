# Gmail Mail Client Interface

> **Note**: This repository is currently in the **interface definition** phase. Only the interface and its tests are implemented; functional logic will follow in later stages.

## Overview

This project defines a standardized API for interacting with Gmail. It is organized into modular components:

- **mail_api**: Defines abstract interfaces for email clients and messages.
- **mail_gmail_impl**: (To be implemented) Gmail-specific implementation of `mail_api`.
- **tests**: Contains interface-level tests using mocking.

## Project Scope

### Minimum Viable Product (MVP)

- Read Gmail inbox messages
- Send simple emails
- Delete emails
- Access standard message fields (sender, recipient, subject, body, etc.)
- Support for email attachments

### In Scope

- Basic email operations (read, send, delete)
- Gmail-specific client implementation
- Interface abstraction and dependency injection
- Interface mocking tests
- Attachments support

### Out of Scope

- CC/BCC, filtering, or search
- Authentication flow (assumes valid credentials)
- Multi-provider support
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
    def send_message(self, to: str, subject: str, body: str) -> bool: ...
    def delete_message(self, message_id: str) -> bool: ...
```

### Factory Functions

```python
def get_client() -> Client:
    ...

def create_attachment(filename: str, data: bytes, content_type: Optional[str] = None) -> Attachment:
    ...
```

## Testing

- Tests are written using the `pytest` framework, with `unittest.mock` used to mock interface definitions.
- Each test validates return types and behaviors as defined in the interface.

Example:

```python
from unittest.mock import Mock
from mail_api import Message, Client

mock_message = Mock(spec=Message)
assert isinstance(mock_message.id, str)

mock_client = Mock(spec=Client)
mock_client.get_messages.return_value = iter([mock_message] * 5)
assert len(list(mock_client.get_messages())) == 5
```

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

## Running Tests

```bash
pytest tests/src/tests
```

## Example Usage (Post-Implementation)

```python
import mail_api

client = mail_api.get_client()
for msg in client.get_messages():
    print(f"{msg.subject} from {msg.from_}")

client.send_message("user@example.com", "Subject", "Body")

# Create and attach a file
with open("document.pdf", "rb") as f:
    data = f.read()
    attachment = mail_api.create_attachment("document.pdf", data)
```

## Development Workflow

1. Clone this repo
2. Create a new branch (`interface-definition`)
3. Modify code and write tests
4. Commit and push
5. Create a Pull Request

## License

This project is licensed under the [Apache License 2.0](LICENSE).
