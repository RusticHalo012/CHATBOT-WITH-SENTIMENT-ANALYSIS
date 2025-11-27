import streamlit as st
import pandas as pd
from sentiment_engine import SentimentEngine
from chat_manager import ChatBot

# --- Page Config ---
st.set_page_config(page_title="Sentiment Chatbot", page_icon="🤖", layout="wide")

# --- Session State Initialization ---
# Streamlit reruns the script on every interaction.
# We use session_state to keep the Bot memory alive.
if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()
    st.session_state.analyzer = SentimentEngine()
    # We need a UI-specific message history to render the chat bubbles easily
    st.session_state.messages = []
    st.session_state.conversation_ended = False

# --- Sidebar: Real-Time Metrics ---
with st.sidebar:
    st.header("📊 Live Analysis")
    st.markdown("---")

    # Only show metrics if there is data
    if st.session_state.bot.context_scores:
        last_score = st.session_state.bot.context_scores[-1]
        avg_score = sum(st.session_state.bot.context_scores) / len(st.session_state.bot.context_scores)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Last Message", f"{last_score:.2f}")
        with col2:
            st.metric("Avg Score", f"{avg_score:.2f}")

        st.caption("Score Range: -1.0 (Neg) to 1.0 (Pos)")
    else:
        st.info("Start chatting to see metrics.")

    st.markdown("---")
    # Button to end conversation
    if st.button("End Conversation & Analyze", type="primary"):
        st.session_state.conversation_ended = True
        st.rerun()

# --- Main Interface ---
st.title("🤖 AI Sentiment Chatbot")
st.markdown("Your Chat Support")

# 1. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If it's a user message, show the sentiment label below it (Tier 2 Req)
        if message["role"] == "user" and "sentiment" in message:
            score = message["sentiment"]["score"]
            label = message["sentiment"]["label"]
            # Color coding based on label
            color = "green" if label == "Positive" else "red" if label == "Negative" else "gray"
            st.caption(f":{color}[Sentiment: {label} ({score})]")

# 2. Chat Input (Only if conversation hasn't ended)
if not st.session_state.conversation_ended:
    if prompt := st.chat_input("Type your message here..."):
        # A. Process User Input
        # Add user message to UI history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # B. Run Logic (Tier 2)
        sentiment_result = st.session_state.analyzer.get_sentiment(prompt)

        # C. Generate Response
        bot_response = st.session_state.bot.generate_response(sentiment_result['label'])

        # D. Store Data (Tier 1 & UI) - [FIXED HERE]
        # Added 'bot_response' as the 3rd argument required by your class
        st.session_state.bot.add_to_history(prompt, sentiment_result, bot_response)

        # Add sentiment data to the last message in UI history for display
        st.session_state.messages[-1]["sentiment"] = sentiment_result

        # E. Display Bot Response
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Rerun to update sidebar metrics
        st.rerun()

# --- Final Analysis Section (Triggered by Button) ---
else:
    st.divider()
    st.header("📝 Final Conversation Report")

    # Calculate Results
    # [FIXED HERE] Unpacking the tuple (Label, Description) based on your console logic
    overall_label, overall_desc = st.session_state.bot.get_overall_sentiment()

    trend = st.session_state.analyzer.analyze_trend(st.session_state.bot.context_scores)

    # Display Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Overall Sentiment")
        st.subheader(f"{overall_label}")
        st.caption(overall_desc)

    with col2:
        st.info("Emotional Trend")
        st.subheader(trend)

    with col3:
        st.info("Total Messages")
        st.subheader(len(st.session_state.bot.context_scores))

    # Bonus: Visual Chart
    st.write("### Emotional Arc")
    if st.session_state.bot.context_scores:
        chart_data = pd.DataFrame(
            st.session_state.bot.context_scores,
            columns=["Sentiment Score"]
        )
        st.line_chart(chart_data)
    else:
        st.warning("Not enough data to generate chart.")

    if st.button("Start New Conversation"):
        # Clear state
        st.session_state.clear()
        st.rerun()