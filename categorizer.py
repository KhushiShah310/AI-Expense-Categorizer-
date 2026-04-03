import anthropic #loads the library
import os #lets python talk to our os as it is needed for dotenv
from dotenv import load_dotenv #loads the pythong dotenv library

load_dotenv()

def categorize_transactions(df):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    results = []
    
    for _, row in df.iterrows():
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": f"Categorize this transaction into exactly one of these categories: Food, Rent, Utilities, Subscriptions, Transport, Shopping, Entertainment, Health. Transaction: {row['description']} ${row['amount']}. Reply with ONLY the category name, nothing else."
                }
            ]
        )
        
        category = message.content[0].text.strip()
        results.append(category)
    
    return results