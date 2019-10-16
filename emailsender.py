import smtplib

gmail_user = 'upgradethrowaway@gmail.com'
gmail_pwd = 'thisisathrowaway'
FROM = 'upgradethrowaway@gmail.com'
recipient = 'radeymichael@gmail.com'
TO = recipient if type(recipient) is list else [recipient]
SUBJECT = "New Tutoring Opportunity"
TEXT = "Hello {}, there is a new tutoring opportunity in your area.  Someone needs help in something at somewhere for some time.  Please respond to this email if you are interested!"

# Prepare actual message
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print('successfully sent the mail')
except:
    print("failed to send mail")
