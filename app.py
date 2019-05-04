import pusher
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'


pusher_client = pusher.Pusher(
  app_id='775522',
  key='62f6af6c38e1d298e1b4',
  secret='07ba9120bd2e9e9c508e',
  cluster='mt1',
  ssl=True
)

db = SQLAlchemy(app)

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	message = db.Column(db.String(500))

@app.route('/')
def index():
	
	messages = Message.query.all()
	return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
	try:
		username = request.form.get('username')
		message = request.form.get('message')

		new_message=Message(username=username, message=message)
		db.session.add(new_message)
		db.session.commit()

		pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})

		return jsonify({'result': 'success'})
	except:
		return jsonify({'result':'failure'})
if __name__ == '__main__':
	app.run(debug=True)


