# The Automated System Controller Backend
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import webbrowser
import os

app = Flask(__name__)
CORS(app)

# DYNAMIC DIRECTORY ANCHOR: Lock the processing scope to your project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

@app.route('/')
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: index.html not found in the project folder.", 404

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    print("\n⚡ Web dashboard clicked! Triggering automated pipeline...")
    
    # 1. RUN PACKET GENERATOR
    if os.path.exists("generator.py"):
        print("├── Simulating raw hardware data streams...")
        subprocess.run(["python", "generator.py"], shell=True)
        
    # 2. COMPILE THE C PARSER CODE
    if os.path.exists("parser.c"):
        print("├── Compiling C parser engine binary...")
        subprocess.run(["gcc", "parser.c", "-o", "parser"], shell=True)
        
    # 3. EXECUTE THE C PARSER BINARY RUN
    print("├── Executing C binary to parse 16-bit register bits...")
    if os.name == 'nt':
        subprocess.run(["parser"], shell=True)
    else:
        subprocess.run(["./parser"], shell=True)
        
    packets_list = []
    
    # 4. INGEST EXTRACTED VALUES LOG
    try:
        with open("parsed_data.txt", "r") as file:
            for line in file:
                if line.strip():
                    device_id, priority, payload = line.strip().split(',')
                    packets_list.append({
                        "device_id": int(device_id),
                        "priority": int(priority),
                        "payload": int(payload)
                    })
        print("└── Telemetry packet sync successful! Piping JSON data to UI.\n")
    except FileNotFoundError:
        return jsonify({"error": "Telemetry pipeline log file not found."}), 500

    return jsonify(packets_list)

if __name__ == '__main__':
    print("\n🚀 TELEMETRY ARCHITECTURE ONLINE!")
    print("Automatically launching dashboard interface at http://127.0.0.1:5000 ...")
    webbrowser.open("http://127.0.0.1:5000")
    
    # Boot the pipeline server container engine safely
    app.run(port=5000, host='127.0.0.1', debug=False)
