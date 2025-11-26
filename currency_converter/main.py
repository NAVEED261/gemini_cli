import requests
import spacy

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm' (this may take a few minutes)...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/"

def get_exchange_rates(base_currency):
    """
    Fetches the latest exchange rates for a given base currency.
    """
    try:
        response = requests.get(f"{EXCHANGE_RATE_API_URL}{base_currency}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data["result"] == "success":
            return data["rates"]
        else:
            print(f"Error fetching rates: {data.get('error-type', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error or invalid currency: {e}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    """
    Converts an amount from one currency to another using provided rates.
    """
    if not rates:
        return None

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in rates:
        print(f"Error: Base currency '{from_currency}' not found in rates.")
        return None
    if to_currency not in rates:
        print(f"Error: Target currency '{to_currency}' not found in rates.")
        return None

    # The 'rates' dictionary is already based on 'from_currency'
    amount_in_base = amount

    # If the target currency is the same as the base currency for the rates, no conversion needed (beyond the 1-to-1 rate)
    if from_currency == to_currency:
        return amount

    converted_amount = amount_in_base * rates[to_currency]
    return converted_amount

def parse_input(text):
    """
    Parses natural language input to extract amount, from_currency, and to_currency.
    Uses spaCy for named entity recognition.
    """
    doc = nlp(text)
    amount = None
    from_currency = None
    to_currency = None

    # Extract numerical amount
    for token in doc:
        if token.like_num:
            try:
                amount = float(token.text)
            except ValueError:
                pass # Ignore if not a valid number

    # Extract currencies using custom logic or entity recognition if trained
    # For now, we'll look for common currency codes
    currency_codes = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "GPE"] # Placeholder, needs refinement

    # A more robust way would be to have a list of known currency codes
    # and match against them. Let's keep it simple for now and expect explicit codes.
    tokens = [token.text.upper() for token in doc]

    # Simple heuristic for currency extraction (e.g., "USD", "EUR")
    potential_currencies = []
    for token in tokens:
        if len(token) == 3 and token.isalpha(): # Assume 3-letter alphabetic codes
            potential_currencies.append(token)

    # Heuristic: last two 3-letter codes are likely from and to
    if len(potential_currencies) >= 2:
        to_currency = potential_currencies[-1]
        from_currency = potential_currencies[-2]
    elif len(potential_currencies) == 1:
        # If only one, assume it's target and base is implicit or common
        to_currency = potential_currencies[0]

    return amount, from_currency, to_currency

def main():
    print("Welcome to the AI-Enhanced Currency Converter!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("Enter your conversion request (e.g., 'convert 100 USD to EUR'): ").strip()
        if user_input.lower() == 'exit':
            break


        amount, from_currency, to_currency = parse_input(user_input)

        if amount is None:
            print("Could not detect a valid amount. Please specify an amount (e.g., '100').")
            continue
        if from_currency is None or to_currency is None:
            print("Could not detect both 'from' and 'to' currencies. Please specify them (e.g., 'USD to EUR').")
            continue

        print(f"Detected: {amount} {from_currency} to {to_currency}")

        # Fetch rates using the from_currency as base
        rates = get_exchange_rates(from_currency)

        if rates:
            converted_amount = convert_currency(amount, from_currency, to_currency, rates)
            if converted_amount is not None:
                print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        else:
            print("Failed to fetch exchange rates. Please check your currency codes or network connection.")

if __name__ == "__main__":
    main()
