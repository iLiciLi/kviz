import os

from flask import Flask
from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify,Response
)
from flask_cors import CORS,cross_origin
from werkzeug.security import check_password_hash, generate_password_hash

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
        db.execute(
            'INSERT INTO user (email, password,verifikacija) VALUES (?, ?, ?)',
            (email, generate_password_hash(password),'nije verifikovan')
        )
        db.commit()

        return jsonify({'message': 'Registration successful'}), 200

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
                session.clear()
                session['user_id'] = user['id']
                #fali cuvanje sesije za user-a to jest da se zna da li je user logged in ili nije, posto i dalje moze da se loguje iako smo ulogovani
                return jsonify({'message': 'Login successful'}), 200


    #@app.before_request
    #def load_logged_in_user():
        #@app.route('/logout')
        #def logout():
            #pass

    
    return app