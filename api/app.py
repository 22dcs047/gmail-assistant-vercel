from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data
emails = [
    {'id': '1', 'subject': 'Chess Tournament Invitation', 'from_email': 'Chess.com', 'priority': 'medium', 'to_field': '22dcs047@charusat.edu.in', 'cc_field': '', 'snippet': 'Join our chess tournament...', 'body': 'Hungry for a new chess challenge? Join our latest tournament and test your skills against our advanced chess bots.', 'date': '2025-08-08', 'time': '08:30', 'email_type': 'general'},
    {'id': '2', 'subject': 'Kaggle Competition: AI Red Team Challenge', 'from_email': 'Kaggle', 'priority': 'high', 'to_field': '22dcs047@charusat.edu.in', 'cc_field': '', 'snippet': 'Join the red-teaming challenge...', 'body': 'Hi Jai Mehtani, Join the red-teaming challenge and discover new vulnerabilities in a newly released model. Prize pool of $50,000!', 'date': '2025-08-07', 'time': '19:29', 'email_type': 'academic'},
    {'id': '3', 'subject': 'Assignment Deadline Extended', 'from_email': 'Professor Smith', 'priority': 'high', 'to_field': 'class2024@charusat.edu.in', 'cc_field': '22dcs047@charusat.edu.in', 'snippet': 'Deadline extended to Friday...', 'body': 'Dear Students, The deadline for the final project has been extended to next Friday due to technical issues.', 'date': '2025-08-08', 'time': '14:30', 'email_type': 'academic'},
    {'id': '4', 'subject': 'Security Alert: New Login', 'from_email': 'GitHub', 'priority': 'critical', 'to_field': '22dcs047@charusat.edu.in', 'cc_field': '', 'snippet': 'New sign-in detected...', 'body': 'We noticed a new sign-in to your GitHub account from a Windows device. If this wasn\'t you, secure your account immediately.', 'date': '2025-08-08', 'time': '16:45', 'email_type': 'security'},
    {'id': '5', 'subject': 'Campus Newsletter', 'from_email': 'University', 'priority': 'low', 'to_field': 'all-students@charusat.edu.in', 'cc_field': '22dcs047@charusat.edu.in', 'snippet': 'Weekly campus updates...', 'body': 'This week\'s campus updates include information about upcoming cultural events and research opportunities.', 'date': '2025-08-08', 'time': '09:15', 'email_type': 'newsletter'}
]

def get_stats():
    direct = [e for e in emails if '22dcs047@charusat.edu.in' in e['to_field']]
    cc = [e for e in emails if '22dcs047@charusat.edu.in' in e['cc_field']]
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
            'priority_counts': {'critical': len([e for e in emails if e['priority'] == 'critical']), 'high': len([e for e in emails if e['priority'] == 'high']), 'medium': len([e for e in emails if e['priority'] == 'medium']), 'low': len([e for e in emails if e['priority'] == 'low'])}
        },
        'last_updated': datetime.now().isoformat(),
        'demo_mode': True
    }

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Smart Gmail Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: white; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .hero { background: rgba(255,255,255,0.15); padding: 80px 40px; border-radius: 25px; backdrop-filter: blur(20px); text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .hero h1 { font-size: 3.5rem; margin-bottom: 20px; font-weight: 700; }
        .hero p { font-size: 1.3rem; margin-bottom: 40px; opacity: 0.9; }
        .btn { background: white; color: #667eea; padding: 18px 35px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; text-decoration: none; display: inline-block; margin: 10px 15px; transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 12px 35px rgba(0,0,0,0.2); color: #5a67d8; }
        .demo-badge { background: linear-gradient(45deg, #ffd700, #ffed4e); color: #333; padding: 12px 25px; border-radius: 50px; font-weight: 600; margin-bottom: 30px; display: inline-block; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="demo-badge"><i class="fas fa-star"></i> LIVE DEMO <i class="fas fa-star"></i></div>
            <h1><i class="fas fa-envelope-open-text"></i> Smart Gmail Assistant</h1>
            <p>AI-powered email management dashboard</p>
            <a href="/dashboard" class="btn"><i class="fas fa-rocket"></i> Launch Dashboard</a>
            <a href="/debug" class="btn" style="background: rgba(255,255,255,0.2); color: white;"><i class="fas fa-code"></i> Debug View</a>
        </div>
    </div>
</body>
</html>'''

@app.route('/dashboard')
def dashboard():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Gmail Assistant Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2); }
        .header h1 { font-size: 2.2rem; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 1.1rem; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s ease; position: relative; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); }
        .stat-card h3 { font-size: 2.5rem; color: #2c3e50; margin-bottom: 10px; }
        .stat-card p { color: #7f8c8d; font-size: 1.1rem; font-weight: 500; }
        .action-bar { background: white; padding: 25px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .action-btn { padding: 15px 30px; border: none; border-radius: 50px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-size: 1rem; }
        .action-btn.primary { background: #4CAF50; color: white; }
        .action-btn.secondary { background: #f8f9fa; color: #495057; border: 1px solid #dee2e6; }
        .action-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .email-section { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .tab-container { display: flex; gap: 5px; margin-bottom: 25px; }
        .tab-btn { padding: 15px 25px; border: none; background: #f8f9fa; border-radius: 50px; cursor: pointer; font-weight: 600; transition: all 0.3s ease; }
        .tab-btn.active { background: #667eea; color: white; }
        .email-item { background: #f8f9fb; padding: 20px; margin: 15px 0; border-radius: 15px; border-left: 5px solid #ddd; transition: all 0.3s ease; cursor: pointer; }
        .email-item:hover { transform: translateX(5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        .email-item.priority-critical { border-left-color: #dc3545; }
        .email-item.priority-high { border-left-color: #fd7e14; }
        .email-item.priority-medium { border-left-color: #ffc107; }
        .email-item.priority-low { border-left-color: #28a745; }
        .priority-badge { padding: 6px 12px; border-radius: 20px; color: white; font-size: 0.85rem; font-weight: 600; }
        .priority-critical .priority-badge { background: #dc3545; }
        .priority-high .priority-badge { background: #fd7e14; }
        .priority-medium .priority-badge { background: #ffc107; color: #333; }
        .priority-low .priority-badge { background: #28a745; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .modal-content { background: white; margin: 5% auto; padding: 0; border-radius: 20px; width: 90%; max-width: 800px; box-shadow: 0 25px 50px rgba(0,0,0,0.3); }
        .modal-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; display: flex; justify-content: space-between; align-items: center; }
        .modal-body { padding: 30px; }
        .modal-close { background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-envelope-open-text"></i> Smart Gmail Assistant</h1>
            <p>Intelligent email management for Jai Mehtani (22dcs047@charusat.edu.in)</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card"><h3 id="totalEmails">0</h3><p><i class="fas fa-inbox"></i> Total Unread</p></div>
            <div class="stat-card"><h3 id="directEmails">0</h3><p><i class="fas fa-at"></i> Direct Emails</p></div>
            <div class="stat-card"><h3 id="highPriority">0</h3><p><i class="fas fa-exclamation-triangle"></i> High Priority</p></div>
            <div class="stat-card"><h3 id="ccEmails">0</h3><p><i class="fas fa-share-alt"></i> CC'd Emails</p></div>
        </div>

        <div class="action-bar">
            <div>
                <button class="action-btn primary" onclick="createDrafts()"><i class="fas fa-edit"></i> Create Auto-Reply Drafts</button>
                <button class="action-btn secondary" onclick="exportEmails()"><i class="fas fa-download"></i> Export Summary</button>
                <button class="action-btn secondary" onclick="window.location.href='/debug'"><i class="fas fa-bug"></i> Debug View</button>
            </div>
            <div style="color: #6c757d;"><i class="fas fa-clock"></i> Last updated: <span id="lastUpdated">Never</span></div>
        </div>

        <section class="email-section">
            <h2><i class="fas fa-envelope"></i> Email Management</h2>
            <div class="tab-container">
                <button class="tab-btn active" onclick="showTab('direct')"><i class="fas fa-inbox"></i> Direct Emails (<span id="directCount">0</span>)</button>
                <button class="tab-btn" onclick="showTab('cc')"><i class="fas fa-share-alt"></i> CC'd Emails (<span id="ccCount">0</span>)</button>
            </div>
            <div id="directTab"><p>Loading emails...</p></div>
            <div id="ccTab" style="display: none;"><p>Loading CC'd emails...</p></div>
        </section>
    </div>

    <div id="emailModal" class="modal">
        <div class="modal-content">
            <div class="modal-header"><h3 id="modalTitle">Email Details</h3><button class="modal-close" onclick="closeModal()">×</button></div>
            <div class="modal-body" id="modalBody"></div>
        </div>
    </div>

    <script>
        let emailData = {};
        
        async function loadEmails() {
            try {
                const response = await fetch('/api/emails');
                const data = await response.json();
                emailData = data;
                
                document.getElementById('totalEmails').textContent = data.stats.total_unread;
                document.getElementById('directEmails').textContent = data.stats.direct_count;
                document.getElementById('highPriority').textContent = data.stats.high_priority_count;
                document.getElementById('ccEmails').textContent = data.stats.cc_count;
                document.getElementById('directCount').textContent = data.stats.direct_count;
                document.getElementById('ccCount').textContent = data.stats.cc_count;
                
                updateEmailList('directTab', data.direct_emails);
                updateEmailList('ccTab', data.cc_emails);
                
                document.getElementById('lastUpdated').textContent = new Date(data.last_updated).toLocaleString();
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function updateEmailList(tabId, emails) {
            const tab = document.getElementById(tabId);
            if (emails.length === 0) {
                tab.innerHTML = '<p style="text-align: center; padding: 40px; color: #666;">No emails found</p>';
                return;
            }
            
            let html = '';
            emails.forEach(email => {
                const icon = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🟢'}[email.priority] || '⚪';
                html += `
                    <div class="email-item priority-${email.priority}" onclick="openModal('${email.id}')">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="margin-bottom: 8px;">${email.subject}</h4>
                                <p style="color: #666; font-size: 0.9rem; margin-bottom: 8px;">${email.from_email}</p>
                                <p style="margin-bottom: 10px;">${email.snippet}</p>
                                <small style="color: #888;">${email.date} ${email.time}</small>
                            </div>
                            <div class="priority-badge">${icon} ${email.priority.toUpperCase()}</div>
                        </div>
                    </div>
                `;
            });
            tab.innerHTML = html;
        }
        
        function showTab(tab) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('directTab').style.display = tab === 'direct' ? 'block' : 'none';
            document.getElementById('ccTab').style.display = tab === 'cc' ? 'block' : 'none';
        }
        
        function openModal(emailId) {
            const allEmails = [...emailData.direct_emails, ...emailData.cc_emails];
            const email = allEmails.find(e => e.id === emailId);
            if (!email) return;
            
            document.getElementById('modalTitle').textContent = email.subject;
            document.getElementById('modalBody').innerHTML = `
                <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                    <p><strong>From:</strong> ${email.from_email}</p>
                    <p><strong>To:</strong> ${email.to_field}</p>
                    <p><strong>CC:</strong> ${email.cc_field || 'None'}</p>
                    <p><strong>Date:</strong> ${email.date} ${email.time}</p>
                    <p><strong>Priority:</strong> ${email.priority.toUpperCase()}</p>
                </div>
                <div>
                    <h4>Content:</h4>
                    <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-top: 10px;">
                        ${email.body}
                    </div>
                </div>
            `;
            document.getElementById('emailModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('emailModal').style.display = 'none';
        }
        
        async function createDrafts() {
            try {
                const response = await fetch('/api/create-drafts', { method: 'POST' });
                const result = await response.json();
                alert(`Found ${result.high_priority_emails} high-priority emails. ${result.message}`);
            } catch (error) {
                alert('Error creating drafts');
            }
        }
        
        function exportEmails() {
            const data = JSON.stringify(emailData, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `gmail-export-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
            alert('Email data exported successfully!');
        }
        
        window.onclick = function(event) {
            if (event.target.id === 'emailModal') closeModal();
        }
        
        loadEmails();
        setInterval(loadEmails, 60000);
    </script>
</body>
</html>'''

@app.route('/debug')
def debug():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Debug - Gmail Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 4px; overflow: auto; }
        .btn { background: #1a73e8; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Gmail Assistant Debug</h1>
        <button class="btn" onclick="loadDebug()">Refresh</button>
        <button class="btn" onclick="window.location.href='/'">Home</button>
        <h3>Debug Information</h3>
        <pre id="debugInfo">Loading...</pre>
    </div>
    <script>
        async function loadDebug() {
            try {
                const response = await fetch('/api/debug');
                const data = await response.json();
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
    return jsonify(get_stats())

@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    return jsonify({'status': 'success'})

@app.route('/api/create-drafts', methods=['POST'])
def api_create_drafts():
    data = get_stats()
    high_priority = [e for e in data['direct_emails'] if e['priority'] in ['high', 'critical']]
    return jsonify({
        'status': 'success',
        'high_priority_emails': len(high_priority),
        'message': f'Found {len(high_priority)} high-priority emails (Demo mode)'
    })

@app.route('/api/debug')
def api_debug():
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(debug=True)
