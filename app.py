from flask import Flask, request, render_template, jsonify
import asyncio
import os
import sys

# FunHindi folder ko import path me daalna
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'FunHindi'))

from HindiFun import start as funhindi_start

app = Flask(__name__, template_folder='templates')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/join', methods=['POST'])
async def join_meeting():
    try:
        meetingcode = request.form['meeting_id']
        passcode = request.form['password']
        num_users = int(request.form['members'])
        timeout = int(request.form['timeout'])

        asyncio.create_task(run_funhindi(meetingcode, passcode, num_users, timeout))
        return jsonify({"status": "Started", "meeting": meetingcode})
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)})

async def run_funhindi(meetingcode, passcode, num_users, timeout):
    print(f"🚀 Starting FunHindi automation for meeting {meetingcode}")
    wait_time = timeout
    tasks = []
    for i in range(num_users):
        user = f"User{i}"
        task = asyncio.create_task(funhindi_start(user, wait_time, meetingcode, passcode))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print("✅ All bots finished")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
