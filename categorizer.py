import anthropic #loads the library
import os #lets python talk to our os as it is needed for dotenv
from dotenv import load_dotenv #loads the python dotenv library
import base64 #This is for the convert image to base64 and extract the correct information

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


def extract_from_receipt(image_bytes):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Look at this receipt. Extract the store name, total amount, and date. Reply in this exact format only: Store: X, Amount: X, Date: X"
                    }
                ],
            }
        ],
    )
    
    return message.content[0].text.strip()