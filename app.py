from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from main import main
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

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

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already exists. Please use a different email.', 'error')
        return redirect(url_for('register_form'))

    new_user = User(name=name, email=email)

    db.session.add(new_user)
    db.session.commit()

    flash(f'Registration successful for {email}', 'success')

    return redirect(url_for('home'))

if __name__ == '__main__':
    main()
    app.run(debug=True)
