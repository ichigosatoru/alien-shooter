import json
import os
from datetime import datetime

class HighScoresManager:
    """Manage high scores persistence using JSON."""
    
    def __init__(self, filename='highscores.json'):
        """Initialize high scores manager."""
        self.filename = filename
        self.max_scores = 5
        self.high_scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_scores()
        else:
            # Create file with default scores
            default_scores = self._get_default_scores()
            self.save_scores(default_scores)
            return default_scores
    
    def _get_default_scores(self):
        """Return default high scores."""
        return [
            {"rank": 1, "name": "DUVERNON", "score": 9999999, "date": "2026-01-01"},
            {"rank": 2, "name": "LA MELO", "score": 500000, "date": "2026-01-02"},
            {"rank": 3, "name": "ASTRIDE", "score": 300000, "date": "2026-01-03"},
            {"rank": 4, "name": "DEREK", "score": 200000, "date": "2026-01-04"},
            {"rank": 5, "name": "AAA", "score": 100000, "date": "2026-01-05"}
        ]
    
    def save_scores(self, scores):
        """Save high scores to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(scores, f, indent=4)
        except IOError as e:
            print(f"Error saving high scores: {e}")
    
    def is_high_score(self, score):
        """Check if score qualifies for top 5."""
        if len(self.high_scores) < self.max_scores:
            return True
        return score > self.high_scores[-1]['score']
    
    def add_score(self, name, score):
        """Add a new score to high scores if it qualifies."""
        if not self.is_high_score(score):
            return False
        
        # Add new score
        new_entry = {
            "name": name.upper(),
            "score": int(score),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Add to list and sort by score (descending)
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 5
        self.high_scores = self.high_scores[:self.max_scores]
        
        # Update ranks
        for i, score_entry in enumerate(self.high_scores):
            score_entry['rank'] = i + 1
        
        # Save to file
        self.save_scores(self.high_scores)
        
        return True
    
    def get_high_scores(self):
        """Get all high scores."""
        return self.high_scores
    
    def get_rank(self, score):
        """Get what rank a score would be."""
        for i, entry in enumerate(self.high_scores):
            if score > entry['score']:
                return i + 1
        return None
