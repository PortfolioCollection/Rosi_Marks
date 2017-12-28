from bs4 import BeautifulSoup
import requests
import re

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
        
# log onto the server 
with requests.Session() as c:
    
    # Commented out so you dont login every 30 seconds to test
    
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
    
    """     
    ## TESTING FROM DOWNLOADED HTML FILE
    f = open('history.txt','r')    
    html = f.read()
    """
    
    # soup
    soup = BeautifulSoup(html, "lxml")
    
    #Find every table containing marks    
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
