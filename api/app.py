# Real Gmail Assistant with AI Integration for Vercel deployment
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
import os
import base64
from email.mime.text import MIMEText
import time

# Import Gmail API libraries
try:
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

# Import OpenAI
try:
    import openai
    from dotenv import load_dotenv
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

app = Flask(__name__)

# Load environment variables
if OPENAI_AVAILABLE:
    load_dotenv()

class RealGmailAssistant:
    def __init__(self):
        self.user_email = os.getenv('GMAIL_USER_EMAIL', '22dcs047@charusat.edu.in')
        self.scopes = ['https://www.googleapis.com/auth/gmail.readonly', 
                      'https://www.googleapis.com/auth/gmail.compose',
                      'https://www.googleapis.com/auth/gmail.modify']
        
        # Initialize OpenAI
        self.openai_available = False
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_available = True
                print(f"🧠 OpenAI initialized successfully")
            except Exception as e:
                print(f"❌ OpenAI initialization failed: {e}")
        
        # Initialize Gmail
        self.gmail_service = None
        self.gmail_connected = False
        if GMAIL_AVAILABLE:
            self._initialize_gmail()
        
        print(f"🚀 Gmail Assistant initialized")
        print(f"📧 Gmail Connected: {self.gmail_connected}")
        print(f"🧠 OpenAI Available: {self.openai_available}")
    
    def _initialize_gmail(self):
        """Initialize Gmail API connection"""
        try:
            creds = None
            token_path = 'token.json'
            credentials_path = 'credentials.json'
            
            # Try to load existing credentials
            if os.path.exists(token_path):
                try:
                    creds = Credentials.from_authorized_user_file(token_path, self.scopes)
                except Exception as e:
                    print(f"❌ Error loading token: {e}")
            
            # If no valid credentials, try to refresh or create
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                        # Save refreshed credentials
                        with open(token_path, 'w') as token:
                            token.write(creds.to_json())
                        print("✅ Token refreshed successfully")
                    except Exception as e:
                        print(f"❌ Token refresh failed: {e}")
                        return False
                else:
                    print("❌ No valid credentials found")
                    return False
            
            # Build Gmail service
            if creds and creds.valid:
                self.gmail_service = build('gmail', 'v1', credentials=creds)
                self.gmail_connected = True
                print("✅ Gmail API connected successfully")
                return True
            else:
                print("❌ No valid Gmail credentials")
                return False
                
        except Exception as e:
            print(f"❌ Gmail initialization error: {e}")
            return False
    
    def classify_email_with_ai(self, subject, body, sender):
        """Use OpenAI to classify email priority and type"""
        if not self.openai_available:
            return self._classify_email_basic(subject, body, sender)
        
        try:
            prompt = f"""Analyze this email and classify it:

Subject: {subject}
From: {sender}
Content: {body[:500]}...

Provide a JSON response with:
1. priority: "critical", "high", "medium", or "low"
2. email_type: "academic", "security", "personal", "promotional", "work", or "general"
3. urgency_reason: brief explanation for the priority level

Format as valid JSON only."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            result['ai_classified'] = True
            return result
            
        except Exception as e:
            print(f"❌ AI classification error: {e}")
            return self._classify_email_basic(subject, body, sender)
    
    def _classify_email_basic(self, subject, body, sender):
        """Basic rule-based email classification"""
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Critical keywords
        critical_keywords = ['urgent', 'critical', 'emergency', 'immediate', 'asap', 'deadline', 'expires', 'security alert']
        high_keywords = ['important', 'reminder', 'due', 'meeting', 'interview', 'submission']
        
        priority = 'low'
        if any(keyword in subject_lower or keyword in body_lower for keyword in critical_keywords):
            priority = 'critical'
        elif any(keyword in subject_lower or keyword in body_lower for keyword in high_keywords):
            priority = 'high'
        elif 'no-reply' not in sender.lower() and '@charusat.edu.in' in sender:
            priority = 'medium'
        
        # Determine email type
        email_type = 'general'
        if '@charusat.edu.in' in sender or 'professor' in sender.lower() or 'academic' in subject_lower:
            email_type = 'academic'
        elif 'security' in subject_lower or 'alert' in subject_lower or 'github' in sender.lower():
            email_type = 'security'
        elif 'noreply' in sender or 'unsubscribe' in body_lower:
            email_type = 'promotional'
        
        return {
            'priority': priority,
            'email_type': email_type,
            'urgency_reason': f'Classified as {priority} based on keywords and sender',
            'ai_classified': False
        }
    
    def get_unread_emails(self):
        """Get real unread emails from Gmail"""
        if not self.gmail_connected:
            return self.get_demo_emails()
        
        try:
            # Get unread emails from last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
            query = f'is:unread after:{yesterday} -from:me'
            
            result = self.gmail_service.users().messages().list(
                userId='me', q=query, maxResults=50
            ).execute()
            
            messages = result.get('messages', [])
            emails = []
            
            for message in messages[:20]:  # Limit to 20 emails for performance
                try:
                    msg = self.gmail_service.users().messages().get(
                        userId='me', id=message['id'], format='full'
                    ).execute()
                    
                    headers = msg['payload'].get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    to_field = next((h['value'] for h in headers if h['name'] == 'To'), '')
                    cc_field = next((h['value'] for h in headers if h['name'] == 'Cc'), '')
                    date_header = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                    
                    # Get email body
                    body = self._extract_email_body(msg['payload'])
                    snippet = msg.get('snippet', '')
                    
                    # Parse date
                    try:
                        email_date = datetime.fromtimestamp(int(msg['internalDate']) / 1000)
                        date_str = email_date.strftime('%Y-%m-%d')
                        time_str = email_date.strftime('%H:%M')
                    except:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        time_str = datetime.now().strftime('%H:%M')
                    
                    # Classify with AI
                    classification = self.classify_email_with_ai(subject, body, from_email)
                    
                    emails.append({
                        'id': message['id'],
                        'subject': subject,
                        'from_email': from_email,
                        'to_field': to_field,
                        'cc_field': cc_field,
                        'snippet': snippet,
                        'body': body[:1000] + '...' if len(body) > 1000 else body,
                        'date': date_str,
                        'time': time_str,
                        'priority': classification['priority'],
                        'email_type': classification['email_type'],
                        'ai_classified': classification['ai_classified'],
                        'urgency_reason': classification.get('urgency_reason', '')
                    })
                    
                except Exception as e:
                    print(f"❌ Error processing email {message['id']}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return self.get_demo_emails()
    
    def _extract_email_body(self, payload):
        """Extract text content from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        elif payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body.strip()
    
    def create_ai_draft(self, original_email):
        """Create an AI-powered draft reply"""
        if not self.openai_available:
            return self._create_basic_draft(original_email)
        
        try:
            prompt = f"""Create a professional auto-reply for this email:

Original Subject: {original_email['subject']}
From: {original_email['from_email']}
Priority: {original_email['priority']}
Content: {original_email['body'][:500]}...

Generate a professional acknowledgment email that:
1. Acknowledges receipt
2. Indicates understanding of priority level
3. Provides appropriate response timeframe
4. Maintains professional tone
5. Is concise but personalized

Format as plain text email body only."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            ai_body = response.choices[0].message.content.strip()
            
            # Add professional signature
            full_body = f"""{ai_body}

Best regards,
Jai Mehtani
Computer Science Student & Developer
Charusat University
📧 22dcs047@charusat.edu.in

🤖 This is an AI-assisted acknowledgment. I will personally review and respond to your email."""

            return full_body
            
        except Exception as e:
            print(f"❌ AI draft creation error: {e}")
            return self._create_basic_draft(original_email)
    
    def _create_basic_draft(self, original_email):
        """Create basic template draft"""
        priority_responses = {
            'critical': 'I understand this is critical and will respond within 2 hours.',
            'high': 'I understand this is important and will respond within 24 hours.',
            'medium': 'I will respond within 2-3 business days.',
            'low': 'I will respond within a week.'
        }
        
        response_time = priority_responses.get(original_email['priority'], 'I will respond soon.')
        
        return f"""Thank you for your email regarding "{original_email['subject']}".

I have received your message and {response_time}

Best regards,
Jai Mehtani
Computer Science Student & Developer
Charusat University
📧 22dcs047@charusat.edu.in

🤖 This is an automated acknowledgment. I will personally review and respond to your email."""
    
    def create_gmail_draft(self, original_email):
        """Create actual Gmail draft"""
        if not self.gmail_connected:
            return False, "Gmail not connected"
        
        try:
            # Generate AI-powered reply content
            reply_body = self.create_ai_draft(original_email)
            
            # Create draft message
            subject = f"Re: {original_email['subject']}"
            
            message = MIMEText(reply_body)
            message['to'] = original_email['from_email']
            message['subject'] = subject
            
            # Create draft
            draft = {
                'message': {
                    'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
                }
            }
            
            created_draft = self.gmail_service.users().drafts().create(
                userId='me', body=draft
            ).execute()
            
            return True, f"Draft created with ID: {created_draft['id']}"
            
        except Exception as e:
            return False, f"Error creating draft: {e}"
    
    def get_demo_emails(self):
        """Demo emails for fallback"""
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        
        return [
            {
                'id': 'demo_1',
                'subject': '🔴 URGENT: Kaggle Competition Deadline in 3 Hours!',
                'from_email': 'Kaggle <no-reply@kaggle.com>',
                'priority': 'critical',
                'to_field': '22dcs047@charusat.edu.in',
                'cc_field': '',
                'snippet': 'Hi Jai Mehtani, Your submission deadline is approaching fast...',
                'body': 'Hi Jai Mehtani, Your submission for the AI Red-Teaming Challenge is due in 3 hours. Don\'t miss out on the $50,000 prize pool!',
                'date': today,
                'time': (now - timedelta(minutes=30)).strftime('%H:%M'),
                'email_type': 'academic',
                'ai_classified': self.openai_available,
                'urgency_reason': 'Critical deadline approaching'
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
                'ai_classified': self.openai_available,
                'urgency_reason': 'Security threat detected'
            }
        ]
    
    def get_email_stats(self):
        """Get comprehensive email statistics"""
        try:
            emails = self.get_unread_emails()
        except Exception as e:
            print(f"❌ Error getting emails: {e}")
            emails = self.get_demo_emails()
        
        # Separate direct and CC emails
        direct = [e for e in emails if self.user_email in e.get('to_field', '')]
        cc = [e for e in emails if self.user_email in e.get('cc_field', '') and self.user_email not in e.get('to_field', '')]
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
            'gmail_connected': self.gmail_connected,
            'openai_connected': self.openai_available,
            'data_source': 'Real Gmail + AI' if self.gmail_connected and self.openai_available else 
                          'Real Gmail' if self.gmail_connected else 
                          'Demo Data + AI' if self.openai_available else 'Demo Data',
            'capabilities': {
                'gmail_api': self.gmail_connected,
                'ai_classification': self.openai_available,
                'real_draft_creation': self.gmail_connected
            }
        }

# Initialize assistant
assistant = RealGmailAssistant()

@app.route('/')
def home():
    status = "AI-Powered" if assistant.openai_available else "Standard"
    gmail_status = "Connected" if assistant.gmail_connected else "Demo Mode"
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
        .live-badge {{ background: linear-gradient(45deg, #{'00b894, #00cec9' if assistant.gmail_connected else 'ff6b6b, #ee5a24'}); color: white; padding: 12px 25px; border-radius: 50px; font-weight: 600; margin-bottom: 20px; display: inline-block; animation: pulse 2s infinite; }}
        .ai-badge {{ background: linear-gradient(45deg, #00b894, #00cec9); color: white; padding: 12px 25px; border-radius: 50px; font-weight: 600; margin-bottom: 30px; display: inline-block; animation: glow 3s infinite; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        @keyframes glow {{ 0% {{ box-shadow: 0 0 10px rgba(0,184,148,0.5); }} 50% {{ box-shadow: 0 0 25px rgba(0,184,148,0.8); }} 100% {{ box-shadow: 0 0 10px rgba(0,184,148,0.5); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="live-badge"><i class="fas fa-{'satellite-dish' if assistant.gmail_connected else 'exclamation-triangle'}"></i> {gmail_status.upper()} <i class="fas fa-{'satellite-dish' if assistant.gmail_connected else 'exclamation-triangle'}"></i></div>
            <div class="ai-badge"><i class="fas fa-brain"></i> {status.upper()} INTELLIGENCE <i class="fas fa-robot"></i></div>
            <h1><i class="fas fa-envelope-open-text"></i> {status} Gmail Assistant</h1>
            <p>{'Real Gmail integration' if assistant.gmail_connected else 'Demo mode'} with {'AI-powered' if assistant.openai_available else 'intelligent'} email classification and auto-replies</p>
            <a href="/dashboard" class="btn"><i class="fas fa-rocket"></i> Open Dashboard</a>
            <a href="/debug" class="btn" style="background: rgba(255,255,255,0.2); color: white;"><i class="fas fa-code"></i> System Status</a>
        </div>
    </div>
</body>
</html>'''

@app.route('/dashboard')
def dashboard():
    try:
        with open('dashboard.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Dashboard file not found", 404

@app.route('/debug') 
def debug():
    try:
        with open('debug.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Debug file not found", 404

@app.route('/api/emails')
def api_emails():
    return jsonify(assistant.get_email_stats())

@app.route('/api/create-drafts', methods=['POST'])
def api_create_drafts():
    try:
        data = request.json
        emails = data.get('emails', [])
        
        if not assistant.gmail_connected:
            return jsonify({
                'success': False,
                'error': 'Gmail not connected - running in demo mode'
            })
        
        drafts_created = 0
        errors = []
        
        for email in emails:
            try:
                success, message = assistant.create_gmail_draft(email)
                if success:
                    drafts_created += 1
                else:
                    errors.append(f"Failed to create draft for '{email['subject']}': {message}")
            except Exception as e:
                errors.append(f"Error with email '{email['subject']}': {str(e)}")
        
        return jsonify({
            'success': drafts_created > 0,
            'drafts_created': drafts_created,
            'errors': errors,
            'message': f'Created {drafts_created} drafts successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/debug')
def api_debug():
    return jsonify({
        'gmail_connected': assistant.gmail_connected,
        'openai_connected': assistant.openai_available,
        'data_source': assistant.get_email_stats()['data_source'],
        'capabilities': assistant.get_email_stats()['capabilities'],
        'stats': assistant.get_email_stats()['stats'],
        'environment': {
            'openai_key_exists': bool(os.getenv('OPENAI_API_KEY')),
            'gmail_libraries_available': GMAIL_AVAILABLE,
            'openai_libraries_available': OPENAI_AVAILABLE,
            'platform': 'vercel'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)