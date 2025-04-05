import time
from collections import defaultdict
import threading
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    A simple rate limiter that limits requests based on IP address.
    
    Attributes:
        max_requests (int): Maximum number of requests allowed in the time window
        time_window (int): Time window in seconds
        request_counts (dict): Dictionary mapping IP addresses to request counts and timestamps
        lock (threading.Lock): Lock for thread-safe operations
    """
    
    def __init__(self, max_requests, time_window):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests (int): Maximum number of requests allowed in the time window
            time_window (int): Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_counts = defaultdict(list)
        self.lock = threading.Lock()
        
        # Start a cleanup thread
        self._start_cleanup_thread()
    
    def allow_request(self, ip_address):
        """
        Check if a request from the given IP address should be allowed.
        
        Args:
            ip_address (str): The IP address of the client
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            
            # Remove expired timestamps
            self.request_counts[ip_address] = [
                timestamp for timestamp in self.request_counts[ip_address] 
                if current_time - timestamp < self.time_window
            ]
            
            # Check if the limit is exceeded
            if len(self.request_counts[ip_address]) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return False
            
            # Add current timestamp to the list
            self.request_counts[ip_address].append(current_time)
            return True
    
    def _cleanup_expired_records(self):
        """Remove expired records to prevent memory leaks."""
        with self.lock:
            current_time = time.time()
            expired_ips = []
            
            for ip, timestamps in self.request_counts.items():
                # Remove expired timestamps
                valid_timestamps = [ts for ts in timestamps if current_time - ts < self.time_window]
                self.request_counts[ip] = valid_timestamps
                
                # Mark for removal if no valid timestamps remain
                if not valid_timestamps:
                    expired_ips.append(ip)
            
            # Remove entries with no valid timestamps
            for ip in expired_ips:
                del self.request_counts[ip]
    
    def _start_cleanup_thread(self):
        """Start a daemon thread to periodically clean up expired records."""
        def cleanup_job():
            while True:
                time.sleep(self.time_window / 2)  # Clean up at half the time window interval
                self._cleanup_expired_records()
        
        cleanup_thread = threading.Thread(target=cleanup_job, daemon=True)
        cleanup_thread.start()
