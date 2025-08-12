# Simple AI Gmail Assistant for Vercel deployment
from flask import Flask, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Simple assistant class without complex imports
class SimpleGmailAssistant:
    def __init__(self):
        self.user_email = "22dcs047@charusat.edu.in"
        # Check if OpenAI is available
        self.openai_available = bool(os.getenv('OPENAI_API_KEY'))
        print(f"🚀 Initializing Gmail Assistant")
        print(f"🧠 OpenAI Available: {self.openai_available}")
    
    def get_demo_emails(self):
        """Demo emails with current timestamps"""
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        
        return [
            {
                'id': 'demo_1',
                'subject': '🔴 URGENT: Kaggle Competition Deadline in 3 Hours!',
                'from_email': 'Kaggle <no-reply@kaggle.com>',
                'priority': 'high',
                'to_field': '22dcs047@charusat.edu.in',
                'cc_field': '',
                'snippet': 'Hi Jai Mehtani, Your submission deadline is approaching fast...',
                'body': 'Hi Jai Mehtani, Your submission for the AI Red-Teaming Challenge is due in 3 hours. Don\'t miss out on the $50,000 prize pool!',
                'date': today,
                'time': (now - timedelta(minutes=30)).strftime('%H:%M'),
                'email_type': 'academic',
                'ai_classified': self.openai_available
            },
            {
                'id': 'demo_2',
                'subject': '🚨 CRITICAL: Security Alert - Immediate Action Required',
                'from_email': 'GitHub Security <noreply@github.com>',
                'priority': 'critical',
                'to_field': '22dcs047@charusat.edu.in',
                'cc_field': '',
                'snippet': 'We detected suspicious activity on your account...',
                'body': 'We detected suspicious login attempts to your GitHub account from multiple locations. Please secure your account immediately.',
                'date': today,
                'time': (now - timedelta(minutes=15)).strftime('%H:%M'),
                'email_type': 'security',
                'ai_classified': self.openai_available
            },
            {
                'id': 'demo_3',
                'subject': 'Assignment Submission Reminder - Due Tomorrow',
                'from_email': 'Professor Smith <prof.smith@charusat.edu.in>',
                'priority': 'high',
                'to_field': 'class2024@charusat.edu.in',
                'cc_field': '22dcs047@charusat.edu.in',
                'snippet': 'Reminder: Final project submission deadline...',
                'body': 'Dear Students, This is a reminder that your final project submission is due tomorrow at 11:59 PM.',
                'date': today,
                'time': (now - timedelta(hours=2)).strftime('%H:%M'),
                'email_type': 'academic',
                'ai_classified': self.openai_available
            }
        ]
    
    def get_email_stats(self):
        """Get email statistics"""
        emails = self.get_demo_emails()
        direct = [e for e in emails if self.user_email in e['to_field']]
        cc = [e for e in emails if self.user_email in e['cc_field']]
        high_priority = [e for e in emails if e['priority'] in ['high', 'critical']]
        
        return {
            'all_emails': emails,
            'direct_emails': direct,
            'cc_emails': cc,
            'stats': {
                'total_unread': len(emails),
                'direct_count': len(direct),
                'cc_count': len(cc),
                'high_priority_count': len(high_priority),
                'ai_classified_count': len([e for e in emails if e.get('ai_classified', False)])
            },
            'last_updated': datetime.now().isoformat(),
            'gmail_connected': False,  # Demo mode for Vercel
            'openai_connected': self.openai_available,
            'data_source': 'Demo Data + AI' if self.openai_available else 'Demo Data',
            'capabilities': {
                'gmail_api': False,
                'ai_classification': self.openai_available,
                'real_draft_creation': False
            }
        }

# Initialize assistant
assistant = SimpleGmailAssistant()

@app.route('/')
def home():
    status = "AI-Powered" if assistant.openai_available else "Standard"
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>{status} Gmail Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: white; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 40px 20px; }}
        .hero {{ background: rgba(255,255,255,0.15); padding: 80px 40px; border-radius: 25px; backdrop-filter: blur(20px); text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
        .hero h1 {{ font-size: 3.5rem; margin-bottom: 20px; font-weight: 700; }}
        .hero p {{ font-size: 1.3rem; margin-bottom: 40px; opacity: 0.9; }}
        .btn {{ background: white; color: #667eea; padding: 18px 35px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; text-decoration: none; display: inline-block; margin: 10px 15px; transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(0,0,0,0.15); }}
        .btn:hover {{ transform: translateY(-3px); box-shadow: 0 12px 35px rgba(0,0,0,0.2); color: #5a67d8; }}
        .live-badge {{ background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; padding: 12px 25px; border-radius: 50px; font-weight: 600; margin-bottom: 20px; display: inline-block; animation: pulse 2s infinite; }}
        .ai-badge {{ background: linear-gradient(45deg, #00b894, #00cec9); color: white; padding: 12px 25px; border-radius: 50px; font-weight: 600; margin-bottom: 30px; display: inline-block; animation: glow 3s infinite; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        @keyframes glow {{ 0% {{ box-shadow: 0 0 10px rgba(0,184,148,0.5); }} 50% {{ box-shadow: 0 0 25px rgba(0,184,148,0.8); }} 100% {{ box-shadow: 0 0 10px rgba(0,184,148,0.5); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="live-badge"><i class="fas fa-satellite-dish"></i> LIVE DEMO SYSTEM <i class="fas fa-satellite-dish"></i></div>
            <div class="ai-badge"><i class="fas fa-brain"></i> {status.upper()} INTELLIGENCE <i class="fas fa-robot"></i></div>
            <h1><i class="fas fa-envelope-open-text"></i> {status} Gmail Assistant</h1>
            <p>Demo of Gmail integration with {'AI-powered' if assistant.openai_available else 'intelligent'} email classification and auto-replies</p>
            <a href="/dashboard" class="btn"><i class="fas fa-rocket"></i> Open Live Dashboard</a>
            <a href="/debug" class="btn" style="background: rgba(255,255,255,0.2); color: white;"><i class="fas fa-code"></i> System Status</a>
        </div>
    </div>
</body>
</html>'''

@app.route('/dashboard')
def dashboard():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>AI Gmail Assistant Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2); }
        .header h1 { font-size: 2.2rem; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 1.1rem; }
        .status-badge { padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; margin: 5px; display: inline-block; }
        .connected { background: rgba(76, 175, 80, 0.9); }
        .demo { background: rgba(255, 152, 0, 0.9); }
        .ai-enabled { background: rgba(0, 184, 148, 0.9); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s ease; position: relative; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); }
        .stat-card h3 { font-size: 2.5rem; color: #2c3e50; margin-bottom: 10px; }
        .stat-card p { color: #7f8c8d; font-size: 1.1rem; font-weight: 500; }
        .action-bar { background: white; padding: 25px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .action-btn { padding: 15px 30px; border: none; border-radius: 50px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-size: 1rem; }
        .action-btn.primary { background: linear-gradient(45deg, #00b894, #00cec9); color: white; }
        .action-btn.secondary { background: #f8f9fa; color: #495057; border: 1px solid #dee2e6; }
        .action-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .email-section { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .email-item { background: #f8f9fb; padding: 20px; margin: 15px 0; border-radius: 15px; border-left: 5px solid #ddd; transition: all 0.3s ease; position: relative; }
        .email-item:hover { transform: translateX(5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        .email-item.priority-critical { border-left-color: #dc3545; }
        .email-item.priority-high { border-left-color: #fd7e14; }
        .priority-badge { padding: 6px 12px; border-radius: 20px; color: white; font-size: 0.85rem; font-weight: 600; }
        .priority-critical .priority-badge { background: #dc3545; }
        .priority-high .priority-badge { background: #fd7e14; }
        .ai-badge { position: absolute; top: 10px; right: 10px; background: linear-gradient(45deg, #00b894, #00cec9); color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-brain"></i> AI-Powered Gmail Assistant</h1>
            <p>Demo of Gmail integration with OpenAI intelligence for smart email management</p>
            <div>
                <div id="connectionStatus" class="status-badge"><i class="fas fa-spinner fa-spin"></i> Loading...</div>
                <div id="aiStatus" class="status-badge"><i class="fas fa-spinner fa-spin"></i> Loading AI...</div>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card"><h3 id="totalEmails">0</h3><p><i class="fas fa-inbox"></i> Total Unread</p></div>
            <div class="stat-card"><h3 id="directEmails">0</h3><p><i class="fas fa-at"></i> Direct Emails</p></div>
            <div class="stat-card"><h3 id="highPriority">0</h3><p><i class="fas fa-exclamation-triangle"></i> High Priority</p></div>
            <div class="stat-card"><h3 id="aiClassified">0</h3><p><i class="fas fa-robot"></i> AI Classified</p></div>
        </div>

        <div class="action-bar">
            <div>
                <button class="action-btn primary" onclick="createAIDrafts()"><i class="fas fa-brain"></i> Demo AI Features</button>
                <button class="action-btn secondary" onclick="refreshEmails()"><i class="fas fa-sync-alt"></i> Refresh Demo</button>
                <button class="action-btn secondary" onclick="window.location.href='/debug'"><i class="fas fa-bug"></i> System Status</button>
            </div>
            <div style="color: #6c757d;"><i class="fas fa-clock"></i> Last updated: <span id="lastUpdated">Never</span></div>
        </div>

        <section class="email-section">
            <h2><i class="fas fa-envelope"></i> Demo Email Management</h2>
            <div id="emailList">Loading emails...</div>
        </section>
    </div>

    <script>
        async function loadEmails() {
            try {
                const response = await fetch('/api/emails');
                const data = await response.json();
                
                document.getElementById('totalEmails').textContent = data.stats.total_unread;
                document.getElementById('directEmails').textContent = data.stats.direct_count;
                document.getElementById('highPriority').textContent = data.stats.high_priority_count;
                document.getElementById('aiClassified').textContent = data.stats.ai_classified_count || 0;
                
                // Update status badges
                const statusEl = document.getElementById('connectionStatus');
                const aiStatusEl = document.getElementById('aiStatus');
                
                statusEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Demo Mode';
                statusEl.className = 'status-badge demo';
                
                if (data.openai_connected) {
                    aiStatusEl.innerHTML = '<i class="fas fa-brain"></i> AI Enabled';
                    aiStatusEl.className = 'status-badge ai-enabled';
                } else {
                    aiStatusEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Basic Mode';
                    aiStatusEl.className = 'status-badge demo';
                }
                
                // Display emails
                const emailList = document.getElementById('emailList');
                let html = '';
                data.direct_emails.forEach(email => {
                    const icon = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🟢'}[email.priority] || '⚪';
                    const aiBadge = email.ai_classified ? '<div class="ai-badge"><i class="fas fa-brain"></i> AI</div>' : '';
                    html += `
                        <div class="email-item priority-${email.priority}">
                            ${aiBadge}
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <h4 style="margin-bottom: 8px;">${email.subject}</h4>
                                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 8px;">${email.from_email}</p>
                                    <p style="margin-bottom: 10px;">${email.snippet}</p>
                                    <small style="color: #888;"><i class="fas fa-clock"></i> ${email.date} ${email.time}</small>
                                </div>
                                <div class="priority-badge">${icon} ${email.priority.toUpperCase()}</div>
                            </div>
                        </div>
                    `;
                });
                emailList.innerHTML = html;
                
                document.getElementById('lastUpdated').textContent = new Date(data.last_updated).toLocaleString();
            } catch (error) {
                console.error('Error loading emails:', error);
                document.getElementById('emailList').innerHTML = '<p>Error loading emails</p>';
            }
        }
        
        async function refreshEmails() {
            document.getElementById('emailList').innerHTML = 'Refreshing demo...';
            await loadEmails();
            showNotification('Demo refreshed!', 'success');
        }
        
        async function createAIDrafts() {
            showNotification('This is a demo - AI features would create intelligent drafts in the real version!', 'info');
        }
        
        function showNotification(message, type) {
            const notification = document.createElement('div');
            const colors = { 'success': '#28a745', 'error': '#dc3545', 'info': '#17a2b8' };
            notification.style.cssText = `position: fixed; top: 20px; right: 20px; padding: 15px 25px; border-radius: 10px; color: white; font-weight: 600; z-index: 1001; background: ${colors[type]};`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 4000);
        }
        
        loadEmails();
        setInterval(loadEmails, 120000);
    </script>
</body>
</html>'''

@app.route('/debug')
def debug():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>System Status</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 4px; overflow: auto; max-height: 500px; }
        .btn { background: #1a73e8; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin: 5px; cursor: pointer; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .connected { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .disconnected { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .ai-enabled { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 System Status</h1>
        <button class="btn" onclick="loadDebug()">Refresh Status</button>
        <button class="btn" onclick="window.location.href='/'">Home</button>
        <button class="btn" onclick="window.location.href='/dashboard'">Dashboard</button>
        
        <div id="statusInfo">Loading...</div>
        
        <h3>📊 System Information</h3>
        <pre id="debugInfo">Loading...</pre>
    </div>
    <script>
        async function loadDebug() {
            try {
                const response = await fetch('/api/debug');
                const data = await response.json();
                
                const statusDiv = document.getElementById('statusInfo');
                let statusHTML = `
                    <div class="status disconnected">
                        <h3>📱 Demo Mode Active</h3>
                        <p>This is a demonstration version showing the interface</p>
                    </div>
                `;
                
                if (data.openai_connected) {
                    statusHTML += `
                        <div class="status ai-enabled">
                            <h3>🧠 OpenAI Integration: READY</h3>
                            <p>AI features would be enabled in the full version</p>
                        </div>
                    `;
                } else {
                    statusHTML += `
                        <div class="status disconnected">
                            <h3>🧠 AI Features: Demo Mode</h3>
                            <p>Add OpenAI API key to enable AI features</p>
                        </div>
                    `;
                }
                
                statusDiv.innerHTML = statusHTML;
                document.getElementById('debugInfo').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('debugInfo').textContent = 'Error: ' + error.message;
            }
        }
        loadDebug();
    </script>
</body>
</html>'''

@app.route('/api/emails')
def api_emails():
    return jsonify(assistant.get_email_stats())

@app.route('/api/debug')
def api_debug():
    return jsonify({
        'gmail_connected': False,
        'openai_connected': assistant.openai_available,
        'data_source': assistant.get_email_stats()['data_source'],
        'capabilities': assistant.get_email_stats()['capabilities'],
        'stats': assistant.get_email_stats()['stats'],
        'environment': {
            'openai_key_exists': bool(os.getenv('OPENAI_API_KEY')),
            'platform': 'vercel'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
