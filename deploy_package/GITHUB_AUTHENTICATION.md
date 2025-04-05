# Setting Up GitHub Authentication

This document explains how to set up GitHub authentication for the GitHub File Reader API to avoid rate limiting issues.

## Why You Need This

GitHub's API has rate limits:
- **Without authentication**: 60 requests per hour per IP address
- **With authentication**: 5,000 requests per hour per user token

If you're experiencing the error "API rate limit exceeded", you need to set up authentication.

## Getting a GitHub Personal Access Token

1. **Log in to your GitHub account**

2. **Go to Settings**
   - Click on your profile picture in the top-right corner
   - Select "Settings" from the dropdown menu

3. **Access Developer Settings**
   - Scroll down and click on "Developer settings" in the left sidebar

4. **Create a Personal Access Token**
   - Click on "Personal access tokens" → "Tokens (classic)"
   - Click "Generate new token" → "Generate new token (classic)"
   - Give your token a descriptive name (e.g., "GitHub File Reader API")
   - For scopes, you only need public repository access, so select:
     - `public_repo` (if you want to access public repositories only)
     - Or `repo` (if you need access to private repositories too)
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately! You won't be able to see it again.

## Setting Up the Token in Render

1. **Go to your Render Dashboard**

2. **Select Your Service**
   - Click on the GitHub File Reader API service

3. **Add Environment Variable**
   - Click on "Environment" tab
   - Click "Add Environment Variable"
   - For the key, enter: `GITHUB_TOKEN`
   - For the value, paste your GitHub Personal Access Token
   - Click "Save Changes"

4. **Redeploy Your Application**
   - After adding the environment variable, click "Manual Deploy" and select "Clear build cache & deploy"

## Testing Authentication

Once deployed with the token, your API should now use authenticated requests to GitHub, which will give you:

- Higher rate limits (5,000 requests/hour vs 60 requests/hour)
- Ability to access private repositories (if you included that scope)

The API will automatically detect and use the GitHub token if it's available.