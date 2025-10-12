from flask import Flask, request, render_template
import asyncio
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/join', methods=['POST'])
async def join_meeting():
    meetingcode = request.form['meeting_id']
    passcode = request.form['password']
    num_users = int(request.form['members'])
    timeout = int(request.form['timeout'])
    
    # Main.py के run_meeting को कॉल करें
    await asyncio.run(run_meeting(meetingcode, passcode, num_users, timeout))
    return "मीटिंग शुरू हो गई! लॉग्स चेक करें।"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))