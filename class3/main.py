from agents import Agent, Runner, function_tool
import requests
from connection import config

@function_tool
def crypto_query_handler(
    intent: str,
    coin: str = None,
    coin2: str = None,
    amount: float = None,
    vs_currency: str = "usd"
) -> str:
    """
    A smart crypto tool that handles multiple intents:
    - price: gets price of coin
    - convert: converts amount from one coin to another
    - compare: compares two coins
    - info: shows coin details
    """

    try:
        if intent == "price":
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies={vs_currency.lower()}"
            data = requests.get(url).json()
            price = data[coin.lower()][vs_currency.lower()]
            return f"The current price of {coin.upper()} is {price} {vs_currency.upper()}."

        elif intent == "convert":
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()},{coin2.lower()}&vs_currencies=usd"
            data = requests.get(url).json()
            from_price = data[coin.lower()]["usd"]
            to_price = data[coin2.lower()]["usd"]
            converted = (amount * from_price) / to_price
            return f"{amount} {coin.upper()} is approximately {converted:.6f} {coin2.upper()}."

        elif intent == "compare":
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()},{coin2.lower()}&vs_currencies=usd"
            data = requests.get(url).json()
            c1 = data[coin.lower()]["usd"]
            c2 = data[coin2.lower()]["usd"]
            return f"{coin.upper()}: ${c1}\n{coin2.upper()}: ${c2}"

        elif intent == "info":
            url = f"https://api.coingecko.com/api/v3/coins/{coin.lower()}"
            data = requests.get(url).json()
            desc = data['description']['en'].split(".")[0]
            rank = data['market_cap_rank']
            price = data['market_data']['current_price']['usd']
            return f"🪙 {coin.upper()} (Rank {rank}): ${price}\nAbout: {desc}"

        else:
            return "❌ Unknown intent."

    except Exception as e:
        return f"❌ Error: {str(e)}"



shopping_crypto_agent = Agent(
    name="Crypto Agent",
    instructions="""
You are a smart Crypto Assistant.

You must always use the available tool `crypto_query_handler` to fulfill user queries.

You should:
- Understand what the user is asking: price, comparison, conversion, or info.
- Set the `intent` as one of ["price", "convert", "compare", "info"] based on the question.
- Extract coins and other values (like amount or target currency) from the query.
- Call the tool with appropriate parameters.

You are responsible for choosing the right parameters — the tool only executes, not interprets.
    """,
    tools=[crypto_query_handler]
)

# Example run
response = Runner.run_sync(
    shopping_crypto_agent,
    input="What is the price of Bitcoin?",
    run_config=config
)

print(response.final_output)

