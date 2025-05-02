
# Mail AI Spam Detector

A simple Python component to:
- Crawl your mailbox using a mail client (e.g., Gmail API)
- Analyze each email via an AI conversation client (e.g., Gemini)
- Predict the probability of an email being spam
- Output results into a CSV file

## Features

- Crawl emails
- Classify emails using an AI model
- Generate a CSV report with:
  - `mail_id`
  - `Pct_spam` (Spam probability %)

## Installation

Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install the package and its dependencies:

```bash
uv pip install -e .
```

## Environment Setup

You must have:
- A valid `credentials.json` for Gmail API access
- A `.env` file containing your Gemini API key:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

Run the spam detector:

```bash
python src/mail_ai_spam_detector/detector.py
```

This will create a `spam_detection_results.csv` file containing the analysis results.

## Output CSV Format

| mail_id          | Pct_spam |
|------------------|----------|
| unique_mail_id_1 | 12.5     |
| unique_mail_id_2 | 88.0     |

Each row corresponds to one analyzed email.

## Running Tests

To run the live integration tests:

```bash
pytest tests/src/tests/integration/test_detector_live.py
```

If you want to skip live tests (e.g., on CI pipelines):

```bash
export SKIP_LIVE_TESTS=1
```

## Notes

- Live tests require valid Gmail and Gemini service access.
- Tests that require manual checking are marked with `xfail`.
- AI output is clamped between 0% and 100% to ensure consistency.
