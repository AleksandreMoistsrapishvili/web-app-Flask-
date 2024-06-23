from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Custom Jinja2 options
app.jinja_options = Flask.jinja_options.copy()
app.jinja_options.update({
    'block_start_string': '{%',
    'block_end_string': '%}',
    'variable_start_string': '{{',
    'variable_end_string': '}}',
    'comment_start_string': '{#',
    'comment_end_string': '#}'
})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

with app.app_context():
    db.create_all()

def load_quotes(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        quotes = [row[0] for row in reader]
    return quotes

def load_authors(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        authors = [row[1] for row in reader]
    return authors

def load_tags(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        tags = [row[2] for row in reader]
    return tags

def load_all(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        all_data = [row for row in reader]
    return all_data

@app.route('/')
@app.route('/home')
def home():
    quotes = load_quotes('quotes.csv')
    return render_template('home.html', quotes=quotes)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/authors')
def authors():
    authors = load_authors('quotes.csv')
    return render_template('authors.html', authors=authors)

@app.route('/tags')
def tags():
    tags = load_tags('quotes.csv')
    return render_template('tags.html', tags=tags)

@app.route('/full')
def full():
    all_data = load_all('quotes.csv')
    return render_template('full.html', all_data=all_data)

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already exists. Please use a different email.', 'error')
        return redirect(url_for('register_form'))

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    flash(f'Registration successful for {email}', 'success')

    return redirect(url_for('home'))

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        flash('Login successful', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login failed. Check your email and password.', 'error')
        return redirect(url_for('login_form'))

if __name__ == '__main__':
    app.run(debug=True)
