from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Ticket %r>' % self.id


# Check if the database already exists
with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table(Ticket.__tablename__):
        # Create the tables
        db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_data = request.form['content']
        new_ticket = Ticket(content=new_data)
        try:
            db.session.add(new_ticket)
            db.session.commit()
            return redirect('/')
        except:
            return "Encountered issue adding new ticket"
    else:
        tickets = Ticket.query.order_by(Ticket.date_created).all()
        return render_template('index.html', tickets=tickets)


if __name__ == "__main__":
    app.run(debug=True)
