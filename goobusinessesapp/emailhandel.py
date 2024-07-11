from goobusinessesapp.models import ControlWeb
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

OurMainURL = "https://goobusines.com/"


def sendEmailFaild(messageText):
    emailReceiver="barmanpari163@gmail.com"
    emailSender = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
    ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
    smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
    subject = f"Website send Email Faild {datetime.now()}"
    body =messageText

    em = EmailMessage()
    em['From'] = emailSender
    em['To'] = emailReceiver
    em['subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as smtp:
        smtp.login(emailSender, ePassword)
        smtp.sendmail(emailSender, emailReceiver, em.as_string())


def sendInterveiwTime(emailReceiver, ivdate, ivtime, meetinglink, candidatename):
    if meetinglink=="":
        meetinglink = "Will be given 10 minutes before the interview."

    if emailReceiver!="":
        emailSender = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        
        body = f"""Dear {candidatename},

I hope this email finds you well.

I am reaching out to inform you that we have reviewed your application, and we are impressed with your qualifications and experience. We would like to invite you to interview with us Date: {ivdate} to further discuss your candidacy.

The interview will be conducted via Google Meet at {ivtime} IST. During the interview, we will discuss your skills, experiences, and how they align with the requirements of the position. Additionally, there will be an opportunity for you to ask any questions you may have about the role or our company.

Please confirm your availability for the interview by replying to this email at your earliest convenience. We understand that short notice may be inconvenient, but we hope you can accommodate this schedule.

We look forward to speaking with you and learning more about how you can contribute to our team at Goo Business.

Best regards,

Goo Business Team

Meeting Link: {meetinglink}
"""

        em = EmailMessage()
        em['From'] = emailSender
        em['To'] = emailReceiver
        em['subject'] = f'Invitation to Interview at Goo Business {datetime.now()}'
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as smtp:
            smtp.login(emailSender, ePassword)
            smtp.sendmail(emailSender, emailReceiver, em.as_string())



def sendEmailAndPassword(emailReceiver,users_password):
    if emailReceiver!="":
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f'Successfully created your account {datetime.now()}'
        messagee["From"] = senderEmail
        messagee["To"] = emailReceiver
        htmlHead = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin: 0;padding: 0;font-family: Arial, Helvetica, sans-serif;
}
.header{background-color: #2874f0;width: 100%;min-height: 54px;}
h1{color: rgb(9, 164, 9);margin: 10px;text-align: center;}
.data{color: blueviolet;}
.msg{margin:60px 0px;color: #5f6368;text-align: center;}
</style>
</head>"""
        htmlBody = f"""<body>
<div class="header"></div>
<h1>Goo Business<br>Successfully created your account</h1>
<div class="msg">Your login credential:<br><br>Dashboard: <a href="{OurMainURL}studentLogin">"{OurMainURL}studentLogin"</a><br>Username: "{emailReceiver}"<br>Password: "{users_password}"</div>
<div class="msg">Please do not share your login credential with anyone.</div>
</body>
</html>"""
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, emailReceiver, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            sendEmailFaild('Faild to send LogIn credential')

