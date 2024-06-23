from flask import Flask, render_template, redirect, url_for, request, flash
import csv
from main import main
import time
app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

    flash(f"წარმატებულად დარეგისტრირდა {email}")

    return redirect(url_for('home'))


if __name__ == '__main__':
    main()
    app.run(debug=True)
