import requests
import base64
import logging
from urllib.parse import quote

# Setup logging
logger = logging.getLogger(__name__)

class GitHubError(Exception):
    """Exception raised for GitHub API errors."""
    
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def get_file_content(owner, repo, path, branch='main'):
    """
    Get the content of a file from a GitHub repository.
    
    Args:
        owner (str): The GitHub repository owner
        repo (str): The repository name
        path (str): Path to the file within the repository
        branch (str, optional): The branch to use. Defaults to 'main'.
    
    Returns:
        tuple: (content, file_size) - The file content and size in bytes
    
    Raises:
        GitHubError: If there's an error fetching the file
    """
    # Validate inputs
    for param in [owner, repo, path, branch]:
        if not isinstance(param, str) or not param.strip():
            raise GitHubError(f"Invalid parameter: {param}")
    
    # Sanitize and encode the path properly
    path = path.strip('/')
    encoded_path = quote(path)
    
    # Construct the GitHub API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{encoded_path}?ref={branch}"
    
    logger.debug(f"Fetching file from GitHub: {url}")
    
    try:
        # Make the request to GitHub API
        response = requests.get(
            url,
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'TwitchGithubReader/1.0'
            },
            timeout=10
        )
        
        # Handle HTTP errors
        if response.status_code != 200:
            error_data = response.json()
            error_message = error_data.get('message', 'Unknown error')
            
            if response.status_code == 404:
                raise GitHubError(f"Repository or file not found: {error_message}", 404)
            elif response.status_code == 403:
                raise GitHubError(f"API rate limit exceeded: {error_message}", 403)
            else:
                raise GitHubError(f"GitHub API error: {error_message}", response.status_code)
        
        # Parse the response
        data = response.json()
        
        # Check if it's a file
        if isinstance(data, dict) and data.get('type') == 'file':
            # Check if the file is too large
            if data.get('size', 0) > 1000000:  # 1MB limit
                raise GitHubError("File is too large (>1MB)", 413)
            
            # Check if it's a binary file
            if data.get('encoding') != 'base64':
                raise GitHubError("File is not a text file", 415)
            
            # Decode the content
            content = base64.b64decode(data.get('content', '')).decode('utf-8', errors='replace')
            file_size = data.get('size', 0)
            
            return content, file_size
        elif isinstance(data, dict) and data.get('type') == 'dir':
            raise GitHubError("The specified path is a directory, not a file", 400)
        else:
            raise GitHubError("Unexpected response format from GitHub API", 500)
    
    except requests.RequestException as e:
        logger.exception("Request error when accessing GitHub API")
        raise GitHubError(f"Failed to connect to GitHub: {str(e)}", 503)
    
    except ValueError as e:
        logger.exception("Error parsing JSON response from GitHub")
        raise GitHubError(f"Failed to parse GitHub response: {str(e)}", 500)
    
    except UnicodeDecodeError:
        raise GitHubError("Unable to decode file (might be binary)", 415)
    
    except Exception as e:
        logger.exception("Unexpected error processing GitHub file")
        raise GitHubError(f"Unexpected error: {str(e)}", 500)
