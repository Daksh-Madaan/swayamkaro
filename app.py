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
            mm = int(request.form['mm'])
            mongo.db.app_users.insert_one({'admno': request.form['admno'],
                                           'password': request.form['regPassword'],
                                           'eng': (int(request.form['eng'])/mm)*100,
                                           'maths': (int(request.form['maths'])/mm)*100,
                                           'sci': (int(request.form['sci'])/mm)*100,
                                           'sst': (int(request.form['sst'])/mm)*100,
                                           'lang': (int(request.form['lang'])/mm)*100,
                                           'est': request.form['est'],
                                          'engR': 0,
                                          'mathsR': 0,
                                          'sciR': 0,
                                          'sstR': 0,
                                          'langR': 0})

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


@app.route('/update', methods=['GET','POST'])
def update():
    if 'admno' in session:
        admno = session['admno']
        if request.method == 'POST':
            mm = int(request.form['mm'])
            update = {'eng': (int(request.form['eng'])/mm)*100,
                        'maths': (int(request.form['maths'])/mm)*100,
                        'sci': (int(request.form['sci'])/mm)*100,
                        'sst': (int(request.form['sst'])/mm)*100,
                        'lang': (int(request.form['lang'])/mm)*100,
                        'est':request.form['est']}
            mongo.db.app_users.update_one({'admno': admno},{'$set': update})
            return redirect(url_for('dashboard'))
        
        return render_template('update.html')

    else:
        return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'admno' in session:
        admno = session['admno']
        stm = mongo.db.app_users.find_one({'admno': admno})
        est = int(stm['est'])
        
        st = est-2
        slot1 = 0
        slot3 = 2
        if est <=4:
            st = est-1
            slot3 = 1
            slot1 = math.floor(st*(2/3))
        elif est <= 7:
            
            slot1 = math.floor(st*(2/3))
        else:
            st = est-3
            slot3 = 3
            slot1 = math.floor(st*(3/5))

        slot2 = st - slot1
        if request.method == 'POST':
          update = {'engR': request.form['eng'],
                        'mathsR': request.form['maths'],
                        'sciR': request.form['sci'],
                        'sstR': request.form['sst'],
                        'langR': request.form['lang']}
          print(request.form['lang'])
                    
          mongo.db.app_users.update_one({'admno': admno},{'$set': update})
          return redirect(url_for('dashboard'))
          
          
        subs = {"English": int(stm['eng']), "Maths": int(stm['maths']), "Science": int(stm['sci']),"SST": int(stm['sst']),"Language": int(stm['lang'])}
        priority = sorted(subs, key=lambda i: int(subs[i]))
        engR = stm['engR']
        mathsR = stm['mathsR']
        langR = stm['langR']
        sciR = stm['sciR']
        sstR = stm['sstR']
                                  
        return render_template('dashboard.html', admno=admno, subs=subs, priority=priority, slot1=slot1, slot2=slot2, slot3=slot3, 
                               engR=engR,
                               mathsR=mathsR,
                               langR=langR,
                               sciR=sciR,
                               sstR=sstR)
        
    
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
