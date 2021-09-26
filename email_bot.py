import re
import smtplib
import time
import random
import pandas
import datetime
from src.m_config import *

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email_log = data["email"]
password = data["password"]
subject_str = data["subject"]
#message = finishedQuote#input("Enter Message:")
text = data["path"]
with open(text,"r") as f:
    text = f.read()
def check(email):
    n_email = re.findall(regex, email)
    return n_email
 
def sendemail(bomb_email,amt,x):
    total_time = datetime.datetime.now()
    try:
        try:
            subject = subject_str + " - %s" % (bomb_email)
            message = 'Subject: {}\n\n{}'.format(subject, text)
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login(email_log,password)
            mail.sendmail(email,bomb_email,message)
            print(str(x) + "/" + amt +" message sent to {}".format(bomb_email))
        except Exception as e:
            print("Failed to send email to %s"%(bomb_email))
            print("Error -", e)
            return False
        time.sleep(1)

        mail.close()
    except Exception as e:
        print(e)
        mail.close()
        time.sleep(3)

    print("Execution time: ", datetime.datetime.now() - total_time)
    print("Done")

with open("src/emails.txt", encoding="utf8") as f:
    emails = f.readlines()

def to_sheet(name):
    df = pandas.read_csv("src/sent.csv", index_col = False)
    l = []
    d = {}
    date = str(datetime.datetime.now()).split(" ")[0]
    d["Address sent"] = name
    d["Date"] = "%s" % (date)
    l.append(d)
    content = pandas.DataFrame(l)
    content = pandas.concat([df, content],ignore_index=True)
    content.to_csv("src/sent.csv")
    print("Saved %s to sheets" % (name))


num = []
for i in range(0,200,30):
    num.append(i)

new_data = pandas.read_csv("src/sent.csv")
old_data = []
for i in emails:
    old_data.append(i.replace("\n","").strip())
mail_l = []
for i in new_data["Address sent"]:
    mail_l.append(i)

x = len(mail_l)
k = 0
for i in old_data:
    if k > 500:
        print()
        print("Reached",k,"emails")
        k = 0
        for j in range(90000):
            print("Time remaining till next run:",j, end="\r")
            time.sleep(1)
    if i in mail_l:
        print("Already sent to", i)
        continue
    else:
        email = i
        email = check(email)
        if len(email) == 0:
            continue
        if email[0].split("@")[1] == "gmail.com" or email[0].split("@")[1] == "yahoo.com":
            x += 1
            nani = sendemail(email[0],str(len(old_data)),x)
            k += 1
            if nani == False:
                rnd_time = random.choice(num)
                print("Continuing in", rnd_time, "seconds")
                time.sleep(rnd_time)
            else:
                to_sheet(email[0])
                rnd_time = random.choice(num)
                print("Next email in ", "1", "seconds")
                time.sleep(1)

print("\nNo email address left")
input("Press the enter key to terminate:")