#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime
import time,re,os


def due_calc(roll_number):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    book_names=[]
    fine_list=[]
    due_dates=[]
    present_date = datetime.date.today()

    def date_formatter(due_date):
        due_date = datetime.datetime.strptime(due_date, '%d/%m/%Y')
        return due_date.date()

    def site_login():
        driver.get("http://www.library.iitkgp.ac.in/opac/myaccount/myAccount.html")
        driver.find_element_by_id("usernameId").send_keys(roll_number)
        driver.find_element_by_id("submitButton").click()

    site_login()
    time.sleep(1)
    driver.get("http://www.library.iitkgp.ac.in/opac/myaccount/checkout.html")
    book_list = driver.find_element_by_id("Iterator1")
    books = book_list.find_elements_by_tag_name("li")
    username=driver.find_element_by_id("lblUserName").text
    username=username.split()
    stud_name=username[1]
    for book in books:
        fine=0
        info = book.text.splitlines()
        name = info[0]
        due_date = info[5]
        due_date = date_formatter(due_date)
        if due_date < present_date:
            numbers = re.findall('\d+', info[7])
            fine = int(numbers[0])
        book_names.append(name)
        due_dates.append(due_date)
        fine_list.append(fine)
    return book_names,due_dates,fine_list,stud_name

def send_mail(content,subject,email):
	message = Mail(
	    from_email='libdue@gmail.com',
	    to_emails=[email,'libdue@gmail.com'],
	    subject=subject ,
	    html_content=content)
	try:
	    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	except Exception as e:
		print(e.message)

def date_check(roll,email):
	flag=0
	overdue_flag=0
	book_exist_flag=0
	book_list=due_calc(roll)
	if len(book_list[0]):
		book_exist_flag=1
		content='<div><p style="font-size:1.8em;">Hey {}!</p>'.format(book_list[3])
		content+='<p style="font-size:1.3em";>Here are the details:</p>'
		content+="""<table border=1 style="border-collapse:collapse;border:3px solid #4000FF">
				<th>Book Name</th>
				<th>Due Date</th>
				<th>Fine</th>"""
		for i in range(0,len(book_list[0])):
			due_date=book_list[1][i]
			present_date=datetime.date.today()
			diff=(due_date-present_date).days
			if(diff>0 and (diff==7 or diff==1)):
				flag=1
				if overdue_flag==0:
					if diff==7:
						subject="Reminder! Library Books are due in {} days!".format(diff)
					elif diff==1:
						subject="Reminder! Library Books are due tomorrow!".format(diff)
				row='''
					<tr>
					<td> {name}</td>
					<td> {due_date} </td>
					<td> {fine} </td>
					</tr>'''.format(name=book_list[0][i],due_date=book_list[1][i].strftime("%A, %d %B %Y"),fine=book_list[2][i])
				content+=row
			elif diff<0:
				overdue_flag=1
				if (abs(diff)>0 and abs(diff)%7==0):
					flag=1
				subject="Uh oh! Your books are overdue in the Library!"
				row='''
					<tr>
					<td> {name}</td>
					<td> {due_date} </td>
					<td style="color: red;"> {fine} </td>
					</tr>'''.format(name=book_list[0][i],due_date=book_list[1][i].strftime("%A, %d %B %Y"),fine=book_list[2][i])
				content+=row
	if book_exist_flag:
		content+="</div>"
	print("Mail Flag: "+ str(flag))
	print("Overdue Flag: " + str(overdue_flag))
	print(book_list)
	print(overdue_flag)
	if flag:
		send_mail(content,subject,email)

