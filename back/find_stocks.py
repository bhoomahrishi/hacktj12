from dotenv import load_dotenv
import os
import openai
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Function to fetch stock list based on the prompt
def stock_list(prompt):
    # Ensure the API key is loaded from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_key = api_key

    client = OpenAI()

    # Create a completion request to GPT-4
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Generate a space-separated string of 9 stock symbols based on the following prompt: " + prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Return the text of the response
    return response.choices[0].message.content.split()[:9]

def risk_measure(prompt):
    # Ensure the API key is loaded from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_key = api_key

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": "Generate an integer from 1 to 10 representing the riskiness of the user."
            },
            {
            "role": "user",
            "content": prompt
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return int(response.choices[0].message.content)

if __name__ == '__main__':
    interest_prompt = "i love music and food as well as watching sports and taking care of the environment"
    goals_prompt = "i want a diverse portfolio of a variety of relatively stable stocks so that I can make safe long-term investments"
    print(stock_list(interest_prompt))
    print(risk_measure(goals_prompt))