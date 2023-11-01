from flask import Flask, request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
import math

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'StudentDB'
app.config['MONGO_URI'] = 'mongodb+srv://admin:xwPZ20bmjBBr2kBE@studentdb.xl39sis.mongodb.net/StudentDB?retryWrites=true&w=majority'

app.secret_key = 'stm'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if mongo.db.app_users.find_one({'admno': request.form['admno']}) is None:
            mongo.db.app_users.insert_one({'admno': request.form['admno'],
                                           'password': request.form['regPassword'],
                                           'eng': request.form['eng'],
                                           'maths': request.form['maths'],
                                           'sci': request.form['sci'],
                                           'sst': request.form['sst'],
                                           'lang': request.form['lang'],
                                           'est':request.form['est']})
            return redirect(url_for('login'))
        
        return 'User Already Registered'
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if mongo.db.app_users.find_one({'admno': request.form['admno'], 'password': request.form['loginPassword']}) is not None:
            session['admno'] = request.form['admno']
            return redirect(url_for('dashboard'))
        else:
            return redirect('/login')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'admno' in session:
        admno = session['admno']
        stm = mongo.db.app_users.find_one({'admno': admno})
        est = int(stm['est'])
        timeone = math.floor(est*(2/3))
        timetwo = math.floor(est*(1/3))

        subs = {"English": int(stm['eng']), "Maths": int(stm['maths']), "Science": int(stm['sci']),"SST": int(stm['sst']),"Language": int(stm['lang'])}
        priority = sorted(subs, key=lambda i: int(subs[i]))
        return render_template('dashboard.html', admno=admno, subs=subs, priority=priority, timeone=timeone, timetwo=timetwo)
    
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)