import os

from flask import Flask
from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify,Response
)
from flask_cors import CORS,cross_origin
from werkzeug.security import check_password_hash, generate_password_hash

#user = None
jelUlogovan = None

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, origins={'http://localhost:5173'}, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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
        data = request.json
        email = data.get('email')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        
        
        # Da li se sifre podudaraju
        if password != confirmPassword:
            return jsonify({'message': 'Passwords do not match'}), 400

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
        return jsonify({'message': 'Registration successful','userAIDI':user.lastrowid}), 200

    @app.route('/login',methods=['GET','POST'])
    @cross_origin(supports_credentials=True)
    def login():
        if request.method == 'POST':
            data = request.json
            email = data.get('email')
            password = data.get('password')

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
                        
                    return jsonify({'message': 'Login successful','userAIDI':userLogovan.lastrowid}), 200
                elif jelUlogovan is not None:
                    userLogovan = db.execute(
                    'UPDATE logovan SET trenutnaSesija = ? WHERE idSesije=?',
                    ('true',user['id'])
                    )

                    db.commit()
                        
                    return jsonify({'message': 'Login successful','userAIDI':userLogovan.lastrowid}), 200
                    

    
    
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
            redirect(url_for('/ulogovan'))
        elif jelUlogovan is not None:
            db.execute(
                'UPDATE logovan SET trenutnaSesija = ?',
                ('false',)
            )
            db.commit()
            return jsonify({'message': 'izlogovan'}), 200
    
    return app