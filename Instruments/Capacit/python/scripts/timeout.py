import time 
import traceback

class Timeout: 
    def __init__(self, interval):
        """Sets the timeout period (in minutes)."""
        self._interval = interval  # ✅ Correctly initialize instance variable
        self._unit = 60  # Timeout in seconds
        self._counter = time.perf_counter()  # ✅ Ensure this starts at the correct time
        self._cancel = False  # Use `False` instead of `1`/`0` for clarity

    def check(self):
        """Returns `0` (exit) if timeout or cancellation has occurred, otherwise `1`."""
        current_time = time.perf_counter()
        elapsed_time = current_time - self._counter

        if self._cancel:
            print("Cancelled script manually")
            return 0
        
        if elapsed_time > self._interval * self._unit:
            print("Cancelled script due to timeout")
            return 0
        
        return 1  # ✅ Keep running

    def update(self):
        """Resets the timeout countdown."""
        self._counter = time.perf_counter()

    def cancel(self):
        """Manually cancels the timeout and prints debug info."""
        self._cancel = True