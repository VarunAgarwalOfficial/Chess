'''
Settings and Statistics Management
Handles game configuration and player statistics
'''

import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "chess_settings.json"
        self.stats_file = "chess_stats.json"

        # Default settings
        self.default_settings = {
            "theme": "classic",
            "board_colors": {
                "light": [241, 218, 179],
                "dark": [182, 136, 96]
            },
            "time_control": "blitz",
            "show_legal_moves": True,
            "show_last_move": True,
            "show_coordinates": True,
            "animations_enabled": True,
            "sound_enabled": True,
            "auto_queen_promotion": False,
            "difficulty": "medium",
            "player_name": "Player"
        }

        # Default statistics
        self.default_stats = {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "rating": 1200,
            "highest_rating": 1200,
            "win_streak": 0,
            "longest_win_streak": 0,
            "total_moves": 0,
            "checkmates_delivered": 0,
            "pieces_captured": {
                "pawn": 0,
                "knight": 0,
                "bishop": 0,
                "rook": 0,
                "queen": 0
            },
            "opening_stats": {},
            "time_played_minutes": 0
        }

        self.settings = self.load_settings()
        self.stats = self.load_stats()

    def load_settings(self):
        '''Load settings from file'''
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new settings
                    settings = self.default_settings.copy()
                    settings.update(loaded)
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.default_settings.copy()
        return self.default_settings.copy()

    def save_settings(self):
        '''Save settings to file'''
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def load_stats(self):
        '''Load statistics from file'''
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    stats = self.default_stats.copy()
                    stats.update(loaded)
                    return stats
            except Exception as e:
                print(f"Error loading stats: {e}")
                return self.default_stats.copy()
        return self.default_stats.copy()

    def save_stats(self):
        '''Save statistics to file'''
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving stats: {e}")
            return False

    def update_game_result(self, result, opponent_rating=1200):
        '''Update statistics after a game'''
        self.stats["games_played"] += 1

        if result == "win":
            self.stats["wins"] += 1
            self.stats["win_streak"] += 1
            if self.stats["win_streak"] > self.stats["longest_win_streak"]:
                self.stats["longest_win_streak"] = self.stats["win_streak"]

            # Update rating (simplified Elo)
            self.stats["rating"] += self.calculate_elo_change(True, opponent_rating)

        elif result == "loss":
            self.stats["losses"] += 1
            self.stats["win_streak"] = 0
            self.stats["rating"] += self.calculate_elo_change(False, opponent_rating)

        else:  # draw
            self.stats["draws"] += 1
            self.stats["win_streak"] = 0

        # Update highest rating
        if self.stats["rating"] > self.stats["highest_rating"]:
            self.stats["highest_rating"] = self.stats["rating"]

        # Ensure rating doesn't go below 100
        self.stats["rating"] = max(100, self.stats["rating"])

        self.save_stats()

    def calculate_elo_change(self, won, opponent_rating, k_factor=32):
        '''Calculate Elo rating change'''
        # Expected score
        expected = 1 / (1 + 10 ** ((opponent_rating - self.stats["rating"]) / 400))

        # Actual score
        actual = 1 if won else 0

        # Rating change
        change = k_factor * (actual - expected)

        return int(change)

    def record_checkmate(self):
        '''Record a checkmate'''
        self.stats["checkmates_delivered"] += 1
        self.save_stats()

    def record_capture(self, piece_type):
        '''Record a piece capture'''
        if piece_type in self.stats["pieces_captured"]:
            self.stats["pieces_captured"][piece_type] += 1
            self.save_stats()

    def record_move(self):
        '''Record a move'''
        self.stats["total_moves"] += 1

    def record_opening(self, opening_name):
        '''Record an opening played'''
        if opening_name not in self.stats["opening_stats"]:
            self.stats["opening_stats"][opening_name] = 0
        self.stats["opening_stats"][opening_name] += 1

    def add_playtime(self, minutes):
        '''Add playtime in minutes'''
        self.stats["time_played_minutes"] += minutes
        self.save_stats()

    def get_win_rate(self):
        '''Calculate win rate percentage'''
        if self.stats["games_played"] == 0:
            return 0.0
        return (self.stats["wins"] / self.stats["games_played"]) * 100

    def reset_stats(self):
        '''Reset all statistics'''
        self.stats = self.default_stats.copy()
        self.save_stats()

    def get_setting(self, key):
        '''Get a setting value'''
        return self.settings.get(key)

    def set_setting(self, key, value):
        '''Set a setting value'''
        self.settings[key] = value
        self.save_settings()
