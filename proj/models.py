from flask_login import UserMixin

from proj import database, manager


class Item(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	title = database.Column(database.String(100), nullable = False)
	price = database.Column(database.Integer, nullable = False)
	isActive = database.Column(database.Boolean, default = True)
	text = database.Column(database.Text, default = "",nullable = False)

	def __repr__(self):
		return self.title


class User(database.Model, UserMixin):
	id = database.Column(database.Integer, primary_key = True)
	login = database.Column(database.String(100), nullable = False, unique = True)
	password = database.Column(database.String(100), nullable = False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

