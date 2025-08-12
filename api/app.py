        
        <div id="statusInfo">Loading...</div>
        
        <h3>📊 Detailed System Information</h3>
        <pre id="debugInfo">Loading...</pre>
    </div>
    <script>
        async function loadDebug() {
            try {
                const response = await fetch('/api/debug');
                const data = await response.json();
                
                const statusDiv = document.getElementById('statusInfo');
                let statusHTML = '';
                
                if (data.gmail_connected) {
                    statusHTML += `
                        <div class="status connected">
                            <h3>✅ Gmail Connection: ACTIVE</h3>
                            <p>Successfully connected to Gmail API</p>
                        </div>
                    `;
                } else {
                    statusHTML += `
                        <div class="status disconnected">
                            <h3>❌ Gmail Connection: NOT ACTIVE</h3>
                            <p>Using demo data - Gmail API not connected</p>
                        </div>
                    `;
                }
                
                if (data.openai_connected) {
                    statusHTML += `
                        <div class="status ai-enabled">
                            <h3>🧠 OpenAI Integration: ACTIVE</h3>
                            <p>AI-powered email classification and reply generation enabled</p>
                        </div>
                    `;
                } else {
                    statusHTML += `
                        <div class="status disconnected">
                            <h3>❌ OpenAI Integration: NOT ACTIVE</h3>
                            <p>Using basic classification - AI features not available</p>
                        </div>
                    `;
                }
                
                statusHTML += `
                    <div class="status" style="background: #e2e3e5; color: #383d41; border: 1px solid #d6d8db;">
                        <h3>📊 System Capabilities</h3>
                        <p><strong>Data Source:</strong> ${data.data_source}</p>
                        <p><strong>Gmail API:</strong> ${data.capabilities?.gmail_api ? '✅ Available' : '❌ Not Available'}</p>
                        <p><strong>AI Classification:</strong> ${data.capabilities?.ai_classification ? '✅ Enabled' : '❌ Disabled'}</p>
                        <p><strong>Real Draft Creation:</strong> ${data.capabilities?.real_draft_creation ? '✅ Enabled' : '❌ Disabled'}</p>
                    </div>
                `;
                
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

if __name__ == '__main__':
    print("🚀 Starting ENHANCED AI Gmail Assistant Web Server...")
    print(f"📧 Gmail Connected: {bool(gmail_assistant.gmail_service)}")
    print(f"🧠 OpenAI Connected: {bool(gmail_assistant.openai_client)}")
    app.run(debug=True)