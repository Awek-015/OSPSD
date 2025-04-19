#!/usr/bin/env python3
"""
Manual Test Script - Gmail Client Implementation

This script provides a simple command-line interface for interacting with the Gmail API implementation
for manual testing and verification. It is not part of the automated test suite but is used for
development and debugging purposes.
"""

import os
import sys
import logging
from mail_gmail_impl import get_gmail_client, create_gmail_attachment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("manual_test.log")],
)
logger = logging.getLogger(__name__)


def manual_test():
    """Run an interactive test of the Gmail client"""
    # Check for credentials file
    if not os.path.exists("credentials.json"):
        logger.error("credentials.json file not found.")
        print("Error: credentials.json file not found.")
        print(
            "Please follow the setup instructions in mail_gmail_impl/README.md to create credentials."
        )
        return 1

    # Create Gmail client (will open browser for auth on first run)
    try:
        print("Creating Gmail client...")
        client = get_gmail_client()
        logger.info("Gmail client created successfully")
        print("Gmail client created successfully!")

        while True:
            # Display main menu
            print("\n===== Gmail API Test Menu =====")
            print("1. Show first 5 emails from inbox")
            print("2. Send test email (without attachment)")
            print("3. Send test email (with attachment)")
            print("4. Exit")

            choice = input("\nSelect an operation (1-4): ")

            if choice == "1":
                # Display first 5 emails
                print("\n====== Inbox Messages ======")
                count = 0
                for message in client.get_messages():
                    print(f"From: {message.from_}")
                    print(f"Subject: {message.subject}")
                    print(f"Date: {message.date}")
                    print("-" * 30)
                    count += 1
                    if count >= 5:
                        break

                if count == 0:
                    print("No messages found.")
                    logger.warning("No messages found in inbox")

            elif choice == "2" or choice == "3":
                # Send test email
                your_email = input(
                    "\nEnter the email address to receive the test email: "
                )

                if not your_email or "@" not in your_email:
                    print("Invalid email address.")
                    logger.warning(f"Invalid email address entered: {your_email}")
                    continue

                print(f"\n====== Sending test email to {your_email} ======")
                logger.info(f"Sending test email to {your_email}")

                attachments = None
                if choice == "3":
                    # Create test attachment
                    print("Creating test attachment...")
                    attachment_data = (
                        b"This is a test attachment content."  # ASCII characters only
                    )
                    attachment = create_gmail_attachment(
                        filename="test_attachment.txt",
                        data=attachment_data,
                        content_type="text/plain",
                    )
                    attachments = [attachment]
                    print("Attachment created successfully!")
                    logger.info("Test attachment created successfully")

                result = client.send_message(
                    to=your_email,
                    subject="Test Email - Gmail API Interface Test",
                    body="This is a test email sent via our Gmail API interface implementation."
                    + ("\n\nThis email includes an attachment." if attachments else ""),
                    attachments=attachments,
                )

                if result:
                    print("Email sent successfully")
                    logger.info(f"Email sent successfully to {your_email}")
                else:
                    print("Email sending failed")
                    logger.error(f"Failed to send email to {your_email}")

            elif choice == "4":
                print("Exiting test program.")
                logger.info("Test program exited by user")
                break

            else:
                print("Invalid choice, please try again.")
                logger.warning(f"Invalid menu choice: {choice}")

    except Exception as e:
        error_msg = f"An error occurred during testing: {e}"
        print(error_msg)
        logger.exception(error_msg)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(manual_test())
