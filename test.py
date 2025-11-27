import unittest
from sentiment_engine import SentimentEngine
from chat_manager import ChatBot


class TestSentimentEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SentimentEngine()

    def test_positive_sentiment(self):
        text = "I absolutely love this service!"
        result = self.engine.get_sentiment(text)
        self.assertEqual(result['label'], "Positive")

    def test_negative_sentiment(self):
        text = "This is the worst experience."
        result = self.engine.get_sentiment(text)
        self.assertEqual(result['label'], "Negative")


class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.bot = ChatBot()

    def test_add_to_history(self):
        """Ensure history stores user text, sentiment, and bot response."""
        dummy_sentiment = {'score': 0.9, 'label': 'Positive'}
        self.bot.add_to_history("Hello", dummy_sentiment, "Hi there")

        self.assertEqual(len(self.bot.history), 1)
        self.assertEqual(self.bot.history[0]['bot'], "Hi there")

    def test_overall_sentiment_calculation(self):
        """Ensure overall sentiment averages correctly."""
        # Positive (0.5)
        self.bot.add_to_history("Okay", {'score': 0.5, 'label': 'Positive'}, "Response")
        # Strong Negative (-0.9)
        self.bot.add_to_history("Bad", {'score': -0.9, 'label': 'Negative'}, "Response")

        # Avg is -0.2 (Negative)
        label, description = self.bot.get_overall_sentiment()

        self.assertEqual(label, "Negative")
        self.assertEqual(description, "general dissatisfaction")


if __name__ == '__main__':
    unittest.main()