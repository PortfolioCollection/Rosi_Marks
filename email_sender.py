import smtplib

def send_mail(info,body):
    # Send an email if mark changed 
    if body != "":
        student_number, pin, gmail_address, gmail_password, to_address = info
        print("======================================= Changes dectected =======================================")
        print(body)
        print("=================================================================================================")  
        print("Attempting sending email to: " + to_address)
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
        except Exception as e:
            print ("failed to send mail")
            print(e)
                
        print("=================================================================================================")        
    else:
        print(">>> No changes found")
