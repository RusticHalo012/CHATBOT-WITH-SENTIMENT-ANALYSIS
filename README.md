🤖 Sentiment Analysis Chatbot

A Python-based conversational agent that performs real-time sentiment analysis on user input. This project features both a Command Line Interface (CLI) and a modern Streamlit Web Interface. It is designed to detect emotional trends and provide a comprehensive summary of the user's mood.

📋 Project Requirements & Features

Tier 1: Conversation-Level Analysis (Mandatory)

✅ Full History Tracking: The bot retains memory of the entire conversation.

✅ Final Report: Generates a summary at the end of the session indicating the overall emotional direction (e.g., "Negative – general dissatisfaction").

Tier 2: Statement-Level Analysis (Additional Credit)

✅ Real-Time Feedback: Every user message is immediately analyzed, and the sentiment (Positive/Negative/Neutral) is displayed alongside the text.

✅ Trend Analysis (Bonus): The system detects shifts in mood (e.g., "Mood Improved 📈" or "Mood Declined 📉") by comparing the first half of the conversation to the second half.

🌟 Innovations & Enhancements

Dual Interface: Includes both a standard CLI (main.py) and a graphical web app (app.py) built with Streamlit.

Robust Testing: Includes a full unit test suite (tests.py) to verify logic stability.

Modular Architecture: Logic is strictly separated from the UI for maintainability.

📂 Project Structure

chatbot_sentiment/
│
├── sentiment_engine.py  # Core Logic: Handles VADER analysis and trend calculation
├── chat_manager.py      # State Management: Stores history and generates bot responses
├── app.py               # Web Interface: Streamlit-based frontend
├── main.py              # CLI Interface: Terminal-based frontend
├── tests.py             # Unit Tests: Verifies accuracy and robustness
├── requirements.txt     # Dependencies list
└── README.md            # Documentation


🚀 Setup & Installation

Clone the Repository

git clone <repository_url>
cd chatbot_sentiment


Install Dependencies
Ensure you have Python installed, then run:

pip install -r requirements.txt


Dependencies include: nltk, streamlit, pandas.

💻 How to Run

Option 1: The Web Interface (Recommended)

This provides the best visual experience with chat bubbles and charts.

streamlit run app.py


Opens automatically in your default web browser.

Click "End Conversation & Generate Report" to see the final transcript and trend chart.

Option 2: The Command Line Interface (CLI)

For a classic terminal experience.

python main.py


Type exit or quit to finish the chat and trigger the final report.

🧪 Running Tests

To verify the system's logic and robustness:

python tests.py


Expected Output: Ran 5 tests in 0.0xxs OK

🧠 Explanation of Logic

1. Sentiment Analysis Engine (sentiment_engine.py)

We utilize NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner).

Why VADER? Unlike standard text analysis, VADER is tuned for social media and conversation. It correctly interprets capitalization ("GREAT!"), emojis ("😃"), and slang.

Scoring: It returns a compound score between -1.0 (Extreme Negative) and 1.0 (Extreme Positive).

Thresholds:

Score >= 0.05 → Positive

Score <= -0.05 → Negative

Otherwise → Neutral

2. Trend Detection Algorithm

To determine if a conversation is "improving" or "worsening," we do not just look at the average.

The conversation scores are split into two chronological halves.

We calculate the mean score of the First Half ($T_1$) vs. the Second Half ($T_2$).

Result:

If $T_2 > T_1$ by a significant margin: Mood Improved 📈

If $T_1 > T_2$: Mood Declined 📉

3. Overall Sentiment Calculation

At the end of the chat, we calculate the average of all sentiment scores.

High Average: "Positive – general satisfaction"

Low Average: "Negative – general dissatisfaction"

Near Zero: "Neutral – balanced exchange"

📸 Example Output Format

User: "Your service disappoints me"

→ Sentiment: Negative

Chatbot: "I’m sorry to hear that."

User: "Last experience was better"

→ Sentiment: Positive

Final Output:

Overall conversation sentiment: Negative – general dissatisfaction
