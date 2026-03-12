from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # This serves your Stitch HTML file
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    # This sends the message to EVERYONE connected
    emit('render_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
