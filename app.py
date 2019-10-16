from flask import Flask, render_template, request
#from twilio.rest import Client
import pickle
import smtplib
import random
import string

def randomStringDigits(stringLength):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

gmail_user = 'upgradethrowaway@gmail.com'
gmail_pwd = 'thisisathrowaway'
FROM = 'upgradethrowaway@gmail.com'
SUBJECT = "New Tutoring Opportunity"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("findtutor.html")
@app.route("/activation/<id>")
def activation(id):
    return render_template("tutor.html")
@app.route("/find", methods=['POST'])
def find():
    #projectpath = request.form['phone']
    #print(projectpath)
    if request.method == "POST":
        phone = request.form['phone']
        subject = request.form['sub']
        location = request.form['loc']
        estimated_min = request.form['eta']
        tmpsite = randomStringDigits(10)
        TEXT = "Hello tutors,\n\nWe need a tutor to help with {} at {} for {} min.  Please click the link below and paste this code if interested: {}\n\n http://127.0.0.1:5000/activation/{}".format(subject,location,estimated_min,tmpsite,tmpsite)
        #get all tutor phones
        with open('tutors.pickle', 'rb') as handle:
            d = pickle.load(handle)
            TO = [d[tutorPhone]["email"] for tutorPhone in d]

        #add tutoring opportunity
        with open('current_opportunities.pickle', 'rb') as handle:
            d = pickle.load(handle)
        d[tmpsite] = {"tutorfound":False, "phone":phone, "subject":subject, "location":location,"estimated_min":estimated_min}
        with open('current_opportunities.pickle', 'wb') as handle:
            pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            return "Tutors have been alerted! We will text you back once someone has responded. <a href='./'>return</a>".format(tmpsite)
        except:
            return "Could not send mail, please try again: <a href='./'>return</a>"
@app.route("/proposal", methods=['POST'])
def proposal():
    if request.method == "POST":
        code = request.form['code']
        with open('current_opportunities.pickle', 'rb') as handle:
            d = pickle.load(handle)
        print(d[code]["tutorfound"])
        print(d[code]["tutorfound"] == True)
        if d[code]["tutorfound"]:
            return "Sorry a tutor was already found for this position. We will alert you for future opportunities."
        else:
            d[code]["tutorfound"] = True
            with open('current_opportunities.pickle', 'wb') as handle:
                pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return str(d[code])
        return code
@app.route("/register", methods=['POST'])
def register():
    #projectpath = request.form['phone']
    #print(projectpath)
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        major = request.form['major']
        #add tutor
        with open('tutors.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
        unserialized_data[phone] = {"name":name,"email":email,"major":major}
        with open('tutors.pickle', 'wb') as handle:
            pickle.dump(unserialized_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return "You have been registered.  We will alert you when someone requests a tutor. <a href='./'>return</a>"

if __name__ == "__main__":
    app.run(debug=True)
