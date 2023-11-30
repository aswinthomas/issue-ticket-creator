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
        print("DB does not exist, creating...")
        # Create the tables
        db.create_all()
    else:
        print(f"DB already exists")


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
            return "Encountered issue adding new ticket. Create a ticket for it :)"
    else:
        tickets = Ticket.query.order_by(Ticket.date_created).all()
        return render_template('index.html', tickets=tickets)


@app.route('/delete/<int:id>')
def delete(id):
    ticket_to_delete = Ticket.query.get_or_404(id)
    try:
        db.session.delete(ticket_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Encountered issue deleting the ticket. Create a ticket for it :)"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    ticket = Ticket.query.get_or_404(id)
    if request.method == 'POST':
        ticket.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Encountered issue adding new ticket. Create a ticket for it :)"
    else:
        return render_template('update.html', ticket=ticket)


if __name__ == "__main__":
    app.run(debug=True)
