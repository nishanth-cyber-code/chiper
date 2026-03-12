from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from supabase import create_client
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- REPLACE THESE WITH YOUR KEYS FROM SUPABASE SETTINGS ---
SUPABASE_URL = "https://bltcuwllxpkhgkxkrgbp.supabase.co"
SUPABASE_KEY = "sb_publishable_GUBKr-rRvx8K3PLvkQZCiA_gFPDiCdk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # 1. Cleanup: Delete messages older than 48 hours
    threshold = (datetime.utcnow() - timedelta(days=2)).isoformat()
    supabase.table("messages").delete().lt("created_at", threshold).execute()

    # 2. History: Fetch remaining messages to show the user
    response = supabase.table("messages").select("*").order("created_at").execute()
    for msg in response.data:
        emit('render_message', {'text': msg['text'], 'sender': msg['sender']})

@socketio.on('message')
def handle_message(data):
    # data now includes 'text', 'sender', AND 'reply_to'
    supabase.table("messages").insert({
        "text": data['text'], 
        "sender": data['sender'],
        "reply_to": data.get('reply_to') # Add a 'reply_to' column in Supabase if you want to save it!
    }).execute()
    
    emit('render_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)


