import csv
from typing import List
from mail_api import Message, Client
from ai_conversation_client.client import AIConversationClient


class SpamDetector:
    """Spam detector that uses a mail client and an AI conversation client."""

    def __init__(self, mail_client: Client, ai_client: AIConversationClient) -> None:
        self.mail_client = mail_client
        self.ai_client = ai_client

    def crawl_emails(self, max_count: int = 10) -> List[Message]:
        """Fetch emails from the mailbox."""
        return list(self.mail_client.get_messages())[:max_count]

    def analyze_email(self, session_id: str, email: Message) -> float:
        """Analyze a single email and return spam probability percentage."""
        prompt = (
            "You are an email classifier. Given the following email content, "
            "analyze and output the probability that this email is spam. "
            "Reply only with a number between 0 and 100. No explanation.\n\n"
            f"Subject: {email.subject}\n"
            f"From: {email.from_}\n"
            f"To: {email.to}\n"
            f"Date: {email.date}\n"
            f"Body: {email.body}\n"
        )

        response = self.ai_client.send_message(session_id, prompt)
        content = response.get("content", "").strip()

        try:
            probability = float(content)
            return max(0.0, min(100.0, probability))  # Clamp to [0, 100]
        except ValueError:
            return 0.0

    def detect_spam(self, output_csv: str, max_emails: int = 10) -> None:
        """Run detection and save results to a CSV file."""
        session_id = self.ai_client.start_new_session(user_id="spam_detector")
        emails = self.crawl_emails(max_count=max_emails)

        rows = []
        for email in emails:
            pct_spam = self.analyze_email(session_id, email)
            rows.append({
                "mail_id": email.id,
                "Pct_spam": pct_spam
            })

        self.ai_client.end_session(session_id)

        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["mail_id", "Pct_spam"])
            writer.writeheader()
            writer.writerows(rows)
