#####################################
#####################################
## Project: PCA                    ##
##         Streamlit               ##
#####################################
## Description:                    ##
## This script was made to apply   ##
## the Inverse Laplace Transform   ##
## on CPMG, IR and SR data         ##
#####################################
## Version:  1.0                   ##
## Revision: 1.0                   ##
## Date: 07/13/2023                ##
#####################################
## Requirements:                   ##
##                                 ##
##  - matplotlib = 3.7.2		   ##
##  - numpy = 1.25.1		       ##
##  - streamlit = 1.24.1		   ##
##  - streamlit-option-menu = 0.3.6##
##  - plotly = 5.15.0       	   ##
##  - secure-smtplib = 0.1.1       ##
##  - python-dotenv = 1.0.0        ##
##                                 ##
##     //--- INTRUCTIONS ---//     ##
##                                 ##
##  pip install matplotlib==3.7.2  ##
##  pip install numpy==1.25.1      ##
##  pip install streamlit==1.24.1  ##
##  pip install streamlit-option-  ##
## menu==0.3.6                     ##
##  pip install plotly==5.15.0     ##
##  pip install secure-smtplib==0.1.1#
##  pip install python-dotenv==1.0.0#
##				                   ##
#####################################
## Script Development:             ##
##                                 ##
## - Tiago Bueno de Moraes         ##
##  [Developer]		               ##
##                                 ##
## - William Silva Mendes          ##
##  [Developer]		               ##
##                                 ##
## - Larissa Perosso Mazzero       ##
##  [Developer]		               ##
##                                 ##
##  [07/13/2023]                   ##
#####################################
## Modifications:                  ##
## 01. <NAME>                      ##
##     <COMPANY>                   ##
##     <SECTOR>                    ##
##     <DATE>                      ##
##     <MODIFICATIONS MADE>        ##
##				                   ##
##                                 ##
#####################################
#####################################

##################################
### Import Libraries
##################################
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

##################################
### Configurations
##################################
# Load environment variables from the .env file
load_dotenv()

##################################
### Functions
##################################

##################################
## This function will renderizer the contact page
##
##
def send_email(name, email, message):

    receiver_email = "tiago.moraes@usp.com"

    subject = f"Contact form submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\n{message}"

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = os.getenv("GMAIL_USERNAME")
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the Gmail SMTP server and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_PASSWORD"))
        server.sendmail(os.getenv("GMAIL_USERNAME"), receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")
        return False

def contact():
    st.header(":mailbox: Contact us!")

    name = st.text_input("Your name", key="name0")
    email = st.text_input("Your email", key="email0")
    message = st.text_area("Your message here", key="message0")
    if st.button("Send"):
        if name and email and message:
            if send_email(name, email, message):
                st.success("Email sent successfully!")
                # Clear the form after sending the email
                #st.text_input("Your name", value='', key="name1")
                #st.text_input("Your email", value='', key="email1")
                #st.text_area("Your message here", value='', key="message1")
        else:
            st.warning("Please fill in all fields before sending the email.")
##################################

if __name__ == "__main__":
    contact()
##################################
##################################
#######     CODE END       #######
##################################
##################################