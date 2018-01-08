def read_credentials():
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
    return (student_number, pin, gmail_address, gmail_password, to_address)

def get_timeout():
    
    timeout = ""
    login = open("config.txt", "r").read().split("\n")

    for line in login:
        if line.startswith('pause'):
            timeout = line[line.find("=") + 1:]
    return timeout    