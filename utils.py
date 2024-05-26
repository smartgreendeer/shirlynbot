import time
import replicate  # Assuming replicate module is imported

# Define a debounce function for replicate.run
def debounce_replicate_run(func, delay):
    last_call = 0
    
    def debounced_func(*args, **kwargs):
        nonlocal last_call
        
        # Calculate time elapsed since last call
        elapsed = time.time() - last_call
        
        # If elapsed time is less than delay, wait
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        # Call the function
        result = func(*args, **kwargs)
        
        # Update last_call time
        last_call = time.time()
        
        return result
    
    return debounced_func

# Wrap replicate.run with debounce function
debounced_replicate_run = debounce_replicate_run(replicate.run, delay=2)  # Adjust delay as needed
