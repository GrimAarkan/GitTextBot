import os
import logging
from flask import Flask, request, jsonify, render_template, abort
import github_service
from rate_limiter import RateLimiter

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

# Initialize rate limiter (500 requests per hour per IP)
rate_limiter = RateLimiter(500, 3600)

@app.route('/')
def index():
    """Render the main page with API documentation."""
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    """Render the detailed API documentation page."""
    return render_template('documentation.html')

@app.route('/api/github/read', methods=['GET'])
def read_github_file():
    """
    API endpoint to read a text file from a GitHub repository.
    
    Query Parameters:
    - owner: GitHub repository owner/username
    - repo: Repository name
    - path: Path to the file within the repository
    - branch: (Optional) Branch name, defaults to 'main'
    - format: (Optional) Response format, can be 'plain', 'json', 'oneline'. Defaults to 'plain'
    - max_length: (Optional) Maximum number of characters to return, defaults to 500
    
    Returns:
        JSON or plain text response with the file content
    """
    client_ip = request.remote_addr
    
    # Apply rate limiting
    if not rate_limiter.allow_request(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return jsonify({
            "error": "Rate limit exceeded. Please try again later.",
            "status": 429
        }), 429
    
    # Get request parameters
    owner = request.args.get('owner')
    repo = request.args.get('repo')
    file_path = request.args.get('path')
    branch = request.args.get('branch', 'main')
    response_format = request.args.get('format', 'plain')
    max_length = request.args.get('max_length', 500)
    
    # Validate required parameters
    if not all([owner, repo, file_path]):
        return jsonify({
            "error": "Missing required parameters. Please provide 'owner', 'repo', and 'path'.",
            "status": 400
        }), 400
    
    try:
        max_length = int(max_length)
        if max_length <= 0 or max_length > 5000:
            max_length = 500  # Default to 500 if invalid
    except ValueError:
        max_length = 500  # Default to 500 if not a valid integer
    
    try:
        # Fetch file content from GitHub
        content, file_size = github_service.get_file_content(owner, repo, file_path, branch)
        
        # Truncate content if necessary and add indicator
        if max_length and len(content) > max_length:
            truncated = True
            content = content[:max_length] + "..."
        else:
            truncated = False
        
        # Format the response
        if response_format == 'json':
            return jsonify({
                "content": content,
                "truncated": truncated,
                "full_size": file_size,
                "repo": f"{owner}/{repo}",
                "path": file_path,
                "branch": branch,
                "status": 200
            })
        elif response_format == 'oneline':
            # Format for easier use in Twitch chat - single line
            content = content.replace('\n', ' ').replace('\r', ' ')
            while '  ' in content:  # Remove extra spaces
                content = content.replace('  ', ' ')
            return content
        else:  # plain format
            return content
    
    except github_service.GitHubError as e:
        logger.error(f"GitHub error: {str(e)}")
        
        if response_format == 'json':
            return jsonify({
                "error": str(e),
                "status": e.status_code
            }), e.status_code
        else:
            return f"Error: {str(e)}", e.status_code
    
    except Exception as e:
        logger.exception("Unexpected error")
        
        if response_format == 'json':
            return jsonify({
                "error": "An unexpected error occurred",
                "status": 500
            }), 500
        else:
            return "Error: An unexpected error occurred", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
