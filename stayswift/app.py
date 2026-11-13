import os, sqlite3, secrets, smtplib, calendar
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, abort

app=Flask(__name__); app.secret_key=os.getenv('SECRET_KEY','change-this-secret-before-deploying'); DB=os.getenv('DATABASE_PATH','hotel.db')
BASE='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>StaySwift Hotel</title><style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');:root{--ink:#172b2a;--green:#1e6255;--bg:#f7f8f4;--muted:#71817d;--line:#e4eae5}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}nav{height:72px;background:white;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 max(calc((100% - 1080px)/2),22px)}nav a{margin-left:18px;color:var(--green);text-decoration:none;font-size:14px}.logo{font-size:23px;font-weight:700;color:var(--ink);margin:0}main{max-width:1080px;margin:35px auto;padding:0 22px}footer{text-align:center;color:#91a099;padding:30px;font-size:12px}.hero{background:#e7eee8;border-radius:18px;min-height:300px;padding:50px 7%;display:flex;justify-content:space-between;align-items:center}.hero h1,h1{font:600 44px/1.13 'Playfair Display',serif}.hero i{color:var(--green)}.hero p{max-width:440px;color:#60716c;line-height:1.7}.orb{width:180px;height:180px;border-radius:50%;background:var(--green);color:#e1eee6;display:grid;place-content:center;text-align:center;font-size:70px;box-shadow:18px 16px #d1dfd5}.orb small{font:10px 'DM Sans';letter-spacing:3px}.panel{background:white;border:1px solid var(--line);border-radius:14px;padding:25px;margin:18px 0;box-shadow:0 8px 28px #193b2b08}.eyebrow{color:#6d9185;letter-spacing:2px;font-weight:bold;font-size:11px}.formgrid{display:grid;grid-template-columns:1.2fr 1fr 1fr auto;gap:13px;align-items:end}.stack{display:grid;gap:16px}label{font-size:12px;font-weight:bold;color:#50615c}input,select{display:block;width:100%;padding:13px;border:1px solid #dce5df;border-radius:8px;margin-top:7px;font:inherit;background:#fff}button,.btn{background:var(--green);color:white;border:0;border-radius:8px;padding:13px 18px;font:inherit;font-weight:bold;cursor:pointer;text-decoration:none;display:inline-block}.danger{background:#a8473c}.secondary{background:#e7f1ed;color:var(--green)}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:25px;padding:25px 5px}.steps b{color:#83a99a}.steps p,.muted{color:var(--muted);font-size:13px;line-height:1.6}.auth{max-width:430px;margin:50px auto}.row{display:flex;align-items:center;justify-content:space-between;gap:15px}.tag{background:#e7f1ed;color:var(--green);border-radius:20px;padding:5px 10px;font-size:11px}.alert{padding:13px 17px;border-radius:8px;margin-bottom:12px}.success{background:#e5f4e9;color:#24603c}.warning{background:#fff3d9;color:#805a13}.alert.danger{background:#fae7e4;color:#9b382c}.navlinks{display:flex;align-items:center;gap:5px;flex-wrap:wrap}.navlinks a{margin-left:8px;padding:9px 11px;border-radius:8px}.navlinks a:hover{background:#e7f1ed}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0}.stat{background:white;border:1px solid var(--line);border-radius:13px;padding:20px}.stat strong{display:block;font-size:28px;margin-top:8px}.calendar{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px}.day{min-height:78px;background:white;border:1px solid var(--line);border-radius:10px;padding:9px;font-size:13px}.day.booked{background:#fff0ed;border-color:#efb4aa}.day.full{background:#f8d9d4;border-color:#dc8b80}.day.empty{background:transparent;border:0}.day .count{display:block;margin-top:8px;font-size:10px;color:var(--muted)}.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted)}.dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px}.search-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}@media(max-width:720px){.stats{grid-template-columns:1fr}.search-grid{grid-template-columns:1fr}.day{min-height:60px;padding:5px;font-size:11px}.navlinks a{font-size:12px;margin-left:0;padding:7px}}table{width:100%;border-collapse:collapse;font-size:13px}td,th{text-align:left;padding:12px;border-bottom:1px solid var(--line)}th{color:var(--muted)}@media(max-width:720px){.hero{padding:28px 20px}.hero h1,h1{font-size:34px}.orb{width:110px;height:110px;font-size:42px}.formgrid{grid-template-columns:1fr 1fr}.formgrid button{grid-column:1/-1}.steps{grid-template-columns:1fr}.row{align-items:flex-start}main{margin:20px auto}}
</style></head><body><nav><a class="logo" href="/">✦ StaySwift</a><div class="navlinks">{% if u %}<a href="/dashboard">Dashboard</a><a href="/find-room">Find a Room</a><a href="/calendar">Calendar</a>{% if u['role']=='admin' %}<a href="/admin">Admin</a>{% endif %}<a href="/logout">Log out</a>{% else %}<a href="/find-room">Find a Room</a><a href="/calendar">Calendar</a><a href="/login">Log in</a><a href="/register">Create account</a>{% endif %}</div></nav><main>{% for cat,msg in get_flashed_messages(with_categories=true) %}<div class="alert {{cat}}">{{msg}}</div>{% endfor %}{{body|safe}}</main><footer>StaySwift · Simple stays, smarter reservations</footer></body></html>'''

def page(body, **kw): return render_template_string(BASE,body=render_template_string(body,**kw),u=current_user())
def db():
 c=sqlite3.connect(DB,timeout=20); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init_db():
 with db() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT,email TEXT UNIQUE,password TEXT,role TEXT DEFAULT 'guest');CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY,number TEXT UNIQUE,kind TEXT,price REAL,active INTEGER DEFAULT 1);CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY,user_id INTEGER,room_id INTEGER,checkin TEXT,checkout TEXT,status TEXT DEFAULT 'confirmed',created TEXT);CREATE TABLE IF NOT EXISTS waiting(id INTEGER PRIMARY KEY,user_id INTEGER,kind TEXT,checkin TEXT,checkout TEXT,status TEXT DEFAULT 'waiting',created TEXT);CREATE TABLE IF NOT EXISTS offers(id INTEGER PRIMARY KEY,waiting_id INTEGER,room_id INTEGER,token TEXT UNIQUE,status TEXT DEFAULT 'open',created TEXT);''')
  if not c.execute("SELECT 1 FROM users WHERE role='admin'").fetchone(): c.execute("INSERT INTO users(name,email,password,role) VALUES('Hotel Admin','admin@hotel.test','Admin123!','admin')")
  if not c.execute('SELECT 1 FROM rooms').fetchone(): c.executemany('INSERT INTO rooms(number,kind,price) VALUES(?,?,?)',[('101','Standard',1800),('102','Standard',1800),('201','Deluxe',2800),('202','Deluxe',2800),('301','Suite',4500)])
def current_user():
 if not session.get('uid'): return None
 with db() as c: return c.execute('SELECT * FROM users WHERE id=?',(session['uid'],)).fetchone()
def login_required(f):
 @wraps(f)
 def w(*a,**k):
  if not current_user(): flash('Please log in first.','warning'); return redirect('/login')
  return f(*a,**k)
 return w
def admin_required(f):
 @wraps(f)
 def w(*a,**k):
  u=current_user()
  if not u or u['role']!='admin': abort(403)
  return f(*a,**k)
 return w
def valid_dates(a,b):
 try: return date.fromisoformat(a)>=date.today() and date.fromisoformat(b)>date.fromisoformat(a)
 except: return False
def free_room(c,kind,a,b):
 return c.execute("SELECT * FROM rooms r WHERE active=1 AND kind=? AND NOT EXISTS(SELECT 1 FROM bookings x WHERE x.room_id=r.id AND x.status='confirmed' AND x.checkin<? AND x.checkout>?) ORDER BY number LIMIT 1",(kind,b,a)).fetchone()
def send_email(to,subject,body):
 host=os.getenv('SMTP_HOST')
 if not host: print('\nEMAIL PREVIEW\nTO:',to,'\nSUBJECT:',subject,'\n',body); return
 m=EmailMessage(); m['To']=to; m['From']=os.getenv('SMTP_FROM',os.getenv('SMTP_USER')); m['Subject']=subject; m.set_content(body)
 with smtplib.SMTP(host,int(os.getenv('SMTP_PORT','587'))) as s: s.starttls(); s.login(os.getenv('SMTP_USER'),os.getenv('SMTP_PASSWORD')); s.send_message(m)
def notify(room):
 with db() as c:
  people=c.execute("SELECT w.*,u.name,u.email FROM waiting w JOIN users u ON u.id=w.user_id WHERE w.status='waiting' AND w.kind=? AND NOT EXISTS(SELECT 1 FROM bookings b WHERE b.room_id=? AND b.status='confirmed' AND b.checkin<w.checkout AND b.checkout>w.checkin) ORDER BY w.created,w.id",(room['kind'],room['id'])).fetchall()
  for p in people:
   token=secrets.token_urlsafe(32); c.execute('INSERT INTO offers(waiting_id,room_id,token,created) VALUES(?,?,?,?)',(p['id'],room['id'],token,datetime.utcnow().isoformat()))
   link=request.url_root.rstrip('/')+url_for('claim',token=token)
   try: send_email(p['email'],'A room is available — claim it now!',f"Hi {p['name']}, a {room['kind']} room is available for {p['checkin']} to {p['checkout']}. First successful claim wins. Claim here: {link}")
   except Exception as e: app.logger.error('Email failed: %s',e)

@app.route('/')
def home():
 with db() as c: kinds=c.execute('SELECT kind,MIN(price) price FROM rooms WHERE active=1 GROUP BY kind').fetchall()
 body='''<section class="hero"><div><span class="eyebrow">WELCOME TO STAYSWIFT</span><h1>Your next stay,<br><i>made simple.</i></h1><p>Reserve a room, or join the waiting list and get notified when a room opens.</p></div><div class="orb">✦<small>REST EASY<br>STAY HAPPY</small></div></section><section class="panel"><span class="eyebrow">PLAN YOUR VISIT</span><h2>Find a room</h2><form action="/book" method="post" class="formgrid"><label>Room type<select name="kind">{% for k in kinds %}<option value="{{k['kind']}}">{{k['kind']}} · from ₱{{k['price']}}</option>{% endfor %}</select></label><label>Check-in<input name="checkin" type="date" required></label><label>Check-out<input name="checkout" type="date" required></label><button>Check availability →</button></form></section><section class="steps"><div><b>01</b><h3>Choose dates</h3><p>Search your preferred room and dates.</p></div><div><b>02</b><h3>Reserve or wait</h3><p>If full, join the waiting list.</p></div><div><b>03</b><h3>Claim it first</h3><p>Get an email when a room opens.</p></div></section>'''
 # Strip price decoration from submitted kind by using option value separately below in template correction
 body=body.replace('<option>{{k[\'kind\']}} · from ₱{{k[\'price\']}}</option>','<option value="{{k[\'kind\']}}">{{k[\'kind\']}} · from ₱{{k[\'price\']}}</option>')
 return page(body,kinds=kinds)
@app.route('/register',methods=['GET','POST'])
def register():
 if request.method=='POST':
  try:
   with db() as c: c.execute('INSERT INTO users(name,email,password) VALUES(?,?,?)',(request.form['name'],request.form['email'].lower(),request.form['password']))
   flash('Account created. Please log in.','success'); return redirect('/login')
  except sqlite3.IntegrityError: flash('Email already registered.','danger')
 return page('''<section class="panel auth"><span class="eyebrow">JOIN STAYSWIFT</span><h1>Create account</h1><form method="post" class="stack"><label>Full name<input name="name" required></label><label>Email<input name="email" type="email" required></label><label>Password<input name="password" type="password" minlength="6" required></label><button>Create account</button></form></section>''')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  with db() as c: u=c.execute('SELECT * FROM users WHERE email=? AND password=?',(request.form['email'].lower(),request.form['password'])).fetchone()
  if u: session.clear(); session['uid']=u['id']; return redirect('/admin' if u['role']=='admin' else '/dashboard')
  flash('Invalid email or password.','danger')
 return page('''<section class="panel auth"><span class="eyebrow">WELCOME BACK</span><h1>Log in</h1><form method="post" class="stack"><label>Email<input name="email" type="email" required></label><label>Password<input name="password" type="password" required></label><button>Log in</button></form></section>''')
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
@app.route('/find-room', methods=['GET', 'POST'])
def find_room():
    with db() as c:
        kinds = c.execute('SELECT kind, MIN(price) price FROM rooms WHERE active=1 GROUP BY kind ORDER BY kind').fetchall()
    results = []
    checkin = request.values.get('checkin', '')
    checkout = request.values.get('checkout', '')
    kind = request.values.get('kind', '')
    searched = request.method == 'POST' or bool(checkin or checkout or kind)
    if searched:
        if not kind or not valid_dates(checkin, checkout):
            flash('Choose a room type and valid future check-in/check-out dates.', 'warning')
        else:
            with db() as c:
                results = c.execute("SELECT r.* FROM rooms r WHERE r.active=1 AND r.kind=? AND NOT EXISTS (SELECT 1 FROM bookings b WHERE b.room_id=r.id AND b.status='confirmed' AND b.checkin < ? AND b.checkout > ?) ORDER BY r.number", (kind, checkout, checkin)).fetchall()
    body = '''<span class="eyebrow">PLAN YOUR STAY</span><h1>Find a room</h1>
    <p class="muted">Choose your dates to see rooms that are available for the entire stay.</p>
    <section class="panel"><form method="post" class="search-grid">
      <label>Room type<select name="kind" required><option value="">Choose room type</option>{% for k in kinds %}<option value="{{k['kind']}}" {% if kind==k['kind'] %}selected{% endif %}>{{k['kind']}} · from ₱{{'%.2f'|format(k['price'])}}</option>{% endfor %}</select></label>
      <label>Check-in<input type="date" name="checkin" value="{{checkin}}" required></label>
      <label>Check-out<input type="date" name="checkout" value="{{checkout}}" required></label>
      <button style="grid-column:1/-1">Search available rooms</button></form></section>
    {% if searched and checkin and checkout and kind and valid %}
      <h2>Search results</h2>{% if results %}<p class="muted">{{results|length}} room(s) available.</p>
      {% for r in results %}<section class="panel row"><div><span class="tag">Available</span><h3>{{kind}} · Room {{r['number']}}</h3><p>₱{{'%.2f'|format(r['price'])}} per night</p></div>
      <form method="post" action="/book"><input type="hidden" name="kind" value="{{kind}}"><input type="hidden" name="checkin" value="{{checkin}}"><input type="hidden" name="checkout" value="{{checkout}}"><button>Book this room</button></form></section>{% endfor %}
      {% else %}<section class="panel"><h3>No rooms available for those dates.</h3><p class="muted">You can join the waiting list by submitting the booking request below.</p>
      <form method="post" action="/book"><input type="hidden" name="kind" value="{{kind}}"><input type="hidden" name="checkin" value="{{checkin}}"><input type="hidden" name="checkout" value="{{checkout}}"><button>Join waiting list</button></form></section>{% endif %}
    {% endif %}'''
    return page(body, kinds=kinds, results=results, checkin=checkin, checkout=checkout, kind=kind, searched=searched, valid=bool(kind and valid_dates(checkin, checkout)))

@app.route('/calendar')
def booking_calendar():
    today = date.today()
    try:
        year = int(request.args.get('year', today.year))
        month = int(request.args.get('month', today.month))
        if month < 1 or month > 12: raise ValueError
        first = date(year, month, 1)
    except (ValueError, TypeError):
        first = date(today.year, today.month, 1)
        year, month = first.year, first.month
    weeks = calendar.monthcalendar(year, month)
    total_days = calendar.monthrange(year, month)[1]
    with db() as c:
        room_total = c.execute('SELECT COUNT(*) FROM rooms WHERE active=1').fetchone()[0]
        bookings = c.execute("SELECT checkin, checkout, COUNT(DISTINCT room_id) AS booked FROM bookings WHERE status='confirmed' AND checkin < ? AND checkout > ? GROUP BY checkin, checkout", (f'{year+1:04d}-01-01', f'{year:04d}-01-01')).fetchall()
        active_bookings = c.execute("SELECT checkin,checkout,room_id FROM bookings WHERE status='confirmed' AND checkin < ? AND checkout > ?", (f'{year+1:04d}-01-01', f'{year:04d}-01-01')).fetchall()
    day_counts = {}
    for d in range(1, total_days + 1):
        target = date(year, month, d).isoformat()
        day_counts[d] = len({b['room_id'] for b in active_bookings if b['checkin'] <= target < b['checkout']})
    prev_month = 12 if month == 1 else month - 1
    prev_year = year - 1 if month == 1 else year
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year
    body = '''<span class="eyebrow">ROOM AVAILABILITY</span><h1>Booking Calendar</h1>
    <p class="muted">A date is marked booked when at least one room has a reservation. Fully booked means every active room is occupied for that date.</p>
    <section class="panel"><div class="row"><a class="btn secondary" href="{{url_for('booking_calendar',year=py,month=pm)}}">← Previous</a><h2>{{month_name}} {{year}}</h2><a class="btn secondary" href="{{url_for('booking_calendar',year=ny,month=nm)}}">Next →</a></div>
    <div class="legend" style="margin:18px 0"><span><i class="dot" style="background:#fff0ed;border:1px solid #efb4aa"></i>Has booking</span><span><i class="dot" style="background:#f8d9d4;border:1px solid #dc8b80"></i>Fully booked</span><span><i class="dot" style="background:#fff;border:1px solid #e4eae5"></i>Available</span></div>
    <div class="calendar">{% for wd in weekdays %}<div class="muted" style="text-align:center;font-weight:bold">{{wd}}</div>{% endfor %}
    {% for week in weeks %}{% for day in week %}{% if day==0 %}<div class="day empty"></div>{% else %}{% set count=counts[day] %}<div class="day {% if room_total and count>=room_total %}full{% elif count>0 %}booked{% endif %}"><strong>{{day}}</strong><span class="count">{% if room_total and count>=room_total %}Fully booked{% elif count>0 %}{{count}} room(s) booked{% else %}Available{% endif %}</span></div>{% endif %}{% endfor %}{% endfor %}</div>
    <p class="muted" style="margin-top:16px">Active rooms: {{room_total}}. Calendar data comes from confirmed reservations.</p></section>'''
    return page(body, py=prev_year, pm=prev_month, ny=next_year, nm=next_month, year=year, month_name=calendar.month_name[month], weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], weeks=weeks, counts=day_counts, room_total=room_total)

@app.route('/book',methods=['POST'])
@login_required
def book():
 a,b,k=request.form['checkin'],request.form['checkout'],request.form['kind']
 if not valid_dates(a,b): flash('Choose valid future dates.','danger'); return redirect('/')
 u=current_user()
 with db() as c:
  r=free_room(c,k,a,b)
  if r: c.execute('INSERT INTO bookings(user_id,room_id,checkin,checkout,created) VALUES(?,?,?,?,?)',(u['id'],r['id'],a,b,datetime.utcnow().isoformat())); flash('Reservation confirmed! Room '+r['number'],'success')
  else: c.execute('INSERT INTO waiting(user_id,kind,checkin,checkout,created) VALUES(?,?,?,?,?)',(u['id'],k,a,b,datetime.utcnow().isoformat())); flash('Fully booked. You have joined the waiting list.','warning')
 return redirect('/dashboard')
@app.route('/dashboard')
@login_required
def dashboard():
    u = current_user()
    with db() as c:
        bs = c.execute('SELECT b.*,r.number,r.kind,r.price FROM bookings b JOIN rooms r ON r.id=b.room_id WHERE b.user_id=? ORDER BY b.id DESC', (u['id'],)).fetchall()
        ws = c.execute('SELECT * FROM waiting WHERE user_id=? ORDER BY id DESC', (u['id'],)).fetchall()
        available = c.execute("SELECT COUNT(*) FROM rooms WHERE active=1").fetchone()[0]
        confirmed = c.execute("SELECT COUNT(*) FROM bookings WHERE user_id=? AND status='confirmed'", (u['id'],)).fetchone()[0]
        waiting_count = c.execute("SELECT COUNT(*) FROM waiting WHERE user_id=? AND status='waiting'", (u['id'],)).fetchone()[0]
    body = '''<span class="eyebrow">GUEST OVERVIEW</span><h1>Welcome back, {{u['name']}}.</h1><p class="muted">Manage your stays and discover your next room.</p>
    <div class="stats"><div class="stat"><span class="muted">Active hotel rooms</span><strong>{{available}}</strong></div><div class="stat"><span class="muted">Your confirmed bookings</span><strong>{{confirmed}}</strong></div><div class="stat"><span class="muted">Waiting-list requests</span><strong>{{waiting_count}}</strong></div></div>
    <section class="panel"><div class="row"><div><h2>Find your next stay</h2><p class="muted">Search room availability or check the hotel calendar.</p></div><a class="btn" href="/find-room">Find a Room →</a></div><a class="btn secondary" href="/calendar">View Booking Calendar</a></section>
    <h2>My reservations</h2>{% for b in bs %}<section class="panel row"><div><span class="tag">{{b['status']}}</span><h3>{{b['kind']}} · Room {{b['number']}}</h3><p>{{b['checkin']}} → {{b['checkout']}}</p></div>{% if b['status']=='confirmed' %}<form method="post" action="/cancel/{{b['id']}}"><button class="danger">Cancel</button></form>{% endif %}</section>{% else %}<section class="panel"><p>You don't have any reservations yet. <a href="/find-room">Find a room</a> to get started.</p></section>{% endfor %}
    <h2>My waiting-list requests</h2>{% for w in ws %}<section class="panel"><span class="tag">{{w['status']}}</span><h3>{{w['kind']}} room</h3><p>{{w['checkin']}} → {{w['checkout']}}</p></section>{% else %}<p class="muted">You are not on a waiting list.</p>{% endfor %}'''
    return page(body, u=u, bs=bs, ws=ws, available=available, confirmed=confirmed, waiting_count=waiting_count)
@app.route('/cancel/<int:bid>',methods=['POST'])
@login_required
def cancel(bid):
 u=current_user()
 with db() as c: r=c.execute('SELECT b.*,rm.* FROM bookings b JOIN rooms rm ON rm.id=b.room_id WHERE b.id=? AND b.user_id=? AND b.status=\'confirmed\'',(bid,u['id'])).fetchone(); c.execute("UPDATE bookings SET status='cancelled' WHERE id=?",(bid,)) if r else None
 if r: notify(dict(r)); flash('Cancelled. Matching waiting-list guests are being notified.','success')
 return redirect('/dashboard')
@app.route('/claim/<token>')
def claim(token):
 c=db()
 try:
  c.execute('BEGIN IMMEDIATE'); o=c.execute('SELECT o.*,w.user_id,w.kind,w.checkin,w.checkout,w.status wstatus,rm.number FROM offers o JOIN waiting w ON w.id=o.waiting_id JOIN rooms rm ON rm.id=o.room_id WHERE o.token=?',(token,)).fetchone()
  if not o or o['status']!='open' or o['wstatus']!='waiting': c.rollback(); return page('<section class="panel auth"><h1>Offer unavailable</h1><p>This offer is no longer available. Someone may have claimed it first.</p></section>')
  conflict=c.execute("SELECT 1 FROM bookings WHERE room_id=? AND status='confirmed' AND checkin<? AND checkout>?",(o['room_id'],o['checkout'],o['checkin'])).fetchone()
  if conflict: c.execute("UPDATE offers SET status='taken' WHERE room_id=? AND status='open'",(o['room_id'],)); c.commit(); return page('<section class="panel auth"><h1>Offer unavailable</h1><p>Someone else claimed the room first.</p></section>')
  c.execute('INSERT INTO bookings(user_id,room_id,checkin,checkout,created) VALUES(?,?,?,?,?)',(o['user_id'],o['room_id'],o['checkin'],o['checkout'],datetime.utcnow().isoformat())); c.execute("UPDATE offers SET status='taken' WHERE room_id=? AND status='open'",(o['room_id'],)); c.execute("UPDATE waiting SET status='fulfilled' WHERE id=?",(o['waiting_id'],)); c.commit()
  return page(f'<section class="panel auth"><h1>Room claimed!</h1><p>Congratulations! Room {o["number"]} is reserved for you.</p><a class="btn" href="/dashboard">Go to my bookings</a></section>')
 finally: c.close()
@app.route('/admin')
@admin_required
def admin():
 with db() as c:
  rooms=c.execute('SELECT * FROM rooms ORDER BY kind,number').fetchall(); bs=c.execute('SELECT b.*,u.name,u.email,r.number,r.kind FROM bookings b JOIN users u ON u.id=b.user_id JOIN rooms r ON r.id=b.room_id ORDER BY b.id DESC').fetchall(); ws=c.execute('SELECT w.*,u.name,u.email FROM waiting w JOIN users u ON u.id=w.user_id ORDER BY w.id DESC').fetchall()
 body='''<h1>Hotel admin</h1><section class="panel"><h2>Add room</h2><form class="formgrid" method="post" action="/admin/add"><label>Room number<input name="number" required></label><label>Room type<input name="kind" required></label><label>Price/night<input name="price" type="number" min="1" step=".01" required></label><button>Add room</button></form></section><h2>Rooms</h2><section class="panel">{% for r in rooms %}<p>Room {{r['number']}} · {{r['kind']}} · ₱{{r['price']}}</p>{% endfor %}</section><h2>Reservations</h2><section class="panel"><table><tr><th>Guest</th><th>Room</th><th>Dates</th><th>Status</th><th></th></tr>{% for b in bs %}<tr><td>{{b['name']}}<br>{{b['email']}}</td><td>{{b['kind']}} {{b['number']}}</td><td>{{b['checkin']}}–{{b['checkout']}}</td><td>{{b['status']}}</td><td>{% if b['status']=='confirmed' %}<form method="post" action="/admin/cancel/{{b['id']}}"><button class="danger">Cancel</button></form>{% endif %}</td></tr>{% endfor %}</table></section><h2>Waiting list</h2><section class="panel">{% for w in ws %}<p>{{w['name']}} · {{w['kind']}} · {{w['checkin']}}–{{w['checkout']}} · {{w['status']}}</p>{% endfor %}</section>'''
 return page(body,rooms=rooms,bs=bs,ws=ws)
@app.route('/admin/add',methods=['POST'])
@admin_required
def add_room():
 try:
  with db() as c: c.execute('INSERT INTO rooms(number,kind,price) VALUES(?,?,?)',(request.form['number'],request.form['kind'],float(request.form['price'])))
  flash('Room added.','success')
 except: flash('Could not add room. Check for duplicate room number or invalid price.','danger')
 return redirect('/admin')
@app.route('/admin/cancel/<int:bid>',methods=['POST'])
@admin_required
def admin_cancel(bid):
 with db() as c: r=c.execute('SELECT b.*,rm.* FROM bookings b JOIN rooms rm ON rm.id=b.room_id WHERE b.id=? AND b.status=\'confirmed\'',(bid,)).fetchone(); c.execute("UPDATE bookings SET status='cancelled' WHERE id=?",(bid,)) if r else None
 if r: notify(dict(r)); flash('Cancelled; waitlist emails triggered.','success')
 return redirect('/admin')
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
