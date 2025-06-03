# Onlive Google GenAI Testing

A production-ready Python application for testing Google's Gemini AI services with proper authentication, error handling, and logging.

## Features

- **Production-ready code**: Proper error handling, logging, and resource management
- **Modular architecture**: Clean separation of concerns with service classes
- **Multiple execution modes**: Single requests and chat conversations
- **Secure authentication**: Uses Google Cloud secret manager for credentials
- **Comprehensive logging**: Structured logging with appropriate levels

## Installation

1. Install dependencies using Poetry:
```bash
poetry install
```

2. Ensure your Google Cloud credentials are set up in the secret manager.

## Usage

### Method 1: Using Poetry with PYTHONPATH (Recommended)
```bash
cd /path/to/project
PYTHONPATH=. poetry run python -m app.services.google_gemini
```

### Method 2: Using direct Python execution
```bash
cd /path/to/project
python main.py
```

### Method 3: Using the run script
```bash
./run.sh
```

## Project Structure

```
app/
├── config/           # Configuration files
│   ├── logging_config.py
│   ├── secret_manager.py
│   └── settings.py
├── services/         # External service integrations
│   └── google_gemini.py
└── utils/           # Utility functions
    └── secrets.py
```

## API Usage

The `GoogleGeminiService` class provides two main methods:

### Single Content Generation
```python
from app.services.google_gemini import GoogleGeminiService

service = GoogleGeminiService()
response = service.generate_content("Your prompt here")
print(response.text)
```

### Chat Conversations
```python
with service.create_chat() as chat:
    response = chat.send_message("Your message")
    print(response.text)
```

## Error Handling

The application includes comprehensive error handling:
- Authentication failures
- API request errors
- Network timeouts
- Invalid responses

All errors are properly logged with context for debugging.

## Security

- Credentials are managed through Google Cloud Secret Manager
- No hardcoded secrets or API keys
- Environment-specific configuration support
