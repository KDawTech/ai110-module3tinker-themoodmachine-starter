# mood_analyzer.py
# mood_analyzer.py

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A simple rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        self.positive_words.update({
            "hopeful", "proud", "finished", "works", "clean",
            "fire", "sick", "😄", "🔥"
        })

        self.negative_words.update({
            "trash", "stuck", "died", "hated", "exhausted",
            "worst", "broken", "💀"
        })

        self.negation_words = {"not", "no", "never", "dont", "don't", "cant", "can't"}

    def preprocess(self, text: str) -> List[str]:
        text = text.lower().strip()
        tokens = re.findall(r"[a-zA-Z']+|[😄🔥💀]", text)
        return tokens

    def _score_details(self, text: str) -> Dict:
        tokens = self.preprocess(text)
        score = 0
        positive_hits = []
        negative_hits = []

        for i, token in enumerate(tokens):
            value = 0

            if token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1

            # Simple negation handling: "not happy" becomes negative,
            # and "not bad" becomes positive.
            if value != 0 and i > 0 and tokens[i - 1] in self.negation_words:
                value *= -1

            score += value

            if value > 0:
                positive_hits.append(token)
            elif value < 0:
                negative_hits.append(token)

        return {
            "tokens": tokens,
            "score": score,
            "positive_hits": positive_hits,
            "negative_hits": negative_hits,
        }

    def score_text(self, text: str) -> int:
        details = self._score_details(text)
        return details["score"]

    def predict_label(self, text: str) -> str:
        details = self._score_details(text)

        score = details["score"]
        positive_hits = details["positive_hits"]
        negative_hits = details["negative_hits"]

        if positive_hits and negative_hits:
            return "mixed"
        elif score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    def explain(self, text: str) -> str:
        details = self._score_details(text)

        return (
            f"Tokens = {details['tokens']} | "
            f"Score = {details['score']} | "
            f"Positive hits = {details['positive_hits']} | "
            f"Negative hits = {details['negative_hits']}"
        )