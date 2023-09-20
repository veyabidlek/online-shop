
from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    desc = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return self.title
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    with app.app_context():
        db.create_all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    return render_template('buy.html', item_id=id)

@app.route('/buy/<int:item_id>/confirm', methods=['POST'])
def item_buy_confirm(item_id):
    email = request.form['email']

    # Create an SMTP connection
    smtp_server = 'smtp.gmail.com'
    port = 587
    email_sender = 'Cristiano@gmail.com'
    email_password = 'Ronaldo1985'

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email_sender, email_password)

        # Create an email message
        subject = 'Order Confirmation'
        body = 'Wait, while we process your order.'
        from_email = email_sender
        to_email = email

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        server.quit()

        return "Order confirmation email sent. Thank you for your purchase!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"



@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        desc = request.form['desc']
        item = Item(title=title, price=price,desc=desc)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"
    else:
        return render_template('create.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

