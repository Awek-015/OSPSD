"""Test for Gmail attachment functionality"""

import os
from mail_gmail_impl import create_gmail_attachment


def test_attachment():
    # Create a test file
    test_file_path = "test_attachment.txt"

    with open(test_file_path, "w") as f:
        f.write("This is a test attachment file content.")

    try:
        # Read file content
        with open(test_file_path, "rb") as f:
            file_data = f.read()

        # Create attachment object
        print("Creating attachment object...")
        attachment = create_gmail_attachment(
            filename="test_attachment.txt", data=file_data, content_type="text/plain"
        )

        # Verify attachment object
        print(f"Attachment filename: {attachment.filename}")
        print(f"Attachment content type: {attachment.content_type}")
        print(f"Attachment data size: {len(attachment.data)} bytes")

        print("\nAttachment object created successfully!")

    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


if __name__ == "__main__":
    try:
        test_attachment()
    except Exception as e:
        print(f"Error occurred during testing: {e}")
