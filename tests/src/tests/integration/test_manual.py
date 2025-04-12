"""Manual test for Gmail client implementation"""

import os
from mail_gmail_impl import get_gmail_client


def test_gmail():
    # Check for credentials file
    if not os.path.exists("credentials.json"):
        print("Error: credentials.json not found.")
        print(
            "Please follow the setup instructions in the mail_gmail_impl/README.md to create credentials."
        )
        return

    # Create Gmail client (will open browser for auth first time)
    try:
        print("Creating Gmail client...")
        client = get_gmail_client()

        # Display first 5 emails from inbox
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

        # Prompt user to decide whether to send a test email
        should_send = input("\nSend a test email? (y/n): ").lower() == "y"

        if should_send:
            # Send test email
            your_email = input("\nEnter your email address: ")
            print(f"\n====== Sending test email to {your_email} ======")
            result = client.send_message(
                to=your_email,
                subject="Test Email - Gmail API Interface Test",
                body="This is a test email sent via our Gmail API interface implementation.",
            )
            print(f"Email sent {'successfully' if result else 'failed'}")
    except Exception as e:
        print(f"Error occurred during testing: {e}")


if __name__ == "__main__":
    test_gmail()
