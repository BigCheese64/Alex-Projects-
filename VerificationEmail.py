import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
class verification_email():
    def __init__(self,toaddr, vcode):
        self._toaddr=toaddr
        self.subject="ResCloud Verification"
        self.body="You verification code is "+str(vcode)
        self.fromaddr=""
        self.password=""
    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self._toaddr
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)#server only works for gmail
        server.starttls()
        server.login(fromaddr, self.password)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self._toaddr, text)
        server.quit()

verfication_email(sys.argv[1],sys.argv[2]).send_email()

"""
const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["path/to/script.py", arg1, arg2, ...]);

pythonProcess.stdout.on('data', (data) => {
    // Do something with the data returned from python script
});
"""
        
        
