from bs4 import BeautifulSoup
import requests
import re
import smtplib
import os.path
import time 

# read config file
student_number, pin, gmail_address, gmail_password, to_address = "","","","",""

login = open("config.txt", "r").read().split("\n")

for line in login:
    if line.startswith('student_number'):
        student_number = line[line.find("=") + 1:]
    if line.startswith('pin'):
        pin = line[line.find("=") + 1:]
    if line.startswith('your_gmail_address'):
        gmail_address = line[line.find("=") + 1:]
    if line.startswith('your_gmail_password'):
        gmail_password = line[line.find("=") + 1:]
    if line.startswith('to_email_address'):
        to_address = line[line.find("=") + 1:]
# Part of the email
body = ""

# if update is false, download data and write to file
# if update is true, read file and compare
update = False
if os.path.exists("saved"):
    update = True

while True:    
    # log onto the server 
    with requests.Session() as c:  
        url = 'https://sws.rosi.utoronto.ca/sws/auth/login/verify.do'
        c.get(url, verify=False) 
        
        payload = {"personId": student_number,
                   "pin": pin, 
                   "verify.dispatch": "1"
                   }
        
        c.post(url, data=payload)
        
        # The main page after login
        c.get('https://sws.rosi.utoronto.ca/sws/welcome.do?welcome.dispatch')
        
        # The transcript page
        page = c.get('https://sws.rosi.utoronto.ca/sws/transcript/main.do?main.dispatch')
        
        #print(page.content)    
        html = page.content
        
        # soup
        soup = BeautifulSoup(html, "lxml")
        
        if update == False:
            # make a file to save the grades
            f = open('saved', 'w')
        else:
            saved = open("saved", "r").read().split("\n")
            i = 0
        
        print("*************************************** Transcript ***************************************")
        # Find every table containing marks    
        for table in soup.find_all("table", attrs={"class":"recentAcademicHistory"}):
            all_courses = []
            
            # The academic year and degree 
            print(re.sub('\s+', ' ', table.find("tr").find("th").get_text()))
            
            # Rest of the table
            for tr in table.find_all("tr"):
                course = []
                for td in tr.find_all("td"):
                    # get individual line 
                    line = (re.sub('\s+', ' ', td.get_text()))
                    
                    # replace white space with N/A
                    if line == " ":
                        line = "N/A"
                    
                    course.append(line)
                    
                # only keep the lines with courses 
                if len(course) == 5:                
                    print (course)
                    if update == False:
                        f.write(', '.join(course) + "\n")
                    else:
                        if ', '.join(course) == saved[i]:
                            # print("****Did not change****")
                            i+=1
                        else:
                            body += "Before: " + saved[i] + "\n" + "Now: " + ', '.join(course) + "\n"
                            i+=1

        print("******************************************************************************************")                            
                        
    # Send an email if mark changed 
    if body != "":
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (gmail_address, to_address, "Marks updated!", body)
        
        # send the email from the secure port 465
        try:
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server_ssl.ehlo()
            server_ssl.login(gmail_address, gmail_password)  
            server_ssl.sendmail(gmail_address, to_address, message)
            server_ssl.close()
            print ('successfully sent the mail')       
        except:
            print ("failed to send mail")
        # reset email body
        body = ""
        # update the file on the next iteartion 
        update = False
    
    # pause for a bit before checking again (in seconds)   
    time.sleep(1800) 