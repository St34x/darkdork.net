# app.py

from mistralai.models.chat_completion import ChatMessage
from flask import session, copy_current_request_context
from mistralai.client import MistralClient
from flask_socketio import SocketIO, emit
from flask import send_from_directory
from flask_cors import CORS
from app import create_app
import os

app = create_app()
CORS(app, resources={r"/socket.io/*": {"origins": "https://darkdork.net"}})
socketio = SocketIO(app=app, cors_allowed_origins="https://darkdork.net", path='/socket.io')
mistral_api_key = os.environ.get('MISTRAL_API_KEY')

def calculate_token_usage(text):
    return -(-len(text) // 4)  # Round up division

@socketio.on('send_message')
def handle_gpt_request(data):
    @copy_current_request_context
    def handle_request():
        client = MistralClient(api_key=mistral_api_key)
        model = "mistral-medium"
        
        user_input = data['text']
        token_usage = calculate_token_usage(user_input)

        full_response_text = ""

        try:
            messages = [ChatMessage(role="user", content=user_input)]
            session['outgoing_tokens'] += token_usage

            for chunk in client.chat_stream(model=model, messages=messages):
                if chunk.choices[0].delta.content is not None:
                    response_text = chunk.choices[0].delta.content
                    full_response_text += response_text
                    emit('receive_message', {'text': response_text})

            incoming_token_usage = calculate_token_usage(full_response_text)
            session['incoming_tokens'] += incoming_token_usage

            emit('token_usage', {
                'incoming_tokens': session['incoming_tokens'],
                'outgoing_tokens': session['outgoing_tokens'],
            })

        except Exception as e:
            print("Error making request to Mistral API:", str(e))
            emit('error', {'message': str(e)})

    handle_request()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# if __name__ == '__main__':
#     socketio.run(app)
