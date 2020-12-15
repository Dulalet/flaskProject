from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from proj import app, database
from proj.models import Item, User


@app.route('/')
def index():
	items = Item.query.order_by(Item.price).all()
	return render_template('index.html', items=items)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	if request.method == "POST":
		title = request.form['title']
		price = request.form['price']
		text = request.form['text']

		item = Item(title=title, price=price, text=text)

		try:
			database.session.add(item)
			database.session.commit()
			return redirect('/')
		except:
			return("error adding item")

	return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')

		if login and password:
			user = User.query.filter_by(login=login).first()

			if user and check_password_hash(user.password, password):
				login_user(user)

				next_page = request.args.get('next')

				if next_page == None:
					return redirect('/')

				return redirect(next_page)
			else:
				flash('Incorrect username or password')
		else:
			flash('Please fill in both fields')

	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	login = request.form.get('login')
	password = request.form.get('password')
	password2 = request.form.get('password2')

	if request.method == 'POST':
		if not (login or password):
			flash('Please, fill all fields!')
		elif password != password2:
			flash('Passwords are not equal!')
		else:
			hash_pwd = generate_password_hash(password)
			new_user = User(login=login, password=hash_pwd)
			database.session.add(new_user)
			database.session.commit()

			return redirect(url_for('login_page'))

	return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
	if response.status_code == 401:
		return redirect(url_for('login_page') + '?next=' + request.url)

	return response


