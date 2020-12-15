from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

class Item(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	title = database.Column(database.String(100), nullable = False)
	price = database.Column(database.Integer, nullable = False)
	isActive = database.Column(database.Boolean, default = True)
	text = database.Column(database.Text, default = "",nullable = False)

	def __repr__(self):
		return self.title

@app.route('/')
def index():
	items = Item.query.order_by(Item.price).all()
	return render_template('index.html', items=items)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/create', methods=['GET', 'POST'])
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


if __name__ == "__main__":
	app.run(debug=True)

