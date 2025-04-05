# Deployment Guide

This guide provides instructions for deploying the GitHub File Reader API to various platforms.

## Deploying to Render

### Option 1: Deploy from GitHub

1. Push your code to a GitHub repository
2. Log in to [Render](https://render.com/)
3. Click "New" and select "Web Service"
4. Connect your GitHub account and select the repository
5. Configure your web service:
   - **Name**: Choose a name for your service
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
6. Click "Create Web Service"

### Option 2: Deploy using Poetry

1. Push your code to a GitHub repository
2. Log in to [Render](https://render.com/)
3. Click "New" and select "Web Service"
4. Connect your GitHub account and select the repository
5. Configure your web service:
   - **Name**: Choose a name for your service
   - **Runtime**: Python 3
   - **Build Command**: `poetry install`
   - **Start Command**: `poetry run gunicorn --bind 0.0.0.0:$PORT main:app`
6. Click "Create Web Service"

## Deploying to Replit

1. Create a new Replit project or use your existing one
2. Make sure your Replit project has the following files:
   - `main.py` - The application entry point
   - `.replit` - Configuration file for Replit
   - `pyproject.toml` - Dependencies configuration
3. Click the "Run" button to start your application
4. To make your application permanently available:
   - Click the "Deploy" tab at the top of the workspace
   - Follow the instructions to deploy your application

### Using with Twitch Chatbots

Once deployed, you can use your API with various Twitch chatbots:

#### Nightbot Example

```
!addcom !github $(urlfetch https://your-deployed-url.com/api/github/read?owner=$(1)&repo=$(2)&path=$(3)&format=oneline)
```

#### StreamElements Example

```
!addcom !github ${urlfetch https://your-deployed-url.com/api/github/read?owner=${1}&repo=${2}&path=${3}&format=oneline}
```

#### Moobot Example

```
!addcommand !github <url:https://your-deployed-url.com/api/github/read?owner=<1>&repo=<2>&path=<3>&format=oneline>
```