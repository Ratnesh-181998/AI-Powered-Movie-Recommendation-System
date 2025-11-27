from functools import wraps
import time
import traceback
from flask import request
from app.utils.logger import log_request, log_error

def log_api_call(f):
    """Decorator to log API calls with timing"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        endpoint = request.path
        method = request.method
        
        try:
            # Execute the function
            result = f(*args, **kwargs)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Get status code
            if isinstance(result, tuple):
                status_code = result[1] if len(result) > 1 else 200
            else:
                status_code = 200
            
            # Log the request
            log_request(endpoint, method, status_code, response_time)
            
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            log_request(endpoint, method, 500, response_time)
            log_error(type(e).__name__, str(e), traceback.format_exc())
            raise
    
    return decorated_function
