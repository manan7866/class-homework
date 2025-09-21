from agents import Agent, Runner, function_tool
import requests
from connection import config  

@function_tool
def fetch_products_raw() -> list:
    """
    Fetches all products from known APIs and returns raw data to the agent.
    Agent will decide what to show.
    """
    urls = [
        "https://hackathon-apis.vercel.app/api/products",
        "https://template-03-api.vercel.app/api/products",
        "https://next-ecommerce-template-4.vercel.app/api/product",
        "https://template6-six.vercel.app/api/products"
        "https://dummyjson.com/products",
        "https://dummyjson.com/products/category/smartphones",
        "https://jsonmockapi.com/products"
    ]

    all_products = []
    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            data = res.json()

            # Extract common format
            if isinstance(data, dict) and "products" in data:
                all_products.extend(data["products"])
            elif isinstance(data, list):
                all_products.extend(data)
            elif "data" in data:
                all_products.extend(data["data"])

        except Exception as e:
            continue  # ignore error and continue

    return all_products



shopping_agent = Agent(
    name="Smart Shopping Agent",
    instructions="""
You are a shopping assistant. The user will describe what kind of product they want.

Always use the tool to fetch all available products.

Your job is to:
- Analyze user query for key intent: product type, price range, review quality, color, material, etc.
- From the fetched product list, pick 2–3 best matching items.
- You are allowed to do partial matches. E.g., "wooden chair" can match "wood chair" or similar products.
- If rating is missing in a product, don't discard it unless user strictly wants 'high reviews'.
- Price like 'under $100' means price <= 100.
- Also include similar or related products that might interest the user.
- Output product title, price, rating (if available), and image or brand.
""",
    tools=[fetch_products_raw]
)



# Test run
response = Runner.run_sync(
    shopping_agent,
    input="I want to buy a wireless Bluetooth headphones under $100 with good reviews",
    run_config=config
)

print("\n🔍 Agent Response:\n")
print(response.final_output)
