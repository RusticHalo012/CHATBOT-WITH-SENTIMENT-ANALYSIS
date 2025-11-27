import random


class ChatBot:
    def __init__(self):
        # Stores (user_text, sentiment_data, bot_response)
        self.history = []
        self.context_scores = []

        self.responses = {
            "positive": ["That's great to hear!", "I'm glad you're feeling good.", "Awesome!"],
            "negative": ["I'm sorry to hear that.", "How can I make it better?", "That sounds tough."],
            "neutral": ["I see.", "Tell me more.", "Understood."]
        }

    def generate_response(self, sentiment_label):
        return random.choice(self.responses[sentiment_label.lower()])

    def add_to_history(self, user_text, sentiment_result, bot_response):
        """Maintains full conversation history with bot responses."""
        self.history.append({
            "user": user_text,
            "sentiment": sentiment_result,
            "bot": bot_response
        })
        self.context_scores.append(sentiment_result['score'])

    def get_overall_sentiment(self):
        """Calculates sentiment and returns (Label, Description)."""
        if not self.context_scores:
            return "Neutral", "no data"

        # Rounding for robustness
        avg_score = round(sum(self.context_scores) / len(self.context_scores), 2)

        if avg_score >= 0.05:
            return "Positive", "general satisfaction"
        elif avg_score <= -0.05:
            return "Negative", "general dissatisfaction"
        else:
            return "Neutral", "balanced exchange"