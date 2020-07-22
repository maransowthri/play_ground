import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from encrypt_decrypt import get_decrypted_message

port = 2525 
smtp_server = "smtp.gmail.com"
login = "maransowthrik@gmail.com"
password = b'gAAAAABfGB6wN22gR76WRF3KBVn2EN4DFchpDgCSBpQyEvraGqHan3s3YJ479s45a_uvAY_QczYs_jhC9tCix3vDRIP7gCMJ_w=='
sender_email = "maransowthrik@gmail.com"
receiver_email = "kmaran@athenahealth.com"
message = MIMEMultipart("alternative")
message["Subject"] = "Biweekly 31/07/2020"
message["From"] = sender_email
message["To"] = receiver_email

html = """\
<html>
  <body>
    <p>Hi Team, Biweekly for this week has been completed sucessfully.</p>
    <p></p>
    <p><a href="https://athenaconfluence.athenahealth.com/x/qWZGE">Find the Summary Reports here.</a></p>
    <p> Feel free to let us know if you need additional information!</p>
  </body>
</html>
"""

part1 = MIMEText(html, "html")
message.attach(part1)

with smtplib.SMTP_SSL(smtp_server, 465) as server:
    server.login(login, get_decrypted_message(password))
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

print('Sent') 