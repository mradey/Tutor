from flask import Flask, render_template, request
#from twilio.rest import Client
import pickle
import smtplib

gmail_user = 'upgradethrowaway@gmail.com'
gmail_pwd = 'thisisathrowaway'
FROM = 'upgradethrowaway@gmail.com'
SUBJECT = "New Tutoring Opportunity"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("findtutor.html")
@app.route("/find", methods=['POST'])
def find():
    #projectpath = request.form['phone']
    #print(projectpath)
    if request.method == "POST":
        phone = request.form['phone']
        subject = request.form['sub']
        location = request.form['loc']
        estimated_min = request.form['eta']
        TEXT = "Hello tutors,\n\nWe need a tutor to help with {} at {} for {} min.  Please click this link and paste this code if interested".format(subject,location,estimated_min)
        with open('tutors.pickle', 'rb') as handle:
            d = pickle.load(handle)
            TO = [d[tutorPhone]["email"] for tutorPhone in d]
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            return "Tutors have been alerted! We will text you back once someone has responded. <a href='./'>return</a>"
        except:
            return "Could not send mail, please try again: <a href='./'>return</a>"
@app.route("/register", methods=['POST'])
def register():
    #projectpath = request.form['phone']
    #print(projectpath)
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        major = request.form['major']
        with open('tutors.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
        unserialized_data[phone] = {"name":name,"email":email,"major":major}
        with open('tutors.pickle', 'wb') as handle:
            pickle.dump(unserialized_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return "You have been registered.  We will alert you when someone requests a tutor. <a href='./'>return</a>"

if __name__ == "__main__":
    app.run(debug=True)
