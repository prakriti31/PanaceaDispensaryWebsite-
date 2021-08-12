from flask import render_template,url_for,flash,redirect,request
from connector import app, db, bcrypt,mail
from connector.forms import LoginForm,SignupFormEmployee,SignupFormDoctor,SignupFormMember,SearchForm,MemberEntryForm,AppointmentForm1,AppointmentForm2,Edit,ModifyName,ModifyContact
from connector.models import LoginDetails,EmployeeDetails,MemberDetails,DoctorDetails,PatientDetails,PatientRecords,AppointmentDetails,Role
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Mail,Message
import datetime as DT
from flask import jsonify
from sqlalchemy import or_
import string

idtemp=0
user1=[]
user2=[]
role_id=1
doctorname=''
timelist1=[]
hrs="10"
mins="00"
while hrs!="19":
  timelist1.append(hrs+":"+mins)
  mins=str(int(mins)+20)
  if mins=="60":
    mins="00"
    hrs=str(int(hrs)+1)
    if hrs=="13":
      hrs="15"
	  
datelist=[]
@app.route("/",methods=['GET', 'POST'])
def homepage():
	if current_user.is_authenticated:
		usertemp=current_user.userid[:3]
		if current_user.userid=='Admin':
			return redirect(url_for('admin'))
		elif usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))
	form = LoginForm()
	if form.validate_on_submit():
		user=LoginDetails.query.filter_by(userid=form.userid.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page=request.args.get('next')
			usertemp=current_user.userid[:3]
			if current_user.userid=='Admin':
				return redirect(url_for('admin'))
			elif usertemp=='DOC':
				return redirect(url_for('doctorhome'))
			else:
				return redirect(url_for('memberhome'))

	return render_template('homepage.html', title='Login', form=form)


@app.route("/employeesignup",methods=['GET', 'POST'])
@login_required
def employeesignup():

	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	form=SignupFormEmployee()

	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		userlogin=LoginDetails(password=hashed_password)

		db.session.add(userlogin)
		db.session.commit()

		idvalue=userlogin.id
		idvalue="EMP-A"+str(idvalue-1)

		db.session.delete(userlogin)
		db.session.commit()

		userdetails=EmployeeDetails(userid=idvalue,firstname=form.firstname.data,lastname=form.lastname.data,
			role=form.role.data,contactnumber=form.contactnumber.data,email=form.email.data)
		userlogin=LoginDetails(userid=idvalue,password=hashed_password)

		db.session.add(userdetails)
		db.session.add(userlogin)
		db.session.commit()


		msg=Message(
			subject='Welcome to Panacea Dispensary!!',
			recipients=[userdetails.email],
			html="<h2>Welcome To Panacea Dispensary!!</h2><br><br><p>Following is your userid:%s</p>"%idvalue)
		
		mail.send(msg)

		return redirect(url_for('admin'))

	return render_template("employeesignup.html",title='Employee Signup',form=form)

@app.route("/admin")
@login_required
def admin():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')
		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	return render_template("admin.html")

@app.route("/doctorhome",methods=['GET', 'POST'])
@login_required
def doctorhome():
	usertemp=current_user.userid[:3]
	if usertemp!="DOC":
		flash("You don't have Doctor privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('memberhome'))
	form=SearchForm()
	global idtemp
	if form.validate_on_submit():
		idtemp=form.userid.data
		return redirect(url_for('doctor'))

	return render_template("doctorhome.html",title='Doctor Home',form=form)

@app.route("/viewhistorymember")
@login_required
def viewhistorymember():
	usertemp=current_user.userid[:3]
	if usertemp!="EMP":
		flash("You don't have Member privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))

	global idtemp
	idtemp = current_user.userid
	symp = []
	dose = []
	users1=PatientDetails.query.filter_by(userid_patient=idtemp)
	users2=PatientRecords.query.filter_by(userid_patient=idtemp)

	return render_template("viewhistorymember.html",users1=users1,users2=users2)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('homepage'))


@app.route("/doctor")
@login_required
def doctor():
	usertemp=current_user.userid[:3]
	if usertemp!="DOC":
		flash("You don't have Doctor privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('memberhome'))
	return render_template("doctor.html")

@app.route("/doctorsignup",methods=['GET', 'POST'])
@login_required
def doctorsignup():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))


	form=SignupFormDoctor()

	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		role_id=Role.query.filter_by(role=form.role.data).first()
		userlogin=DoctorDetails(firstname=form.firstname.data,lastname=form.lastname.data,
			roleid=role_id.id,contactnumber=form.contactnumber.data,email=form.email.data)

		db.session.add(userlogin)
		db.session.commit()

		idvalue=userlogin.id
		idvalue="DOC"+str(idvalue)
		db.session.delete(userlogin)
		db.session.commit()

		userdetails=DoctorDetails(userid=idvalue,firstname=form.firstname.data,lastname=form.lastname.data,
			roleid=role_id.id,contactnumber=form.contactnumber.data,email=form.email.data)
		userlogin=LoginDetails(userid=idvalue,password=hashed_password)

		db.session.add(userdetails)
		db.session.add(userlogin)
		db.session.commit()

		msg=Message(
			subject='Welcome to Panacea Dispensary!!',
			recipients=[userdetails.email],
			html="<h2>Welcome To Panacea Dispensary!!</h2><br><br><p>Following is your userid:%s</p>"%idvalue)
		
		mail.send(msg)

		return redirect(url_for('admin'))

	return render_template("doctorsignup.html",title='Doctor Signup',form=form)


@app.route("/help")
def help():
	return render_template("help.html")


@app.route("/memberentry",methods=['GET', 'POST'])
@login_required
def memberentry():
	usertemp=current_user.userid[:3]
	if usertemp!="DOC":
		flash("You don't have Doctor privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('memberhome'))

	form=Edit()
	if request.method == "POST":
		rows=form.rows.data
		patient=PatientDetails(userid_patient=idtemp,userid_doctor=current_user.userid,symptoms=request.form["symptoms"],diagnosis=request.form["diagnosis"],no_of_med=rows,date=DT.date.today())
		
		db.session.add(patient)
		db.session.commit()
		linking=patient.id
		for i in range(1,rows+1):
			new_patient = PatientRecords(userid_patient=idtemp,userid_doctor=current_user.userid,name=request.form["extras-"+str(i)+"-name"],days=request.form["extras-"+str(i)+"-days"],dose=request.form["extras-"+str(i)+"-dose"],times=request.form["extras-"+str(i)+"-times"],remarks=request.form["extras-"+str(i)+"-remarks"],link=linking)
			db.session.add(new_patient)
			db.session.commit()
			
		return redirect(url_for('doctor'))

	return render_template("memberentry.html",title='Member entry',form=form)

@app.route("/modifydetailsid",methods=['GET', 'POST'])
@login_required
def modifydetailsid():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	form = SearchForm()
	global idtemp

	if form.validate_on_submit():
		idtemp=form.userid.data
		return redirect(url_for('search_results'))

	return render_template("modifydetailsid.html", form=form)

@app.route('/results',methods=['GET', 'POST'])
@login_required
def search_results():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	global idtemp
	global user1
	global user2
	user1=[]
	user2=[]
	results=[]
	user1.append(EmployeeDetails.query.filter_by(userid=idtemp).first())
	user2.append(DoctorDetails.query.filter_by(userid=idtemp).first())
	print(idtemp)
	
	if user1!=[]:
		results.append(EmployeeDetails.query.filter_by(userid=idtemp).first())
	elif user2!=[]:
		results.append(DoctorDetails.query.filter_by(userid=idtemp).first())
	else:
		results.append(MemberDetails.query.filter_by(userid=idtemp).first())

	return render_template("results.html",results=results)
@app.route("/modifyname",methods=['GET','POST'])
@login_required
def modifyname():
	usertemp=current_user.userid[:3]

	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))
	
	form=ModifyName()
	global idtemp
	global user1
	global user2
	
	if form.validate_on_submit():

		if user1!=[]:
			results=EmployeeDetails.query.filter_by(userid=idtemp).update({EmployeeDetails.firstname:form.firstname.data})
			db.session.commit()
			results_=EmployeeDetails.query.filter_by(userid=idtemp).update({EmployeeDetails.lastname:form.lastname.data})
			db.session.commit()
			
		elif user2!=[]:
			results=DoctorDetails.query.filter_by(userid=idtemp).update({DoctorDetails.firstname:form.firstname.data})
			db.session.commit()
			results_=DoctorDetails.query.filter_by(userid=idtemp).update({DoctorDetails.lastname:form.lastname.data})
			db.session.commit()
			
		else:
			results=MemberDetails.query.filter_by(userid=idtemp).update({MemberDetails.firstname:form.firstname.data})
			db.session.commit()
			results_=MemberDetails.query.filter_by(userid=idtemp).update({MemberDetails.lastname:form.lastname.data})
			db.session.commit()
		return redirect(url_for('modifydetailshome'))

	return render_template("modifyname.html",form=form)

@app.route("/modifycontactnumber",methods=['GET','POST'])
@login_required
def modifycontactnumber():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))
	
	form=ModifyContact()
	global idtemp
	global user1
	global user2

	if form.validate_on_submit():

		if user1!=[]:
			results=EmployeeDetails.query.filter_by(userid=idtemp).update({EmployeeDetails.contactnumber:form.contactnumber.data})
			db.session.commit()

		elif user2!=[]:
			results=DoctorDetails.query.filter_by(userid=idtemp).update({DoctorDetails.contactnumber:form.contactnumber.data})
			db.session.commit()
			
		else:
			results=MemberDetails.query.filter_by(userid=idtemp).update({MemberDetails.contactnumber:form.contactnumber.data})
			db.session.commit()

		return redirect(url_for('modifydetailshome'))
			
		
	return render_template("modifycontactnumber.html",form=form)


@app.route("/modifydetailshome")
@login_required
def modifydetailshome():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	return render_template("modifydetailshome.html")

@app.route("/newmemberdetails",methods=['GET', 'POST'])
@login_required
def newmemberdetails():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	form=SignupFormMember()

	global idtemp

	if form.validate_on_submit():

		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		idvalue="EMP-"+form.role.data+idtemp[5:]

		userdetails=MemberDetails(userid=idvalue,empid=idtemp,firstname=form.firstname.data,lastname=form.lastname.data,
			role=form.role.data,contactnumber=form.contactnumber.data,email=form.email.data)
		userlogin=LoginDetails(userid=idvalue,password=hashed_password)

		db.session.add(userdetails)
		db.session.add(userlogin)
		db.session.commit()

		msg=Message(
			subject='Welcome to Panacea Dispensary!!',
			recipients=[userdetails.email],
			html="<h2>Welcome To Panacea Dispensary!!</h2><br><br><p>Following is your userid:%s</p>"%idvalue)
		
		mail.send(msg)

		return redirect(url_for('admin'))
	return render_template("newmemberdetails.html",title='New member details',form=form)


@app.route("/newmemberemployee",methods=['GET', 'POST'])
@login_required
def newmemberemployee():
	usertemp=current_user.userid[:3]
	if current_user.userid!="Admin":
		flash("You don't have Admin privileges!!",'danger')

		usertemp=current_user.userid[:3]
		if usertemp=='DOC':
			return redirect(url_for('doctorhome'))
		else:
			return redirect(url_for('memberhome'))

	form=SearchForm()
	global idtemp
	if form.validate_on_submit():
		idtemp=form.userid.data
		return redirect(url_for('newmemberdetails'))

	return render_template("newmemberemployee.html",title='New member employee',form=form)

@app.route("/viewhistorydoctor")
@login_required
def viewhistorydoctor():
	usertemp=current_user.userid[:3]
	if usertemp!="DOC":
		flash("You don't have Doctor privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('memberhome'))
	global idtemp
	symp = []
	dose = []
	users1=PatientDetails.query.filter_by(userid_patient=idtemp)
	users2=PatientRecords.query.filter_by(userid_patient=idtemp)


	return render_template("viewhistorydoctor.html",users1=users1,users2=users2)

@app.route("/memberhome")
@login_required
def memberhome():
	usertemp=current_user.userid[:3]
	if usertemp!="EMP":
		flash("You don't have Member privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))

	return render_template("memberhome.html")



@app.route("/appointmentform1",methods=['GET', 'POST'])
@login_required
def appointmentform1():
	usertemp=current_user.userid[:3]
	if usertemp!="EMP":
		flash("You don't have Member privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))
					
	form=AppointmentForm1()

	form.name.choices=[(doctor.firstname+" "+doctor.lastname,doctor.firstname+" "+doctor.lastname) for doctor in DoctorDetails.query.filter_by(roleid=1)]

	if request.method=='POST':
		global role_id
		global doctorname
		role_id=form.role.data
		doctorname=form.name.data

		return redirect(url_for('appointmentform2'))

	return render_template("appointmentform1.html",form=form)

@app.route('/appointmentform1/<role>')
def name(role):

	names= DoctorDetails.query.filter_by(roleid=role).all()
	nameArray = []
	for name in names:
		nameObj = {}
		nameObj['id'] = name.firstname+" "+name.lastname
		nameObj['name'] = name.firstname+" "+name.lastname
		nameArray.append(nameObj)

	return jsonify({'names' : nameArray})

@app.route("/appointmentform2",methods=['GET', 'POST'])
@login_required
def appointmentform2():
	usertemp=current_user.userid[:3]
	if usertemp!="EMP":
		flash("You don't have Member privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))
					
	form=AppointmentForm2()

	global datelist
	global timelist1
	global doc_id
	global doctorname
	datelist=[]
	tmrw=DT.date.today()+DT.timedelta(days=1)
	datelist.append(tmrw)
	for j in range(1,10):
		datelist.append(tmrw+DT.timedelta(days=j))
	
	print(datelist)

	form.date.choices=[(datelist[0],datelist[0]),(datelist[1],datelist[1]),(datelist[2],datelist[2]),(datelist[3],datelist[3]),(datelist[4],datelist[4]),(datelist[5],datelist[5]),(datelist[6],datelist[6]),(datelist[7],datelist[7]),(datelist[8],datelist[8]),(datelist[9],datelist[9])]

	temptime=[time.time for time in AppointmentDetails.query.filter_by(docname=doctorname,date=datelist[0])]
	timelist=[]
	for time in timelist1:
		if time not in temptime:
			timelist.append(time)
	form.time.choices=[(time,time) for time in timelist]

	if request.method=='POST':
		doc=doctorname.split()
		doclast=str(doc[1])
		doctor=DoctorDetails.query.filter_by(lastname=doclast).first()
		patient=AppointmentDetails(userid_patient=current_user.userid,docname=doctorname,date=form.date.data,time=form.time.data,status='BOOKED',userid_doctor=doctor.userid)
		db.session.add(patient)
		db.session.commit()

		return redirect(url_for('memberhome'))

	return render_template("appointmentform2.html",form=form)

@app.route('/appointmentform2/<date>')
def time(date):
	global role_id
	global doctorname
	times_=[time.time for time in AppointmentDetails.query.filter_by(docname=doctorname,date=date)]
	times=[]
	for time in timelist1:
		if time not in times_:
			times.append(time)
	timeArray = []
	for time in times:
		timeObj = {}
		timeObj['id'] = time
		timeObj['time'] = time
		timeArray.append(timeObj)

	return jsonify({'times' : timeArray})

@app.route("/appointmentstatus")
@login_required
def appointmentstatus():
	usertemp=current_user.userid[:3]
	if usertemp!="EMP":
		flash("You don't have Member privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))
	global idtemp
	idtemp=current_user.userid

	users=AppointmentDetails.query.filter_by(userid_patient=idtemp)


	return render_template("appointmentstatus.html",users=users)

@app.route("/doctorappointment")
@login_required
def doctorappointment():
	usertemp=current_user.userid[:3]
	if usertemp!="DOC":
		flash("You don't have Doctor privileges!!",'danger')

		if current_user.userid=="Admin":
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('doctorhome'))

	global idtemp
	datelist=[]
	today=DT.date.today()
	datelist.append(today)
	for j in range(1,11):
		laps=DT.timedelta(days=j)
		datelist.append(str(today+laps))

	users=AppointmentDetails.query.filter_by(userid_doctor=current_user.userid)

	return render_template("doctorappointment.html",users=users,datelist=datelist)



