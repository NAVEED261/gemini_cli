from main import get_exchange_rates, convert_currency, parse_input
import streamlit as st
import spacy

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("Downloading spaCy model 'en_core_web_sm' (this may take a few minutes)...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def main_streamlit():
    st.title("AI-Enhanced Currency Converter")

    user_input = st.text_input("Enter your conversion request (e.g., 'convert 100 USD to EUR'):")

    if user_input:
        amount, from_currency, to_currency = parse_input(user_input)

        if amount is None:
            st.warning("Could not detect a valid amount. Please specify an amount (e.g., '100').")
        elif from_currency is None or to_currency is None:
            st.warning("Could not detect both 'from' and 'to' currencies. Please specify them (e.g., 'USD to EUR').")
        else:
            st.info(f"Detected: {amount} {from_currency} to {to_currency}")

            rates = get_exchange_rates(from_currency)

            if rates:
                converted_amount = convert_currency(amount, from_currency, to_currency, rates)
                if converted_amount is not None:
                    st.success(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
            else:
                st.error("Failed to fetch exchange rates. Please check your currency codes or network connection.")

if __name__ == "__main__":
    main_streamlit()
