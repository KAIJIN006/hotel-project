StaySwift Hotel Reservation System

LOCAL SETUP (Windows)
1. Open this folder in VS Code.
2. Create a virtual environment: py -m venv .venv
3. Activate it: .venv\Scripts\activate
4. Install dependencies: pip install -r requirements.txt
5. Run: python app.py
6. Open http://127.0.0.1:5000

RENDER SETTINGS
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Runtime: Python 3
Root Directory: leave blank if app.py and requirements.txt are at repository root.
Environment: set SECRET_KEY to a long random private value.

DEMO ADMIN (change before any public use)
Email: admin@hotel.test
Password: Admin123!

NEW UI
- Dashboard with reservation and waiting-list summaries
- Find a Room page with date and room-type search
- Booking Calendar with booked and fully-booked day indicators

IMPORTANT
This remains a school-project prototype. Passwords are stored as plain text in this original schema and must be upgraded before public use. Render free local filesystem storage is temporary; use persistent storage or a managed database if you need booking data to survive redeploys/restarts.
