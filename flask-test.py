from flask import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gpt_response', methods=['GET'])
def greet():
    # Gets gpt question
    user_input = request.args.get('gpt_question')

    # Return chatbot response
    response = "You are talking to a chatbot"

		# Render a template to display the response
    return response



if __name__ == '__main__':
    app.run(debug=True, port=8080)