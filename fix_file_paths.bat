@echo off
echo 🔧 FIXING: Dashboard and Debug File Paths...

:: Navigate to the project directory
cd /d "C:\Users\joyme\OneDrive\Desktop\gmail-assistant\web-dashboard-clean"

:: Add all changes
echo 📁 Adding file path fixes...
git add .

:: Commit the fix
echo 💾 Committing file path fixes...
git commit -m "🔧 FIX: Dashboard and Debug File Paths - Moved HTML files to api directory for proper Vercel deployment, Updated file paths in app.py to resolve 'file not found' errors, Fixed dashboard and debug routes for live site"

:: Push to origin
echo 🌐 Pushing fixes to live site...
git push origin main

echo.
echo ✅ FILE PATH FIXES DEPLOYED!
echo.
echo 🔗 Your Gmail Assistant should now work properly:
echo    https://gmailassistant.vercel.app
echo.
echo 📱 Test these pages:
echo    ✅ Dashboard: https://gmailassistant.vercel.app/dashboard
echo    ✅ Debug: https://gmailassistant.vercel.app/debug
echo.
echo ⚡ Changes will be live in 2-3 minutes!
pause