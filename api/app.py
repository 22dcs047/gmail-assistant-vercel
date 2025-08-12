# ENHANCED Gmail Assistant with REAL Gmail + OpenAI Integration
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
import os
import base64
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not available - using OS environment only")

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
    print("✅ Gmail API libraries loaded successfully")
except ImportError as e:
    GMAIL_AVAILABLE = False
    print(f"❌ Gmail API not available: {e}")

# OpenAI imports
try:
    import openai
    OPENAI_AVAILABLE = True
    print("✅ OpenAI library loaded successfully")
except ImportError as e:
    OPENAI_AVAILABLE = False
    print(f"❌ OpenAI not available: {e}")

app = Flask(__name__)

class EnhancedGmailAssistant:
    def __init__(self):
        self.user_email = "22dcs047@charusat.edu.in"
        self.gmail_service = None
        self.openai_client = None
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.send'
        ]
        
        print(f"🚀 Initializing ENHANCED Gmail Assistant for {self.user_email}")
        
        # Initialize Gmail API
        if GMAIL_AVAILABLE:
            try:
                self.authenticate_gmail()
                print("✅ Gmail authentication successful!")
            except Exception as e:
                print(f"⚠️ Gmail authentication failed: {e}")
                self.gmail_service = None
        else:
            print("❌ Gmail API not available - using fallback mode")
        
        # Initialize OpenAI
        if OPENAI_AVAILABLE:
            try:
                self.setup_openai()
                if self.openai_client:
                    print("✅ OpenAI setup successful!")
                else:
                    print("⚠️ OpenAI setup failed - using basic classification")
            except Exception as e:
                print(f"⚠️ OpenAI setup failed: {e}")
                self.openai_client = None
        else:
            print("❌ OpenAI not available - using basic classification")
    
    def authenticate_gmail(self):
        """Authenticate with Gmail API using existing tokens"""
        if not GMAIL_AVAILABLE:
            return False
            
        creds = None
        
        # Try to get paths relative to this file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        token_path = os.path.join(current_dir, 'token.json')
        credentials_path = os.path.join(current_dir, 'credentials.json')
        
        # Also try parent directory (fallback)
        if not os.path.exists(token_path):
            parent_dir = os.path.dirname(current_dir)
            token_path = os.path.join(parent_dir, 'token.json')
            credentials_path = os.path.join(parent_dir, 'credentials.json')
        
        print(f"🔍 Looking for credentials in: {current_dir}")
        print(f"📁 Token path: {token_path}")
        print(f"📁 Credentials path: {credentials_path}")
        
        # Load existing token
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
                print("📁 Loaded existing token.json")
            except Exception as e:
                print(f"❌ Error loading token: {e}")
                return False
        else:
            print("❌ token.json not found")
            return False
        
        # Refresh token if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                try:
                    creds.refresh(Request())
                    
                    # Save refreshed token
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    print("✅ Token refreshed and saved")
                except Exception as e:
                    print(f"❌ Token refresh failed: {e}")
                    return False
            else:
                print("❌ No valid credentials available")
                if not os.path.exists(credentials_path):
                    print(f"❌ credentials.json not found at {credentials_path}")
                return False
        
        # Build Gmail service
        try:
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail service built successfully")
            
            # Test the connection
            profile = self.gmail_service.users().getProfile(userId='me').execute()
            print(f"✅ Connected to Gmail account: {profile.get('emailAddress')}")
            return True
        except Exception as e:
            print(f"❌ Failed to build Gmail service: {e}")
            return False
    
    def setup_openai(self):
        """Setup OpenAI client"""
        # Try to get OpenAI API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized")
                
                # Test the connection with a minimal request
                test_response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                print("✅ OpenAI connection verified")
                return True
            except Exception as e:
                print(f"❌ OpenAI client setup failed: {e}")
                self.openai_client = None
                return False
        else:
            print("❌ OpenAI API key not found in environment")
            return False
    
    def ai_classify_email(self, subject, body, from_email):
        """Use OpenAI to intelligently classify email priority and type"""
        if not self.openai_client:
            # Fallback to basic classification
            return self._basic_classify_priority(from_email, subject, body), self._basic_analyze_email_type(subject, body, from_email)
        
        try:
            prompt = f"""
            Analyze this email and classify it:
            
            From: {from_email}
            Subject: {subject}
            Body: {body[:500]}...
            
            Please provide:
            1. Priority: critical, high, medium, or low
            2. Type: academic, security, job_related, meeting_request, newsletter, or general
            
            Priority guidelines:
            - critical: Security alerts, system emergencies, suspicious activity
            - high: Urgent deadlines, interviews, time-sensitive academic matters
            - medium: Regular academic emails, project discussions, meetings
            - low: Newsletters, updates, non-urgent communications
            
            Respond in JSON format:
            {{"priority": "medium", "type": "academic"}}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"🤖 AI classified email: {result['priority']} priority, {result['type']} type")
            return result['priority'], result['type']
            
        except Exception as e:
            print(f"⚠️ AI classification failed: {e}, using fallback")
            return self._basic_classify_priority(from_email, subject, body), self._basic_analyze_email_type(subject, body, from_email)
    
    def get_real_unread_emails(self):
        """Get ACTUAL unread emails from YOUR Gmail inbox in last 24 hours"""
        if not self.gmail_service:
            print("📧 Gmail service not available - using demo data")
            return self.get_demo_emails()
        
        try:
            # Calculate 24 hours ago
            now = datetime.now()
            past_time = now - timedelta(hours=24)
            
            # Gmail search query for unread emails in last 24 hours
            query = (
                f'is:unread '
                f'after:{int(past_time.timestamp())} '
                f'-subject:"Email Summary Report" '
                f'-subject:"Smart Email Summary" '
                f'-from:"{self.user_email}"'
            )
            
            print(f"🔍 Searching YOUR Gmail for unread emails in last 24 hours...")
            print(f"📧 Query: {query}")
            
            # Search Gmail
            results = self.gmail_service.users().messages().list(
                userId='me', q=query, maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            real_emails = []
            
            print(f"📧 Found {len(messages)} unread emails in YOUR Gmail!")
            
            # Process each email with AI classification
            for i, msg in enumerate(messages):
                try:
                    message = self.gmail_service.users().messages().get(
                        userId='me', id=msg['id'], format='full'
                    ).execute()
                    
                    email = self._parse_email_message_with_ai(message)
                    if email and not self._is_automated_email(email):
                        real_emails.append(email)
                        print(f"📧 {i+1}. {email['subject'][:60]}... [{email['priority'].upper()}]")
                
                except Exception as e:
                    print(f"⚠️ Error processing email {i+1}: {e}")
                    continue
            
            print(f"✅ Successfully processed {len(real_emails)} real emails from YOUR Gmail!")
            
            # If no real emails found, add demo emails to show the interface
            if not real_emails:
                print("📭 No recent unread emails found - adding demo emails for interface demo")
                return self.get_demo_emails()
            
            return real_emails
            
        except Exception as e:
            print(f"❌ Error fetching real emails: {e}")
            print("📧 Falling back to demo data")
            return self.get_demo_emails()
    
    def _parse_email_message_with_ai(self, message):
        """Parse Gmail message with AI classification"""
        try:
            headers = message['payload'].get('headers', [])
            
            from_email = ""
            subject = ""
            to_field = ""
            cc_field = ""
            
            for header in headers:
                name = header['name'].lower()
                value = header['value']
                
                if name == 'from':
                    from_email = value
                elif name == 'subject':
                    subject = value
                elif name == 'to':
                    to_field = value
                elif name == 'cc':
                    cc_field = value
            
            # Get email body
            snippet = message.get('snippet', '')
            
            # Parse timestamp
            timestamp = int(message['internalDate']) / 1000
            email_date = datetime.fromtimestamp(timestamp)
            
            # Use AI to classify email (with fallback)
            priority, email_type = self.ai_classify_email(subject, snippet, from_email)
            
            return {
                'id': message['id'],
                'from_email': from_email,
                'subject': subject,
                'body': snippet,
                'snippet': snippet[:100] + '...' if len(snippet) > 100 else snippet,
                'date': email_date.strftime('%Y-%m-%d'),
                'time': email_date.strftime('%H:%M'),
                'to_field': to_field,
                'cc_field': cc_field,
                'priority': priority,
                'email_type': email_type,
                'ai_classified': bool(self.openai_client)
            }
            
        except Exception as e:
            print(f"⚠️ Error parsing email: {e}")
            return None
    
    def create_real_gmail_draft(self, auto_reply):
        """Create ACTUAL Gmail draft in YOUR Gmail account"""
        if not self.gmail_service:
            print("❌ Gmail service not available - cannot create real draft")
            return False
        
        try:
            print(f"📝 Creating REAL Gmail draft for {auto_reply['to']}...")
            
            # Create email message
            message = MIMEMultipart('alternative')
            message['To'] = auto_reply['to']
            message['Subject'] = auto_reply['subject']
            message['From'] = self.user_email
            
            # Add HTML content
            html_part = MIMEText(auto_reply['body'], 'html')
            message.attach(html_part)
            
            # Create draft
            draft = {
                'message': {
                    'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
                }
            }
            
            # Send to Gmail API
            result = self.gmail_service.users().drafts().create(userId='me', body=draft).execute()
            
            print(f"✅ REAL Gmail draft created successfully! Draft ID: {result['id']}")
            print(f"📧 Check your Gmail Drafts folder!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating real Gmail draft: {e}")
            return False
    
    # Include all the basic classification methods as fallbacks
    def _basic_classify_priority(self, from_email, subject, body):
        """Basic priority classification fallback"""
        from_lower = from_email.lower()
        subject_lower = subject.lower()
        
        # Critical/Emergency
        if any(word in subject_lower for word in ["emergency", "critical", "system down", "security alert", "suspicious"]):
            return "critical"
            
        # High priority
        if any(word in subject_lower for word in ["urgent", "asap", "deadline today", "due today"]):
            return "high"
        if any(word in subject_lower for word in ["deadline", "submission deadline", "submit by", "due date"]):
            return "high"
        if any(word in subject_lower for word in ["interview", "offer", "final round"]):
            return "high"
            
        # Medium priority  
        if any(word in from_lower for word in ["@charusat.edu.in", "professor", "@edu"]):
            return "medium"
        if any(word in subject_lower for word in ["assignment", "project", "meeting"]):
            return "medium"
            
        # Low priority
        if any(word in subject_lower for word in ["digest", "update", "newsletter"]):
            return "low"
            
        return "medium"
    
    def _basic_analyze_email_type(self, subject, body, from_email):
        """Basic email type analysis fallback"""
        subject_lower = subject.lower()
        from_lower = from_email.lower()
        
        if any(word in subject_lower for word in ["meeting", "schedule", "call"]):
            return "meeting_request"
        elif any(word in from_lower for word in ["hr@", "recruiter"]) or any(word in subject_lower for word in ["interview", "job"]):
            return "job_related"
        elif any(word in from_lower for word in ["@charusat.edu.in", "@edu"]) or any(word in subject_lower for word in ["assignment", "practical"]):
            return "academic"
        elif any(word in subject_lower for word in ["urgent", "security", "alert", "suspicious"]):
            return "security"
        else:
            return "general"
    
    def _is_automated_email(self, email):
        """Filter out automated emails"""
        automated_patterns = [
            "email summary report", "smart email summary", "complete email summary",
            "automated", "do-not-reply", "unsubscribe"
        ]
        
        subject_lower = email['subject'].lower()
        from_lower = email['from_email'].lower()
        
        # Skip emails from self
        if self.user_email in from_lower:
            return True
            
        # Skip acknowledged emails
        if "acknowledged" in subject_lower and "re:" in subject_lower:
            return True
        
        # Skip automated patterns
        if any(pattern in subject_lower for pattern in automated_patterns):
            return True
            
        return False
    
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
                'ai_classified': False
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
                'ai_classified': False
            }
        ]
    
    def get_email_stats(self):
        """Get real email statistics"""
        emails = self.get_real_unread_emails()
        direct = [e for e in emails if self.user_email in e['to_field']]
        cc = [e for e in emails if self.user_email in e['cc_field']]
        high_priority = [e for e in emails if e['priority'] in ['high', 'critical']]
        
        stats = {
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
            'demo_mode': not bool(self.gmail_service),
            'data_source': 'Real Gmail API + AI' if self.gmail_service and self.openai_client else 'Real Gmail API' if self.gmail_service else 'Demo Data',
            'gmail_connected': bool(self.gmail_service),
            'openai_connected': bool(self.openai_client),
            'capabilities': {
                'gmail_api': bool(self.gmail_service),
                'ai_classification': bool(self.openai_client),
                'real_draft_creation': bool(self.gmail_service)
            }
        }
        
        return stats

# Initialize ENHANCED Gmail Assistant
print("🚀 Starting ENHANCED Gmail Assistant with AI Integration...")
gmail_assistant = EnhancedGmailAssistant()

# API Routes
@app.route('/api/emails')
def api_emails():
    return jsonify(gmail_assistant.get_email_stats())

@app.route('/api/create-real-drafts', methods=['POST'])
def api_create_real_drafts():
    try:
        data = gmail_assistant.get_email_stats()
        high_priority_emails = [e for e in data['direct_emails'] if e['priority'] in ['high', 'critical']]
        
        if not high_priority_emails:
            return jsonify({
                'status': 'success',
                'message': 'No high-priority emails found.',
                'gmail_connected': bool(gmail_assistant.gmail_service)
            })
        
        real_drafts_created = []
        for email in high_priority_emails:
            auto_reply = generate_auto_reply_draft(email)
            if gmail_assistant.gmail_service:
                success = gmail_assistant.create_real_gmail_draft(auto_reply)
                if success:
                    real_drafts_created.append(auto_reply)
        
        return jsonify({
            'status': 'success',
            'message': f'Created {len(real_drafts_created)} AI-powered Gmail drafts!',
            'gmail_connected': bool(gmail_assistant.gmail_service)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/debug')
def api_debug():
    stats = gmail_assistant.get_email_stats()
    return jsonify({
        'gmail_connected': bool(gmail_assistant.gmail_service),
        'openai_connected': bool(gmail_assistant.openai_client),
        'data_source': stats['data_source'],
        'capabilities': stats['capabilities'],
        'stats': stats['stats']
    })

def generate_auto_reply_draft(email):
    from_email = email['from_email']
    if '<' in from_email:
        match = re.search(r'<([^>]+)>', from_email)
        from_email = match.group(1) if match else from_email
    
    timeframes = {'academic': '2-4 hours', 'security': '1-2 hours', 'general': '24-48 hours'}
    response_timeframe = timeframes.get(email['email_type'], '24-48 hours')
    
    body_content = f"""
    <p>Thank you for your email regarding "{email['subject']}". I will respond within {response_timeframe}.</p>
    <br><p>Best regards,<br>Jai Mehtani<br>📧 22dcs047@charusat.edu.in</p>
    """
    
    return {
        'to': from_email,
        'subject': f"Re: {email['subject']} - Acknowledged",
        'body': body_content,
        'priority': email['priority']
    }

# Simple Flask routes
@app.route('/')
def home():
    return '''<h1>🧠 AI Gmail Assistant</h1>
    <a href="/dashboard">Dashboard</a> | <a href="/debug">Status</a>'''

@app.route('/dashboard')
def dashboard():
    return '''<!DOCTYPE html>
<html><head><title>Dashboard</title></head>
<body>
<h1>📊 AI Gmail Dashboard</h1>
<div id="stats"></div>
<div id="emails"></div>
<script>
fetch('/api/emails').then(r=>r.json()).then(data=>{
    document.getElementById('stats').innerHTML = `
        <p>📧 Gmail: ${data.gmail_connected ? 'Connected' : 'Demo'}</p>
        <p>🧠 AI: ${data.openai_connected ? 'Enabled' : 'Basic'}</p>
        <p>Total: ${data.stats.total_unread} emails</p>
    `;
    let html = '';
    data.direct_emails.forEach(e => {
        html += `<div><h3>${e.subject}</h3><p>${e.snippet}</p></div>`;
    });
    document.getElementById('emails').innerHTML = html;
});
</script>
</body></html>'''

@app.route('/debug')
def debug():
    return '''<h1>🔍 Status</h1><pre id="data"></pre>
    <script>fetch('/api/debug').then(r=>r.json()).then(d=>
    document.getElementById('data').textContent=JSON.stringify(d,null,2))
    </script>'''

if __name__ == '__main__':
    app.run(debug=True)
