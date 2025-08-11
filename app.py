import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import threading
import time

# For production deployment
from flask import Flask, render_template, jsonify, request

# Import Gmail API components
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    print("Gmail API not available - running in demo mode")
    GMAIL_AVAILABLE = False

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
    'demo_mode': not GMAIL_AVAILABLE
}

class WebGmailAssistant:
    def __init__(self):
        self.gmail_service = None
        self.user_email = "22dcs047@charusat.edu.in"
        self.processing = False
        
        # Gmail API scopes
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.send'
        ]

    def authenticate_gmail(self):
        """Authenticate with Gmail API using environment variables or demo mode"""
        if not GMAIL_AVAILABLE:
            return False
            
        # In production, you would handle OAuth differently
        # For demo purposes, we'll create sample data
        return True

    def process_emails_for_web(self):
        """Process emails and return data for web dashboard"""
        global current_email_data
        
        current_email_data['is_processing'] = True
        current_email_data['error_message'] = None
        
        try:
            if GMAIL_AVAILABLE and self.authenticate_gmail():
                # Real Gmail processing would go here
                all_emails = self.get_sample_emails()  # Using sample data for demo
            else:
                # Demo mode with sample data
                all_emails = self.get_sample_emails()
            
            # Enhanced email categorization with debugging
            direct_emails = []
            cc_emails = []
            uncategorized_emails = []
            
            print(f"🔍 DEBUG: Processing {len(all_emails)} total emails")
            
            for email in all_emails:
                print(f"📧 Email: {email.subject[:50]}")
                print(f"   To: {email.to_field}")
                print(f"   CC: {email.cc_field}")
                print(f"   Priority: {email.priority}")
                
                # More flexible email categorization
                user_email = self.user_email.lower()
                to_field_lower = (email.to_field or "").lower()
                cc_field_lower = (email.cc_field or "").lower()
                
                # Check if user email is in To field (direct email)
                is_direct = (user_email in to_field_lower or 
                           "22dcs047@charusat.edu.in" in to_field_lower or
                           any(user_email in addr.strip().lower() for addr in to_field_lower.split(',') if addr.strip()))
                
                # Check if user email is in CC field
                is_cc = (user_email in cc_field_lower or 
                        "22dcs047@charusat.edu.in" in cc_field_lower or
                        any(user_email in addr.strip().lower() for addr in cc_field_lower.split(',') if addr.strip()))
                
                if is_direct:
                    direct_emails.append(email)
                    print(f"   ✅ Categorized as DIRECT")
                elif is_cc:
                    cc_emails.append(email)
                    print(f"   ✅ Categorized as CC")
                else:
                    # If neither direct nor CC, treat as direct (fallback)
                    direct_emails.append(email)
                    uncategorized_emails.append(email)
                    print(f"   ⚠️ Uncategorized - adding to DIRECT as fallback")
                
                print(f"   ---")
            
            print(f"📊 FINAL COUNTS:")
            print(f"   Direct: {len(direct_emails)}")
            print(f"   CC: {len(cc_emails)}")
            print(f"   Uncategorized (added to direct): {len(uncategorized_emails)}")
            
            # Calculate statistics with separate counts for direct and CC emails
            priority_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            direct_priority_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            cc_priority_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            type_counts = {}
            
            for email in all_emails:
                priority_counts[email.priority] = priority_counts.get(email.priority, 0) + 1
                type_counts[email.email_type] = type_counts.get(email.email_type, 0) + 1
            
            # Calculate priority counts for direct emails
            for email in direct_emails:
                direct_priority_counts[email.priority] = direct_priority_counts.get(email.priority, 0) + 1
                
            # Calculate priority counts for CC emails
            for email in cc_emails:
                cc_priority_counts[email.priority] = cc_priority_counts.get(email.priority, 0) + 1
            
            print(f"📈 Priority counts: {priority_counts}")
            print(f"📥 Direct priority counts: {direct_priority_counts}")
            print(f"📩 CC priority counts: {cc_priority_counts}")
            
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
                    'direct_priority_counts': direct_priority_counts,
                    'cc_priority_counts': cc_priority_counts,
                    'type_counts': type_counts,
                    'high_priority_count': priority_counts['critical'] + priority_counts['high'],
                    'direct_high_priority_count': direct_priority_counts['critical'] + direct_priority_counts['high'],
                    'cc_high_priority_count': cc_priority_counts['critical'] + cc_priority_counts['high'],
                    'uncategorized_count': len(uncategorized_emails)  # Added for debugging
                },
                'last_updated': datetime.now().isoformat(),
                'is_processing': False,
                'error_message': None,
                'demo_mode': not GMAIL_AVAILABLE
            })
            
            print(f"✅ Email processing complete!")
            
        except Exception as e:
            print(f"❌ Error processing emails: {e}")
            import traceback
            traceback.print_exc()
            
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
                snippet="JAI MEHTANI Stories for JAI MEHTANI @22dcs047·Become a member Medium daily digest Today's highlights...",
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
                body="Hi Joy MEHTANI, Join the red-teaming challenge",
                snippet="Hi Joy MEHTANI, Join the red-teaming challenge and discover new vulnerabilities in a newly released model.",
                date="2025-08-07",
                time="19:29",
                to_field="22dcs047@charusat.edu.in",
                cc_field="",
                priority="high",
                email_type="academic"
            ),
            # Add more sample emails...
        ]
        
        # Add some CC'd emails
        cc_email = EmailData(
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
        sample_emails.append(cc_email)
        
        return sample_emails

# Initialize the web assistant
web_assistant = WebGmailAssistant()

@app.route('/')
def welcome():
    """Welcome page for new users"""
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/debug')
def debug_page():
    """Debug page to see raw email data"""
    return render_template('debug.html')

@app.route('/api/emails')
def get_emails():
    """API endpoint to get current email data"""
    return jsonify(current_email_data)

@app.route('/api/refresh', methods=['POST'])
def refresh_emails():
    """API endpoint to refresh email data"""
    if current_email_data['is_processing']:
        return jsonify({'status': 'already_processing'})
    
    # Run email processing in a separate thread to avoid blocking
    def process_in_background():
        web_assistant.process_emails_for_web()
    
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'processing_started'})

@app.route('/api/create-drafts', methods=['POST'])
def create_drafts():
    """API endpoint to create drafts for high-priority emails"""
    try:
        print("🔍 DEBUG: Starting draft creation process")
        print(f"📊 Total direct emails available: {len(current_email_data.get('direct_emails', []))}")
        
        if current_email_data.get('demo_mode', False):
            return jsonify({
                'status': 'success',
                'drafts_created': 0,
                'high_priority_emails': 0,
                'message': 'Demo mode - Draft creation not available'
            })
        
        # Get high-priority emails from direct emails
        high_priority_emails = []
        
        for email_dict in current_email_data.get('direct_emails', []):
            print(f"📧 Checking email: {email_dict.get('subject', 'No subject')[:50]}")
            print(f"   Priority: {email_dict.get('priority')}")
            
            if email_dict.get('priority') in ['high', 'critical']:
                high_priority_emails.append(email_dict)
                print(f"   ✅ Added to high-priority list")
            else:
                print(f"   ⏭️ Skipped (not high/critical priority)")
        
        print(f"🎯 Found {len(high_priority_emails)} high-priority emails")
        
        return jsonify({
            'status': 'success',
            'drafts_created': 0,  # Would create actual drafts in production
            'high_priority_emails': len(high_priority_emails),
            'message': f'Found {len(high_priority_emails)} high-priority emails (Demo mode)'
        })
        
    except Exception as e:
        print(f"❌ Error in draft creation process: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/email/<email_id>')
def get_email_details(email_id):
    """API endpoint to get detailed email information"""
    for email in current_email_data['all_emails']:
        if email['id'] == email_id:
            return jsonify(email)
    return jsonify({'error': 'Email not found'}), 404

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to see raw email data"""
    debug_data = {
        'current_data_keys': list(current_email_data.keys()),
        'total_emails': len(current_email_data.get('all_emails', [])),
        'direct_emails': len(current_email_data.get('direct_emails', [])),
        'cc_emails': len(current_email_data.get('cc_emails', [])),
        'stats': current_email_data.get('stats', {}),
        'last_updated': current_email_data.get('last_updated'),
        'is_processing': current_email_data.get('is_processing'),
        'error_message': current_email_data.get('error_message'),
        'demo_mode': current_email_data.get('demo_mode', False),
    }
    
    # Add sample of emails for debugging
    if current_email_data.get('all_emails'):
        debug_data['sample_emails'] = [
            {
                'subject': email['subject'][:50],
                'to_field': email['to_field'],
                'cc_field': email['cc_field'],
                'priority': email['priority'],
                'from_email': email['from_email'][:30]
            }
            for email in current_email_data['all_emails'][:5]
        ]
    
    return jsonify(debug_data)

# Initialize data on startup
web_assistant.process_emails_for_web()

if __name__ == '__main__':
    print("🚀 Starting Gmail Assistant Web Dashboard...")
    print("📱 Dashboard will be available at: http://localhost:5000")
    print("🔄 Loading initial email data...")
    
    # Use different settings for development vs production
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
