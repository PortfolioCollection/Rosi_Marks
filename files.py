from bs4 import BeautifulSoup
import re
import datetime


def check_changes(html):
    print("previous saved transcript detected!")          
    # read the file for comparing
    saved = open("saved", "r").read().split("\n")
    print ("Comparing to the previous transcript......")
    #string = "Before: " + saved[i] + "\n" + "Now: " + ', '.join(course) + "\n"
    body = parse_soup(html,saved,lambda body,saved,course,i:
                      "" if ', '.join(course) == saved[i]
                      else "Before: " + saved[i] + "\n" + "Now: " + ', '.join(course) + "\n")
    if len(body) != 0:
        make_new_file(html)
    return body
    
def make_new_file(html):
    # make a file to save the grades
    f = open('saved', 'w')
    print ("Updating the existing transcript......")
    print("*************************************** ROSI Transcript ***************************************")
    body = parse_soup(html,f,lambda body,f,course,i: f.write(', '.join(course) + "\n"))
    f.close()
    print("******************************************************************************************")
    print("ROSI transcript saved!")
    return body

def parse_soup(html,file,check):    
    # soup
    soup = BeautifulSoup(html, "html5lib")
    # Part of the email
    body = ""
    i = 0
    # Find every table containing marks
    for table in soup.find_all("table", attrs={"class":"recentAcademicHistory"}):
        all_courses = []
        
        ## Print the academic year and degree 
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
                try:
                    body += check(body,file,course,i)
                except Exception as e:
                    print (course)
                i+=1
    return body

def update_file(update,html):
    
    print ("Logged in at: " + str(datetime.datetime.now()))
    if update == False:
        body = make_new_file(html) 
    else:
        body = check_changes(html)
    
    update = True
    return (update,body)
