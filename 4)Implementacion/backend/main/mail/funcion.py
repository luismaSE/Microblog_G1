from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException

def sendMail(to, subject, json_content):
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    try:
        alias = json_content["alias"]

        tema_0 = list(json_content["temas"].keys())[0]
        tema_1 = list(json_content["temas"].keys())[1]
        tema_2 = list(json_content["temas"].keys())[2]

        msg.body = f"Hola {alias} ! \nHay nuevos temas del momento:\n 1º {tema_0} \n 2º {tema_1}\n 3° {tema_2} \n¡Saludos! Microblog Team"

        response = mailsender.send(msg)
        
    except SMTPException as e:
        print(e)
        return "Entrega de correo fallida"
    return True
