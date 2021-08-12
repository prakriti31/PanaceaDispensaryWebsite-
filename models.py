from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from connector import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_userid):
	return LoginDetails.query.get(user_userid)

class LoginDetails(db.Model,UserMixin):
	__tablename__='logindetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid=db.Column(db.String(20),unique=True,nullable=True)
	password=db.Column(db.String(60),nullable=False)

	def __repr__(self):
		return f"LoginDetails('{self.userid},{self.password}')"

class EmployeeDetails(db.Model,UserMixin):
	__tablename__='employeedetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid=db.Column(db.String(20),unique=True,nullable=True)
	firstname=db.Column(db.String(20),nullable=False)
	lastname=db.Column(db.String(20),nullable=False)
	role=db.Column(db.String(20),nullable=False)
	contactnumber=db.Column(db.Integer(),nullable=False,unique=True)
	email=db.Column(db.String(40),unique=True,nullable=False)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')

	def __repr__(self):
		return f"EmployeeDetails('{self.userid},{self.firstname},{self.lastname},{self.role},{self.contactnumber},{self.email}')"

class DoctorDetails(db.Model,UserMixin):
	__tablename__='doctordetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid=db.Column(db.String(20),unique=True,nullable=True)
	firstname=db.Column(db.String(20),nullable=False)
	lastname=db.Column(db.String(20),nullable=False)
	contactnumber=db.Column(db.Integer(),nullable=False,unique=True)
	email=db.Column(db.String(40),unique=True,nullable=False)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	roleid=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False,unique=False)
	link= db.relationship('PatientDetails', backref='doctors', lazy=True)
	docappointment=db.relationship('AppointmentDetails',backref='appointment',lazy=True)
	
	def __repr__(self):
		return f"DoctorDetails('{self.userid},{self.firstname},{self.lastname},{self.contactnumber},{self.email}')"

class MemberDetails(db.Model,UserMixin):
	__tablename__='memberdetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	empid=db.Column(db.Integer)
	userid=db.Column(db.String(20),unique=True,nullable=True)
	firstname=db.Column(db.String(20),nullable=False)
	lastname=db.Column(db.String(20),nullable=False)
	role=db.Column(db.String(20),nullable=False)
	contactnumber=db.Column(db.Integer(),nullable=False,unique=True)
	email=db.Column(db.String(40),unique=True,nullable=False)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')

	def __repr__(self):
		return f"MemberDetails('{self.userid},{self.firstname},{self.lastname},{self.role},{self.contactnumber},{self.email}')"


class PatientDetails(db.Model):
	_tablename_='patientdetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid_patient=db.Column(db.String(20),nullable=False)
	userid_doctor=db.Column(db.String(20),db.ForeignKey('doctordetails.userid'),nullable=False,unique=False)
	diagnosis=db.Column(db.String(500),nullable=False)
	symptoms=db.Column(db.String(500),nullable=False)
	no_of_med=db.Column(db.Integer,nullable=False)
	date=db.Column(db.String(20),nullable=False)
	
	def _repr_(self):
		return f"PatientDetails('{self.userid_patient},{self.diagnosis},{self.symptoms}')"

class PatientRecords(db.Model):
	_tablename_='extra'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid_patient=db.Column(db.String(20),nullable=False)
	userid_doctor=db.Column(db.String(20),nullable=False)
	name=db.Column(db.String(50),nullable=False)
	days=db.Column(db.Integer,nullable=False)
	dose=db.Column(db.String(20),nullable=False)
	times=db.Column(db.Integer,nullable=False)
	remarks=db.Column(db.String(50),nullable=False)
	link=db.Column(db.Integer,nullable=False)

class AppointmentDetails(db.Model):
	__tablename__='appointmentdetails'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	userid_patient=db.Column(db.String(20),nullable=False)
	userid_doctor=db.Column(db.String(20),db.ForeignKey('doctordetails.userid'),nullable=False,unique=False)
	docname=db.Column(db.String(20),nullable=False)
	date=db.Column(db.String(20),nullable=False)
	time=db.Column(db.String(20),nullable=False)
	status=db.Column(db.String(20),nullable=False)

class Role(db.Model):
	__tablename__='role'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	role=db.Column(db.String(20),nullable=False)
	namerole = db.relationship('DoctorDetails', backref='docrole', lazy=True)






	
