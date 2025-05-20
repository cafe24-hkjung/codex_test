import functools
import time
import asyncio
import logging
from typing import Callable, Any, TypeVar
from datetime import datetime

F = TypeVar('F', bound=Callable[..., Any])

def async_retry(retries: int = 3, delay: float = 1.0):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

def performance_monitor(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        start_memory = memory_usage()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            end_memory = memory_usage()
            
            execution_time = end_time - start_time
            memory_diff = end_memory - start_memory
            
            logging.info(f"""
                Function: {func.__name__}
                Execution Time: {execution_time:.4f} seconds
                Memory Usage: {memory_diff:.2f} MB
                Timestamp: {datetime.now()}
            """)
    
    return wrapper

def validate_input(validator: Callable[[Any], bool]):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not validator(*args, **kwargs):
                raise ValueError(f"Invalid input for {func.__name__}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def memory_usage():
    import psutil
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # Convert to MB 