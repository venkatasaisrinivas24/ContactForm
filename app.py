from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if using)
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Configuration for Flask-Mail (example with Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Set in .env or your shell
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.form.get('full_name')
        email_address = request.form.get('email_address')
        contact_number = request.form.get('contact_number')
        message = request.form.get('message')

        # Server-side validation: ensure all fields are provided
        if not full_name or not email_address or not contact_number or not message:
            flash('All fields are required!', 'error')
            return redirect(url_for('contact_form'))

        # Prepare the email content
        email_subject = "New Contact Form Submission"
        email_body = f"""
        You have received a new message from your website contact form.

        Full Name: {full_name}
        Email Address: {email_address}
        Contact Number: {contact_number}
        Message: {message}
        """

        try:
            msg = Message(subject=email_subject,
                          recipients=[app.config['MAIL_USERNAME']],  # Sending to your own email
                          body=email_body)
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while sending your message: {str(e)}', 'error')

        return redirect(url_for('contact_form'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
