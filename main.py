# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv
import datetime as dt
import os
import smtplib
import random
import pandas

load_dotenv()
my_email = os.getenv("EMAIL")
email_password = os.getenv("DOMAIN_PW")
# Comma dilimited file (name,email,year,month,day)
data = pandas.read_csv("birthdays.csv")

# Reformat data to a dictionary format that makes locating information ideal.
bday_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data.iterrows()}
print(bday_dict)
# Check if today matches a birthday the birthdays.csv
now = dt.datetime.now()
this_month = now.month
today = now.day

today_tuple = (now.month, now.day)
if today_tuple in bday_dict:
    letter_number = random.randint(1, 3)
    bday_person = bday_dict[today_tuple]
    bday_email = bday_person.email
    with open(f"letter_templates/letter_{letter_number}.txt") as letter_file:
         letter_content = letter_file.read()
         Bday_letter = letter_content.replace("[NAME]", bday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=email_password)
        connection.sendmail(from_addr=my_email,
                             to_addrs=bday_email,
                             msg=f"Subject:Happy Birthday\n\n{Bday_letter}"
                             )
