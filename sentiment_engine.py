import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class SentimentEngine:
    def __init__(self):
        # Download VADER lexicon if not present
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)

        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        """
        Returns a dictionary with compound score and label.
        Tier 2: Analyzes individual statements.
        """
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']

        # Threshold logic
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "score": compound,
            "label": label
        }

    def analyze_trend(self, scores_history):
        """
        Tier 2 Bonus: Summarizes the trend/shift in mood.
        """
        if len(scores_history) < 2:
            return "Stable (Not enough data for trend)"

        start_avg = sum(scores_history[:len(scores_history) // 2]) / (len(scores_history) // 2)
        end_avg = sum(scores_history[len(scores_history) // 2:]) / (len(scores_history) - len(scores_history) // 2)

        diff = end_avg - start_avg

        if diff > 0.1:
            return "Mood Improved 📈"
        elif diff < -0.1:
            return "Mood Declined 📉"
        else:
            return "Mood remained relatively stable ➡"