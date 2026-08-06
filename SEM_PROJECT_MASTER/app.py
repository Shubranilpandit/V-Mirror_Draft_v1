import sys 
import os # For handling file paths and system operations
import base64 # For encoding and decoding images in base64 format
import cv2 # OpenCV for image processing
import numpy as np # NumPy for array manipulation

from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ai_engine.pose_detector import PoseDetector
from ai_engine.tryon_engine import TryOnEngine

app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_folder='frontend/static'
)

app.secret_key = "sem2_project_secret"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_folder = os.path.join(os.path.dirname(__file__), "database")
os.makedirs(db_folder, exist_ok=True)

db_path = os.path.join(db_folder, "users.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db = SQLAlchemy(app)

detector = PoseDetector()
engine = TryOnEngine()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'User already exists'}), 400

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Signup successful'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Login successful'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/clothes')
def clothes():
    return jsonify({
        'items': engine.list_clothes()
    })


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()

    frame_b64 = data.get('frame')
    cloth = data.get('cloth', 'shirt1')

    encoded = frame_b64.split(',', 1)[-1]
    frame_data = base64.b64decode(encoded)

    nparr = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    pose_data = detector.detect(frame)
    output_frame = engine.apply_tryon(frame, cloth, pose_data)

    success, buf = cv2.imencode('.jpg', output_frame)

    out_b64 = base64.b64encode(buf).decode('ascii')

    return jsonify({
        'frame': 'data:image/jpeg;base64,' + out_b64
    })


if __name__ == '__main__':
    app.run(debug=True)