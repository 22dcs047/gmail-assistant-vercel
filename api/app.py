import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import threading
import time

# For production deployment
from flask import Flask, render_template, jsonify, request

# Simplified EmailData class for deployment
@dataclass
class EmailData:
    id: str
    from_email: str
    subject: str
    body: str
    snippet: str
    date: str
    time: str
    to_field: str
    cc_field: str
    priority: str
    email_type: str

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global variables to store email data
current_email_data = {
    'all_emails': [],
    'direct_emails': [],
    'cc_emails': [],
    'stats': {},
    'last_updated': None,
    'is_processing': False,
    'error_message': None,
    'demo_mode': True  # Always demo mode in production
}

class WebGmailAssistant:
    def __init__(self):
        self.gmail_service = None
        self.user_email = "22dcs047@charusat.edu.in"
        self.processing = False

    def process_emails_for_web(self):
        """Process emails and return data for web dashboard"""
        global current_email_data
        
        current_email_data['is_processing'] = True
        current_email_data['error_message'] = None
        
        try:
            # Always use sample data for demo
            all_emails = self.get_sample_emails()
            
            # Enhanced email categorization
            direct_emails = []
            cc_emails = []
            
            for email in all_emails:
                user_email = self.user_email.lower()
                to_field_lower = (email.to_field or "").lower()
                cc_field_lower = (email.cc_field or "").lower()
                
                # Check if user email is in To field (direct email)
                is_direct = (user_email in to_field_lower or 
                           "22dcs047@charusat.edu.in" in to_field_lower)
                
                # Check if user email is in CC field
                is_cc = (user_email in cc_field_lower or 
                        "22dcs047@charusat.edu.in" in cc_field_lower)
                
                if is_direct:
                    direct_emails.append(email)
                elif is_cc:
                    cc_emails.append(email)
                else:
                    # If neither direct nor CC, treat as direct (fallback)
                    direct_emails.append(email)
            
            # Calculate statistics
            priority_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            type_counts = {}
            
            for email in all_emails:
                priority_counts[email.priority] = priority_counts.get(email.priority, 0) + 1
                type_counts[email.email_type] = type_counts.get(email.email_type, 0) + 1
            
            # Convert EmailData objects to dictionaries for JSON serialization
            def email_to_dict(email):
                return {
                    'id': email.id,
                    'from_email': email.from_email,
                    'subject': email.subject,
                    'body': email.body,
                    'snippet': email.snippet,
                    'date': email.date,
                    'time': email.time,
                    'to_field': email.to_field,
                    'cc_field': email.cc_field,
                    'priority': email.priority,
                    'email_type': email.email_type
                }
            
            current_email_data.update({
                'all_emails': [email_to_dict(email) for email in all_emails],
                'direct_emails': [email_to_dict(email) for email in direct_emails],
                'cc_emails': [email_to_dict(email) for email in cc_emails],
                'stats': {
                    'total_unread': len(all_emails),
                    'direct_count': len(direct_emails),
                    'cc_count': len(cc_emails),
                    'priority_counts': priority_counts,
                    'type_counts': type_counts,
                    'high_priority_count': priority_counts['critical'] + priority_counts['high']
                },
                'last_updated': datetime.now().isoformat(),
                'is_processing': False,
                'error_message': None,
                'demo_mode': True
            })
            
        except Exception as e:
            current_email_data.update({
                'is_processing': False,
                'error_message': str(e)
            })
        
        return current_email_data

    def get_sample_emails(self):
        """Generate sample email data for demo/development"""
        sample_emails = [
            EmailData(
                id="1",
                from_email='"Chess.com" <hello@chess.com>',
                subject="It's a Chess Bot BBQ—Grab a Fork & Skewer!",
                body="Hungry for a new chess challenge?",
                snippet="Hungry for a new chess challenge? Join our latest tournament and test your skills against our advanced chess bots.",
                date="2025-08-08",
                time="08:30",
                to_field="22dcs047@charusat.edu.in",
                cc_field="",
                priority="medium",
                email_type="general"
            ),
            EmailData(
                id="2",
                from_email="Medium Daily Digest <noreply@medium.com>",
                subject="10 Python Libraries So Reliable, I Stopped Debugging My Scripts",
                body="JAI MEHTANI Stories for JAI MEHTANI",
                snippet="JAI MEHTANI Stories for JAI MEHTANI - Today's highlights in tech and programming.",
                date="2025-08-08",
                time="07:00",
                to_field="22dcs047@charusat.edu.in",
                cc_field="",
                priority="medium",
                email_type="general"
            ),
            EmailData(
                id="3",
                from_email="Kaggle <no-reply@kaggle.com>",
                subject="Competition Launch: Open Model Red-Teaming Challenge",
                body="Hi Jai Mehtani, Join the red-teaming challenge",
                snippet="Hi Jai Mehtani, Join the red-teaming challenge and discover new vulnerabilities in a newly released model.",
                date="2025-08-07",
                time="19:29",
                to_field="22dcs047@charusat.edu.in",
                cc_field="",
                priority="high",
                email_type="academic"
            ),
            EmailData(
                id="4",
                from_email="Professor Smith <prof.smith@charusat.edu.in>",
                subject="Important: Assignment Deadline Extended",
                body="The deadline has been extended",
                snippet="The deadline for the final project has been extended to next Friday due to technical issues.",
                date="2025-08-08",
                time="14:30",
                to_field="class2024@charusat.edu.in",
                cc_field="22dcs047@charusat.edu.in, other.student@charusat.edu.in",
                priority="high",
                email_type="academic"
            )
        ]
        
        return sample_emails

# Initialize the web assistant
web_assistant = WebGmailAssistant()

@app.route('/')
def welcome():
    """Welcome page for new users"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Gmail Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 40px; color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .hero { background: rgba(255,255,255,0.1); padding: 60px 40px; border-radius: 20px; backdrop-filter: blur(10px); }
            .btn { background: white; color: #667eea; padding: 15px 30px; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 600; text-decoration: none; display: inline-block; margin: 10px; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>📧 Smart Gmail Assistant</h1>
                <p>Transform your email chaos into organized productivity</p>
                <a href="/dashboard" class="btn">🚀 Try Dashboard</a>
                <a href="/debug" class="btn">🔍 Debug View</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gmail Assistant Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f5f7fa; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 30px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center; }
            .email-section { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .email-item { background: #f8f9fb; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ddd; }
            .priority-high { border-left-color: #e74c3c; }
            .priority-critical { border-left-color: #c0392b; }
            .priority-medium { border-left-color: #f39c12; }
            .priority-low { border-left-color: #27ae60; }
            .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; margin: 10px 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>📧 Smart Gmail Assistant Dashboard</h1>
                <p>Intelligent email management for Jai Mehtani (22dcs047@charusat.edu.in)</p>
                <button class="btn" onclick="loadEmails()">🔄 Refresh</button>
            </header>

            <div class="stats-grid">
                <div class="stat-card">
                    <h3 id="totalEmails">Loading...</h3>
                    <p>Total Unread</p>
                </div>
                <div class="stat-card">
                    <h3 id="directEmails">Loading...</h3>
                    <p>Direct Emails</p>
                </div>
                <div class="stat-card">
                    <h3 id="highPriority">Loading...</h3>
                    <p>High Priority</p>
                </div>
                <div class="stat-card">
                    <h3 id="ccEmails">Loading...</h3>
                    <p>CC'd Emails</p>
                </div>
            </div>

            <section class="email-section">
                <h2>📧 Recent Emails</h2>
                <div id="emailList">Loading emails...</div>
            </section>
        </div>

        <script>
            async function loadEmails() {
                try {
                    const response = await fetch('/api/emails');
                    const data = await response.json();
                    
                    document.getElementById('totalEmails').textContent = data.stats.total_unread || 0;
                    document.getElementById('directEmails').textContent = data.stats.direct_count || 0;
                    document.getElementById('highPriority').textContent = data.stats.high_priority_count || 0;
                    document.getElementById('ccEmails').textContent = data.stats.cc_count || 0;
                    
                    const emailList = document.getElementById('emailList');
                    let html = '';
                    
                    if (data.direct_emails && data.direct_emails.length > 0) {
                        data.direct_emails.forEach(email => {
                            html += `
                                <div class="email-item priority-${email.priority}">
                                    <h4>${email.subject}</h4>
                                    <p style="color: #666;">${email.from_email}</p>
                                    <p>${email.snippet}</p>
                                    <small>${email.date} ${email.time} - Priority: ${email.priority.toUpperCase()}</small>
                                </div>
                            `;
                        });
                    } else {
                        html = '<p>No emails found</p>';
                    }
                    
                    emailList.innerHTML = html;
                } catch (error) {
                    document.getElementById('emailList').innerHTML = '<p style="color: red;">Error loading emails: ' + error.message + '</p>';
                }
            }
            
            loadEmails();
        </script>
    </body>
    </html>
    """

@app.route('/debug')
def debug_page():
    """Debug page to see raw email data"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug - Gmail Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            pre { background: #f5f5f5; padding: 15px; border-radius: 4px; overflow: auto; }
            .btn { background: #1a73e8; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Gmail Assistant Debug</h1>
            <button class="btn" onclick="loadDebugInfo()">Refresh Debug Info</button>
            <button class="btn" onclick="window.location.href='/'">Back to Home</button>
            
            <h3>📊 Debug Information</h3>
            <pre id="debugInfo">Loading...</pre>
        </div>

        <script>
            async function loadDebugInfo() {
                try {
                    const response = await fetch('/api/debug');
                    const data = await response.json();
                    document.getElementById('debugInfo').textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    document.getElementById('debugInfo').textContent = 'Error: ' + error.message;
                }
            }
            
            loadDebugInfo();
        </script>
    </body>
    </html>
    """

@app.route('/api/emails')
def get_emails():
    """API endpoint to get current email data"""
    return jsonify(current_email_data)

@app.route('/api/refresh', methods=['POST'])
def refresh_emails():
    """API endpoint to refresh email data"""
    web_assistant.process_emails_for_web()
    return jsonify({'status': 'success'})

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to see raw email data"""
    debug_data = {
        'total_emails': len(current_email_data.get('all_emails', [])),
        'direct_emails': len(current_email_data.get('direct_emails', [])),
        'cc_emails': len(current_email_data.get('cc_emails', [])),
        'stats': current_email_data.get('stats', {}),
        'last_updated': current_email_data.get('last_updated'),
        'demo_mode': current_email_data.get('demo_mode', True),
        'sample_emails': current_email_data.get('all_emails', [])[:3]  # First 3 emails
    }
    return jsonify(debug_data)

# Initialize data on startup
web_assistant.process_emails_for_web()

if __name__ == '__main__':
    app.run(debug=True)
