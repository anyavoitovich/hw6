#import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_database_user:your_database_password@localhost/your_database_name'  # Используйте свою базу данных
app.config['SECRET_KEY'] = '123'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = 'user'

        new_user = User(username=username, password=password, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('greeting'))

    return render_template('login.html')


@app.route('/greeting')
@login_required
def dashboard():
    return f"Hello, {current_user.username}!"


@app.route('/registration_success')
def registration_success():
    return "Registration successful!"

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_token()
            user.password = token
            db.session.commit()

            send_reset_email(email, token)

            flash('Password reset link has been sent to your email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('No user with this email was found.', 'danger')

    return render_template('reset_password.html')


def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


def send_reset_email(email, token):
    msg = Message('Password reset', sender='noreply@example.com', recipients=[email])
    msg.body = f'To reset your password, please follow the link: {url_for("reset_with_token", token=token, _external=True)}'
    mail.send(msg)

@app.route('/reset_with_token/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    user = User.query.filter_by(password=token).first()

    if not user:
        flash('Invalid token.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        user.password = new_password
        db.session.commit()

        flash('Password successfully reset.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_with_token.html', token=token)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)













