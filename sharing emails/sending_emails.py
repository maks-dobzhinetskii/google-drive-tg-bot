import smtplib


def send_email(receivers, link):
    sender = 'dobzhynetskyy.maksym@chnu.edu.ua'
    receivers = [receivers]
    password = '20082002maks'

    message = f"""From: From Person dobzhynetskyy.maksym@chnu.edu.ua
    To: To Person {receivers}
    Subject: SMTP e-mail test

    Link: {link}
    """

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receivers, message)         
