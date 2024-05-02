import os

from flask import Flask
from email.message import EmailMessage

import ssl
import smtplib

from dotenv import load_dotenv
from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify,Response
)
from flask_cors import CORS,cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
import random
import re

email_sender = 'kvizpzm@gmail.com'
email_password = os.environ.get('SIFRAMEJL')
email_reciever = ''
subject = 'VERIFIKACIJA'
body = """

"""

trenutniUserID = None
jelUlogovan = None
otpBr = 000000
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, origins={'http://localhost:5173'}, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    @app.route('/')
    def home():
        return 'OVO JE <h1>POCETNA STRANICA</h1>'

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/register', methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def register():
        global trenutniUserID,email_reciever
        data = request.json
        email = data.get('email')
        email_reciever = email
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        
        
        # Da li se sifre podudaraju
        if password != confirmPassword:
            return jsonify({'message': 'Passwords do not match'}), 400
        
        if check(email)==False:
            return jsonify({'message': 'Unet email nije tacan'}), 400
            # Provera da li je user vec registrovan
        db = get_db()
        user = db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone()
        if user is not None:
            return jsonify({'message': 'Email already registered'}), 400

        # ubacivanje usera u bazu
        user = db.execute(
            'INSERT INTO user (email, password,verifikacija) VALUES (?, ?, ?)',
            (email, generate_password_hash(password),'false')
        )
        db.commit()
        trenutniUserID = user.lastrowid
        return jsonify({'message': 'Registration successful','userAIDI':user.lastrowid}), 200
        

    @app.route('/login',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def login():
        global email_reciever
        if request.method == 'POST':
            data = request.json
            email = data.get('email')
            password = data.get('password')
            email_reciever = email

            db = get_db()
            error = None

            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)
            ).fetchone()


            if user is None:
                error = 'Incorrect email.'
                return jsonify({'message': 'Incorrect email'}), 400
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
                return jsonify({'message': 'Incorrect password'}), 400
            

            if error is None:
                jelUlogovan = db.execute(
            'SELECT idLog FROM logovan WHERE idSesije = ?', (user['id'],)
        )   .fetchone()

                if jelUlogovan is None:
                    userLogovan = db.execute(
                    'INSERT INTO logovan (trenutnaSesija, idSesije) VALUES (?, ?)',
                    ('true',user['id'])
                    )
                    db.commit()
                        
                    return jsonify({'message': 'Login successful','userAIDI':user['id']}), 200
                elif jelUlogovan is not None:
                    userLogovan = db.execute(
                    'UPDATE logovan SET trenutnaSesija = ? WHERE idSesije=?',
                    ('true',user['id'])
                    )

                    db.commit()
                        
                    return jsonify({'message': 'Login successful','userAIDI':user['id']}), 200
                    

    @app.route('/ulogovan',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def ulogovan():
        db = get_db()
        jelUlogovan = db.execute(
            'SELECT idLog FROM logovan WHERE trenutnaSesija = ?', ('true',)
        ).fetchone()
        if jelUlogovan is None:
            return jsonify({'message': 'nije'}), 200
        elif jelUlogovan is not None:
            return jsonify({'message': 'jeste'}), 200
    
    @app.route('/logout',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def logout():
        db = get_db()
        jelUlogovan = db.execute(
            'SELECT idLog FROM logovan WHERE trenutnaSesija = ?', ('true',)
        ).fetchone()

        if jelUlogovan is None:
            return jsonify({'message': 'nije'}), 200
        elif jelUlogovan is not None:
            db.execute(
                'UPDATE logovan SET trenutnaSesija = ?',
                ('false',)
            )
            db.commit()
            return jsonify({'message': 'izlogovan'}), 200

    
    @app.route('/saljiMail',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def saljiMail():
        if request.method == 'POST':
            global otpBr,body,email_sender,email_reciever,subject
            otpBr = random.randint(000000,999999)
            body = 'Tvoj verifikacioni OTP kod je : '+str(otpBr)
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_reciever
            em['subject'] = subject
            em.set_content(body)
            print(em.as_string())
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_reciever,em.as_string())
            
            return jsonify({'messageEM':'poslat mail'}),200
        
    @app.route('/proveriVerifikaciju',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def proveriVerifikaciju():
        if request.method == 'POST':
            data = request.json
            userid = data.get('uID')
            db = get_db()
            jelVerifikovan = db.execute(
                'SELECT * FROM user WHERE id=?',(userid)
            ).fetchone()

            if jelVerifikovan is None:
                return jsonify({'messagePV':'nijeUlogovan'}),200

            elif jelVerifikovan is not None:
                if jelVerifikovan['verifikacija'] == 'false':
                    return jsonify({'messagePV':'nijeVerifikovan'}),200
                else:
                    return jsonify({'messagePV':'jesteVerifikovan'}),200

    @app.route('/verifikacija',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def verifikacija():
        global otpBr
        if request.method == 'POST':
            data = request.json
            otpBr1 = data.get('otpInput')
            userid = data.get('uID')

            db = get_db()
            error = None


            if str(otpBr) == otpBr1:
                db.execute(
                'UPDATE user SET verifikacija=? WHERE id=?',('true',userid)
                )
                db.commit()
                return jsonify({'messageV':'verifikovan'}),200
            else:
                return jsonify({'messageV':'Pogresan OTP kod'}),400


    
    return app