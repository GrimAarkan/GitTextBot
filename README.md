# GitHub File Reader API for Twitch Chat Commands

A Python-based API service that enables Twitch chatbots to retrieve and display text file content from public GitHub repositories.

## Features

- Retrieve file content from public GitHub repositories
- Multiple response formats: plain text, JSON, and "oneline" for chat compatibility
- Rate limiting for security
- Maximum file size limit (1MB)
- Designed for easy integration with Twitch chatbots

## Usage with Twitch Chatbots

### Nightbot Example

```
!addcom !github $(urlfetch https://your-deployed-url.com/api/github/read?owner=$(1)&repo=$(2)&path=$(3)&format=oneline)
```

Then in your Twitch chat:
```
!github microsoft vscode README.md
```

## API Documentation

The API is available at `/api/github/read` with the following parameters:

- `owner`: GitHub repository owner/username
- `repo`: Repository name
- `path`: Path to the file within the repository
- `branch`: (Optional) Branch name, defaults to 'main'
- `format`: (Optional) Response format, can be 'plain', 'json', 'oneline'. Defaults to 'plain'
- `max_length`: (Optional) Maximum number of characters to return, defaults to 500
