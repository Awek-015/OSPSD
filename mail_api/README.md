# Mail API

## Overview

The `mail_api` package defines a standardized set of interfaces (protocols) for email operations, enabling consistent interaction with any compliant email service implementation. It provides a clean abstraction layer that separates the interface from implementation details.

## Features

- Abstract `Client` interface for email operations
- Abstract `Message` interface for email content representation
- Abstract `Attachment` interface for email attachments
- Protocol-based design using Python's typing.Protocol
- Factory functions for creating clients and attachments

## Installation

```bash
# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
```

## Interface Definitions

### Message Protocol

The `Message` protocol defines the standard interface for email messages:

```python
@runtime_checkable
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

### Attachment Protocol

The `Attachment` protocol defines the standard interface for email attachments:

```python
@runtime_checkable
class Attachment(Protocol):
    @property
    def filename(self) -> str: ...
    
    @property
    def content_type(self) -> str: ...
    
    @property
    def data(self) -> bytes: ...
```

### Client Protocol

The `Client` protocol defines the standard interface for email operations:

```python
@runtime_checkable
class Client(Protocol):
    def get_messages(self) -> Iterator[Message]: ...
    
    def get_message(self, message_id: str) -> Optional[Message]: ...
    
    def send_message(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        attachments: Optional[list[Attachment]] = None
    ) -> bool: ...
    
    def delete_message(self, message_id: str) -> bool: ...
```

### Factory Functions

The package also defines factory functions to create clients and attachments:

```python
def get_client() -> Client: ...

def create_attachment(
    filename: str, 
    data: bytes, 
    content_type: Optional[str] = None
) -> Attachment: ...
```

## Usage

### Implementing the Interfaces

To create a new email provider implementation, implement the protocols defined in this package:

```python
from mail_api import Client, Message, Attachment
from typing import Iterator, Optional

class MyMessage(Message):
    def __init__(self, id, from_, to, date, subject, body):
        self._id = id
        self._from = from_
        self._to = to
        self._date = date
        self._subject = subject
        self._body = body
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def from_(self) -> str:
        return self._from
    
    @property
    def to(self) -> str:
        return self._to
    
    @property
    def date(self) -> str:
        return self._date
    
    @property
    def subject(self) -> str:
        return self._subject
    
    @property
    def body(self) -> str:
        return self._body

class MyClient(Client):
    def get_messages(self) -> Iterator[Message]:
        # Implementation for retrieving messages
        ...
    
    def get_message(self, message_id: str) -> Optional[Message]:
        # Implementation for retrieving a specific message
        ...
    
    def send_message(self, to: str, subject: str, body: str, 
                    attachments: Optional[list[Attachment]] = None) -> bool:
        # Implementation for sending a message
        ...
    
    def delete_message(self, message_id: str) -> bool:
        # Implementation for deleting a message
        ...
```

### Using the Interfaces

Client code should depend on the interfaces, not on specific implementations:

```python
from mail_api import Client, Message, Attachment

def process_emails(client: Client):
    # Works with any implementation of Client
    for message in client.get_messages():
        print(f"Processing email: {message.subject}")
        
        # Do something with the message
        if "urgent" in message.subject.lower():
            print(f"Found urgent message: {message.id}")
```

### Runtime Type Checking

The interfaces use `@runtime_checkable` Protocol, so you can use `isinstance()` to check if an object implements a specific interface:

```python
from mail_api import Message, Client

def validate_message(msg: object) -> bool:
    return isinstance(msg, Message)

def validate_client(client: object) -> bool:
    return isinstance(client, Client)
```

## Design Patterns

This API follows these design patterns:

1. **Interface Segregation Principle**: Separating interfaces for different concerns (Message, Attachment, Client)
2. **Dependency Inversion Principle**: High-level modules depend on abstractions, not concrete implementations
3. **Factory Pattern**: Using factory functions to create instances of implementations

## Available Implementations

- **mail_gmail_impl**: Gmail implementation of these interfaces

## Testing

To test implementations against these interfaces, use mocking and property checking:

```python
from unittest.mock import Mock
from mail_api import Message, Client

def test_client_implementation():
    # Create a mock that implements the Client interface
    mock_client = Mock(spec=Client)
    
    # Configure behavior
    mock_message = Mock(spec=Message)
    mock_message.id = "123"
    mock_message.subject = "Test"
    
    # Set up return values
    mock_client.get_messages.return_value = iter([mock_message])
    mock_client.get_message.return_value = mock_message
    mock_client.send_message.return_value = True
    mock_client.delete_message.return_value = True
    
    # Test the behavior
    messages = list(mock_client.get_messages())
    assert len(messages) == 1
    assert messages[0].subject == "Test"
```

## License

This project is licensed under the Apache License 2.0.
