import credentials
import files
import email_sender
import requests
import time
import os.path

def login():
    info = credentials.read_credentials()
    student_number, pin, gmail_address, gmail_password, to_address = info
    TIMEOUT = (int)(credentials.get_timeout())
    # if update is false, download data and write to file
    # if update is true, read file and compare
    update = False
    if os.path.exists("saved"):
        update = True

    while True:  
        print("...............................")  
        print ("Logging in ROSI")
        # log onto the server and ignore warnings
        requests.packages.urllib3.disable_warnings()
        page = weblogin(student_number,pin)
        html = page.content
            
        update,body = files.update_file(update,html)

        if(update):
            email_sender.send_mail(info,body)
            # update the file on the next iteartion 
            update = False
            # reset email body
            body = ""
        
        #Program will update the save file immediately if transcript was changed  
        #else it will have a timer delay before it checks again (in seconds)
        print ("Recheck in " + str(TIMEOUT) + " seconds ... \n")
        time.sleep(TIMEOUT)

def weblogin(student_number,pin):
    
    """Logs into rosi and navigates to the marks url"""
    
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

        return page
    
if __name__=="__main__":
    login()
