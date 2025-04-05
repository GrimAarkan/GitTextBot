document.addEventListener('DOMContentLoaded', function() {
    // Functionality for the test API section
    const testBtn = document.getElementById('testBtn');
    if (testBtn) {
        testBtn.addEventListener('click', function() {
            // Get form values
            const owner = document.getElementById('owner').value.trim();
            const repo = document.getElementById('repo').value.trim();
            const path = document.getElementById('path').value.trim();
            const branch = document.getElementById('branch').value.trim() || 'main';
            const format = document.getElementById('format').value;
            
            // Validate required fields
            if (!owner || !repo || !path) {
                alert('Please fill in all required fields (owner, repo, path)');
                return;
            }
            
            // Build the API URL
            const apiUrl = `/api/github/read?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}&path=${encodeURIComponent(path)}&branch=${encodeURIComponent(branch)}&format=${format}`;
            
            // Show loading state
            const resultContainer = document.getElementById('resultContainer');
            const resultElem = document.getElementById('result');
            resultContainer.style.display = 'block';
            resultElem.textContent = 'Loading...';
            
            // Fetch from the API
            fetch(apiUrl)
                .then(response => {
                    if (format === 'json') {
                        return response.json();
                    } else {
                        return response.text();
                    }
                })
                .then(data => {
                    if (format === 'json') {
                        resultElem.textContent = JSON.stringify(data, null, 2);
                    } else {
                        resultElem.textContent = data;
                    }
                })
                .catch(error => {
                    resultElem.textContent = `Error: ${error.message}`;
                });
        });
    }
    
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add syntax highlighting for code blocks if Prism is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
    
    // Make external links open in a new tab
    document.querySelectorAll('a').forEach(link => {
        if (link.host !== window.location.host && !link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});
