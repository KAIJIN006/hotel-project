STAYSWIFT — HOTEL ROOM RESERVATION & WAITING LIST

SETUP ON WINDOWS / VS CODE
1. Extract the ZIP and open the stayswift folder in VS Code.
2. Open Terminal.
3. Run: py -m venv .venv
4. Activate: .venv\Scripts\Activate.ps1
   If PowerShell blocks it, use Command Prompt and run: .venv\Scripts\activate.bat
5. Install: pip install -r requirements.txt
6. Run: python app.py
7. Open http://127.0.0.1:5000

ADMIN DEMO LOGIN
Email: admin@hotel.test
Password: Admin123!
Guests can register accounts from the website.

EMAIL SETUP
Without SMTP configuration, email content is printed in the terminal as a preview.
For actual email, set environment variables before starting the app:
SMTP_HOST (example smtp.gmail.com), SMTP_PORT (587), SMTP_USER, SMTP_PASSWORD,
SMTP_FROM, and SECRET_KEY. For Gmail, use an App Password. Never share these secrets.

POWERSHELL EXAMPLE
$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="youraddress@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:SMTP_FROM="youraddress@gmail.com"
$env:SECRET_KEY="a-long-random-secret"
python app.py

HOW THE WAITLIST WORKS
A guest chooses room type and dates. If a matching room is free, booking is confirmed.
If full, the guest joins the waiting list. When a matching reservation is cancelled,
the app emails all matching waiting guests with unique claim links. SQLite BEGIN IMMEDIATE
serializes claim requests: the first successful claim creates the booking; later claims fail.

IMPORTANT
This is a school-project prototype. Before public/real hotel use, add password hashing,
CSRF protection, HTTPS, rate limiting, reliable email queue/retries, audit logs, testing,
and stronger admin controls. The sample app uses simple demo passwords for learning only.
