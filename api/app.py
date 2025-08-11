from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample data with TODAY'S dates
def get_current_emails():
    """Get emails with current dates for last 24 hours"""
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    
    # Create emails with times from last 24 hours
    emails = [
        {
            'id': '1', 
            'subject': 'Chess Tournament Invitation - Join Today!', 
            'from_email': 'Chess.com <hello@chess.com>', 
            'priority': 'medium', 
            'to_field': '22dcs047@charusat.edu.in', 
            'cc_field': '', 
            'snippet': 'Hungry for a new chess challenge? Join our latest tournament...', 
            'body': 'Hungry for a new chess challenge? Join our latest tournament and test your skills against our advanced chess bots. This event features multiple difficulty levels and exciting prizes for winners.', 
            'date': today, 
            'time': (now - timedelta(hours=2)).strftime('%H:%M'), 
            'email_type': 'general'
        },
        {
            'id': '2', 
            'subject': 'URGENT: Kaggle Competition Deadline in 6 Hours!', 
            'from_email': 'Kaggle <no-reply@kaggle.com>', 
            'priority': 'high', 
            'to_field': '22dcs047@charusat.edu.in', 
            'cc_field': '', 
            'snippet': 'Hi Jai Mehtani, Your submission deadline is approaching fast...', 
            'body': 'Hi Jai Mehtani, Your submission for the AI Red-Teaming Challenge is due in 6 hours. Don\'t miss out on the $50,000 prize pool! Submit your solution now.', 
            'date': today, 
            'time': (now - timedelta(hours=1)).strftime('%H:%M'), 
            'email_type': 'academic'
        },
        {
            'id': '3', 
            'subject': 'URGENT: Assignment Submission Due Tomorrow', 
            'from_email': 'Professor Smith <prof.smith@charusat.edu.in>', 
            'priority': 'high', 
            'to_field': 'class2024@charusat.edu.in', 
            'cc_field': '22dcs047@charusat.edu.in', 
            'snippet': 'Reminder: Final project submission deadline is tomorrow...', 
            'body': 'Dear Students, This is a reminder that your final project submission is due tomorrow at 11:59 PM. Please ensure all requirements are met and submit through the portal.', 
            'date': today, 
            'time': (now - timedelta(minutes=45)).strftime('%H:%M'), 
            'email_type': 'academic'
        },
        {
            'id': '4', 
            'subject': 'CRITICAL: Suspicious Login Attempt Detected', 
            'from_email': 'GitHub Security <noreply@github.com>', 
            'priority': 'critical', 
            'to_field': '22dcs047@charusat.edu.in', 
            'cc_field': '', 
            'snippet': 'We detected a suspicious login attempt to your account...', 
            'body': 'We detected a suspicious login attempt to your GitHub account from an unrecognized device in a different location. Please secure your account immediately by changing your password.', 
            'date': today, 
            'time': (now - timedelta(minutes=15)).strftime('%H:%M'), 
            'email_type': 'security'
        },
        {
            'id': '5', 
            'subject': 'Weekly Campus Updates - New Events This Week', 
            'from_email': 'University Newsletter <newsletter@charusat.edu.in>', 
            'priority': 'low', 
            'to_field': 'all-students@charusat.edu.in', 
            'cc_field': '22dcs047@charusat.edu.in', 
            'snippet': 'This week\'s campus updates include exciting new events...', 
            'body': 'This week\'s campus updates include exciting new cultural events, library schedule changes, and amazing research opportunities. Check out the career fair next week!', 
            'date': (now - timedelta(hours=3)).strftime('%Y-%m-%d'), 
            'time': (now - timedelta(hours=3)).strftime('%H:%M'), 
            'email_type': 'newsletter'
        }
    ]
    return emails

def get_stats():
    emails = get_current_emails()  # Get fresh emails with current dates
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
        'demo_mode': True,
        'data_source': 'Live demo with current timestamps'
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
                // Show loading state
                const button = event.target;
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Drafts...';
                button.disabled = true;
                
                const response = await fetch('/api/create-drafts', { method: 'POST' });
                const result = await response.json();
                
                if (result.status === 'success') {
                    if (result.drafts_created && result.drafts_created.length > 0) {
                        // Show detailed results in a modal
                        showDraftResults(result.drafts_created, result.high_priority_emails);
                    } else {
                        alert(`${result.message}`);
                    }
                } else {
                    alert('Error: ' + result.message);
                }
                
                // Reset button
                button.innerHTML = originalText;
                button.disabled = false;
                
            } catch (error) {
                alert('Error creating drafts: ' + error.message);
                // Reset button
                const button = event.target;
                button.innerHTML = '<i class="fas fa-edit"></i> Create Auto-Reply Drafts';
                button.disabled = false;
            }
        }
        
        function showDraftResults(drafts, totalHighPriority) {
            const modal = document.getElementById('emailModal');
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Auto-Reply Drafts Created!';
            
            let html = `
                <div style="margin-bottom: 25px; padding: 20px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; color: #155724;">
                    <h4 style="margin: 0 0 10px 0;"><i class="fas fa-check-circle"></i> Success!</h4>
                    <p style="margin: 0;">Created <strong>${drafts.length}</strong> auto-reply drafts for high-priority emails.</p>
                </div>
                
                <h4 style="color: #2c3e50; margin-bottom: 15px;">Generated Draft Replies:</h4>
            `;
            
            drafts.forEach((draft, index) => {
                const priorityColor = {
                    'critical': '#dc3545',
                    'high': '#fd7e14',
                    'medium': '#ffc107',
                    'low': '#28a745'
                }[draft.priority] || '#6c757d';
                
                html += `
                    <div style="margin-bottom: 20px; border: 1px solid #dee2e6; border-radius: 10px; overflow: hidden;">
                        <div style="background: ${priorityColor}; color: white; padding: 10px; font-weight: 600;">
                            <i class="fas fa-reply"></i> Draft ${index + 1}: ${draft.priority.toUpperCase()} Priority
                        </div>
                        <div style="padding: 15px; background: #f8f9fa;">
                            <p><strong>To:</strong> ${draft.to}</p>
                            <p><strong>Subject:</strong> ${draft.subject}</p>
                            <p><strong>Response Time:</strong> ${draft.response_timeframe}</p>
                            <p><strong>Original Email:</strong> ${draft.original_subject}</p>
                        </div>
                        <div style="padding: 15px; background: white; max-height: 200px; overflow-y: auto;">
                            <strong>Draft Content:</strong>
                            <div style="margin-top: 10px; border: 1px solid #ddd; padding: 10px; border-radius: 5px; font-size: 0.9rem;">
                                ${draft.body}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += `
                <div style="margin-top: 25px; padding: 15px; background: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3;">
                    <h5 style="color: #1976d2; margin-bottom: 8px;"><i class="fas fa-info-circle"></i> Next Steps</h5>
                    <p style="color: #1565c0; margin: 0;">
                        <strong>📝 Note:</strong> These are draft templates showing how auto-replies would be generated. 
                        In a production environment, these would be automatically saved as drafts in your Gmail account.
                    </p>
                </div>
            `;
            
            document.getElementById('modalBody').innerHTML = html;
            modal.style.display = 'block';
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
    try:
        data = get_stats()
        high_priority_emails = [e for e in data['direct_emails'] if e['priority'] in ['high', 'critical']]
        
        if not high_priority_emails:
            return jsonify({
                'status': 'success',
                'high_priority_emails': 0,
                'drafts_created': [],
                'message': 'No high-priority emails found to create drafts for.'
            })
        
        # Generate actual draft replies
        drafts_created = []
        
        for email in high_priority_emails:
            draft_reply = generate_auto_reply_draft(email)
            drafts_created.append(draft_reply)
        
        return jsonify({
            'status': 'success',
            'high_priority_emails': len(high_priority_emails),
            'drafts_created': drafts_created,
            'message': f'Successfully created {len(drafts_created)} auto-reply drafts for high-priority emails!'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error creating drafts: {str(e)}'
        })

def generate_auto_reply_draft(email):
    """Generate professional auto-reply draft"""
    
    # Extract clean email address
    from_email = email['from_email']
    if '<' in from_email:
        import re
        match = re.search(r'<([^>]+)>', from_email)
        from_email = match.group(1) if match else from_email
    
    # Determine response timeframe based on email type
    timeframes = {
        'academic': '2-4 hours',
        'security': '1-2 hours', 
        'general': '24-48 hours',
        'newsletter': '48-72 hours'
    }
    
    response_timeframe = timeframes.get(email['email_type'], '24-48 hours')
    
    # Create smart subject line
    clean_subject = email['subject'].replace('Re: ', '').replace('Fwd: ', '')
    smart_subject = f"Re: {clean_subject} - Acknowledged"
    
    # Generate personalized body content
    body_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px;">
        <p>Dear Sender,</p>
        
        <p>Thank you for your email regarding <strong>"{email['subject']}"</strong>. I have received your message and will review it carefully.</p>
        
        <p>I will get back to you within <strong>{response_timeframe}</strong>.</p>
    """
    
    # Add priority-specific content
    if email['priority'] == 'critical':
        body_content += """
        <p style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px;">
            <strong>⚠️ Note:</strong> I understand this is critical priority and will respond as soon as possible.
        </p>
        """
    elif email['priority'] == 'high':
        body_content += """
        <p style="background: #e7f3ff; border: 1px solid #74b9ff; padding: 10px; border-radius: 5px;">
            <strong>🔴 Note:</strong> I understand this is high priority and will respond promptly.
        </p>
        """
    
    # Add email type specific content
    if email['email_type'] == 'academic':
        body_content += """
        <p>As this appears to be academic-related, I will prioritize reviewing any assignment details or requirements mentioned.</p>
        """
    elif email['email_type'] == 'security':
        body_content += """
        <p>I take security matters seriously and will address this promptly.</p>
        """
    
    # Add closing and signature
    body_content += f"""
        <p>Thank you for your patience.</p>
        
        <br>
        <div style="border-top: 1px solid #eee; padding-top: 15px;">
            <p><strong>Best regards,</strong><br>
            <strong>Jai Mehtani</strong><br>
            <em>Computer Science Student & Developer</em><br>
            Charusat University<br>
            📧 22dcs047@charusat.edu.in</p>
            
            <p style="font-size: 11px; color: #666; margin-top: 20px;">
                <em>This is an automated acknowledgment. I will personally review and respond to your email.</em>
            </p>
        </div>
    </div>
    """
    
    return {
        'to': from_email,
        'subject': smart_subject,
        'body': body_content,
        'priority': email['priority'],
        'email_type': email['email_type'],
        'response_timeframe': response_timeframe,
        'original_subject': email['subject'],
        'created_at': datetime.now().isoformat()
    }

@app.route('/api/debug')
def api_debug():
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(debug=True)
