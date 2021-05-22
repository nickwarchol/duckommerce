from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Product %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_content = request.form['content']
        new_product = Todo(content=product_content)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your product :( '
    else:
        products = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)