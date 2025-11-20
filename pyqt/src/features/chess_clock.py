'''
Chess Clock Implementation
Supports various time control formats
'''

import time

class ChessClock:
    def __init__(self, time_control="blitz"):
        '''
        Initialize chess clock
        time_control options:
        - "bullet": 1 minute
        - "blitz": 3 minutes
        - "rapid": 10 minutes
        - "classical": 30 minutes
        - "unlimited": no time limit
        - Custom: (minutes, increment) tuple
        '''
        self.time_controls = {
            "bullet": (60, 0),        # 1 min, 0 increment
            "blitz": (180, 2),        # 3 min, 2 sec increment
            "rapid": (600, 5),        # 10 min, 5 sec increment
            "classical": (1800, 0),   # 30 min, 0 increment
            "unlimited": (None, 0)    # No limit
        }

        if isinstance(time_control, str):
            initial_time, increment = self.time_controls.get(time_control, (180, 2))
        else:
            initial_time, increment = time_control

        self.time_remaining = {
            "white": initial_time,
            "black": initial_time
        }

        self.increment = increment
        self.active_color = None
        self.last_switch_time = None
        self.paused = True
        self.game_over = False

    def start(self, color="white"):
        '''Start the clock for specified color'''
        self.active_color = color
        self.last_switch_time = time.time()
        self.paused = False

    def switch_turn(self):
        '''Switch to other player's clock'''
        if self.paused or self.game_over:
            return

        # Update current player's time
        elapsed = time.time() - self.last_switch_time
        if self.time_remaining[self.active_color] is not None:
            self.time_remaining[self.active_color] -= elapsed

            # Add increment
            if self.increment > 0:
                self.time_remaining[self.active_color] += self.increment

            # Check if time ran out
            if self.time_remaining[self.active_color] <= 0:
                self.time_remaining[self.active_color] = 0
                self.game_over = True
                return

        # Switch to other color
        self.active_color = "black" if self.active_color == "white" else "white"
        self.last_switch_time = time.time()

    def pause(self):
        '''Pause the clock'''
        if not self.paused and not self.game_over:
            elapsed = time.time() - self.last_switch_time
            if self.time_remaining[self.active_color] is not None:
                self.time_remaining[self.active_color] -= elapsed
            self.paused = True

    def resume(self):
        '''Resume the clock'''
        if self.paused and not self.game_over:
            self.last_switch_time = time.time()
            self.paused = False

    def get_time(self, color):
        '''Get remaining time for a color'''
        if self.time_remaining[color] is None:
            return None

        remaining = self.time_remaining[color]

        # If this color is active and not paused, subtract elapsed time
        if color == self.active_color and not self.paused and not self.game_over:
            elapsed = time.time() - self.last_switch_time
            remaining -= elapsed

        return max(0, remaining)

    def format_time(self, seconds):
        '''Format time as MM:SS or HH:MM:SS'''
        if seconds is None:
            return "Unlimited"

        seconds = int(seconds)

        if seconds >= 3600:  # More than 1 hour
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}:{secs:02d}"

    def is_time_out(self, color):
        '''Check if a player ran out of time'''
        time_left = self.get_time(color)
        return time_left is not None and time_left <= 0

    def reset(self, time_control=None):
        '''Reset the clock'''
        if time_control:
            self.__init__(time_control)
        else:
            # Reset to initial values
            for color in ["white", "black"]:
                if self.time_remaining[color] is not None:
                    if self.increment > 0:
                        self.time_remaining[color] = 180  # Default 3 min
                    else:
                        self.time_remaining[color] = 180

        self.active_color = None
        self.last_switch_time = None
        self.paused = True
        self.game_over = False
