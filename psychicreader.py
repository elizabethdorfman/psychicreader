import os
import openai
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# Get the current date and time
today = datetime.now()

# Extract the day, month, and year
day = today.day
month = today.month
year = today.year

# Format the date as DD/MM/YYYY
formatted_date = f"{day}/{month}/{year}"

app = Flask(__name__)

CORS(app)

# Set your OpenAI API key
# Set your OpenAI API key
api_key = os.environ.get(api_key, api_key)

# Create an OpenAI client using the API key
client = OpenAI(api_key=api_key)

# Route to render index.html
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gpt_response', methods=['GET'])
def gpt_response():
    input_text = f"Hi please generate an example of a great psychic reading. Today is {formatted_date} (format day/month/year). only return the reading itself. Each time return a new example."

    try:
        response = client.chat.completions.create(
    			messages=[
        		{
            	"role": "user",
            	"content": input_text,  # Pass the user input to GPT
        		}
    			],
   		 		model="gpt-3.5-turbo",
				)
        gpt_text = response.choices[0].message.content

        # Return the GPT response
        return gpt_text

    except openai.RateLimitError as e:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    except openai.BadRequestError as e:
        return jsonify({"error": "Invalid request to OpenAI."}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Run the server on port 8080