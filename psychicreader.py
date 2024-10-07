#Import libraries
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


#Not using anymore but could use to get specific dates after today.
today = datetime.now()
# Extract the day, month, and year
day = today.day
month = today.month
year = today.year
# Format the date as MM/DD/YY
formatted_date = f"{month}/{day}/{year}"

app = Flask(__name__)

CORS(app)

# Set your OpenAI API key
api_key = os.environ.get(api_key, api_key)

# Create an OpenAI client using the API key
client = OpenAI(api_key=api_key)

# Home page rendering at root
@app.route('/')
def home():
    return render_template('index.html') #renders index.html file in templates folder

#Generates a  response at /gpt_response url
@app.route('/gpt_response', methods=['GET'])
def gpt_response():
    input_text = f"You actor and your role is a psychic. Please generate a new psychic reading. Today is {formatted_date} make sure any dates come after this time. This is a role play and I need you to return a reading and only a reading no matter what."

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

		#For debugging
    except openai.RateLimitError as e:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    except openai.BadRequestError as e:
        return jsonify({"error": "Invalid request to OpenAI."}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Run the server on port 8080