from flask import Flask, request, jsonify, render_template
import threading
import time
import requests

app = Flask(__name__)

# Global variables to manage the thread
thread = None
stop_thread = False

def call_api_periodically(url, seconds):
    global stop_thread
    try:
        while not stop_thread:
            response = requests.get(url)
            print(f"API Response: {response.status_code} - {response.text}")
            time.sleep(seconds)
    except Exception as e:
        print(f"Error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global thread, stop_thread
    stop_thread = False
    data = request.json
    url = data['url']
    interval = data['interval']
    
    # Start the API request in a new thread
    thread = threading.Thread(target=call_api_periodically, args=(url, interval))
    thread.start()
    return jsonify({"message": "Script started"}), 200

@app.route('/stop', methods=['POST'])
def stop():
    global stop_thread
    stop_thread = True
    return jsonify({"message": "Script stopped"}), 200

if name == "__main__":
    app.run(host='0.0.0.0', port=5000)
