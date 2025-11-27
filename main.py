from sentiment_engine import SentimentEngine
from chat_manager import ChatBot


def main():
    # Initialize modules
    analyzer = SentimentEngine()
    bot = ChatBot()

    print("--- Sentiment Analysis Chatbot ---")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() in ['exit', 'quit']:
            break

        # 1. Tier 2: Statement-Level Analysis
        sentiment_result = analyzer.get_sentiment(user_input)

        # Display Immediate Sentiment (Tier 2)
        print(f"→ Sentiment: {sentiment_result['label']} (Score: {sentiment_result['score']:.2f})")

        # 2. Generate Bot Response
        bot_response = bot.generate_response(sentiment_result['label'])
        print(f"Chatbot: {bot_response}\n")

        # 3. Store History (Tier 1) - FIXED: Now includes bot_response
        bot.add_to_history(user_input, sentiment_result, bot_response)

    # --- End of Conversation Reporting ---
    print("\n" + "=" * 30)
    print("FINAL CONVERSATION REPORT")
    print("=" * 30)

    # Tier 1: Overall Sentiment
    # FIXED: Now unpacks the tuple (Label, Description)
    overall_label, overall_desc = bot.get_overall_sentiment()

    print(f"Final Output:")
    print(f"Overall conversation sentiment: {overall_label} – {overall_desc}")

    # Tier 2 Bonus: Trend Analysis
    trend = analyzer.analyze_trend(bot.context_scores)
    print(f"Emotional Trend: {trend}")
    print("=" * 30)


if __name__ == "__main__":
    main()