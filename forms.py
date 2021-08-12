from flask_wtf import FlaskForm
from connector import bcrypt
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,SelectField,FieldList,FormField,TextAreaField,validators,DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,NumberRange
from connector.models import LoginDetails,EmployeeDetails,MemberDetails,DoctorDetails,PatientDetails,PatientRecords



idtemp=0

class SignupFormEmployee(FlaskForm):
    firstname = StringField('First name',
                           validators=[DataRequired()])
    lastname = StringField('Last name',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=8,message='Password should be of atleast 8 characters.')])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    contactnumber=IntegerField('Contact Number',validators=[DataRequired(message="Data required and should be digits.")])

    role=SelectField('Department',choices=[('Technical', 'Technical'), ('Research', 'Research'), ('Software', 'Software'),('Hardware','Hardware')],
                           validators=[DataRequired()])

    submit = SubmitField('Sign Up')


    def validate_email(self,email):
      user1=MemberDetails.query.filter_by(email=email.data).first()
      user2= MemberDetails.query.filter_by(email=email.data).first()
      user3= MemberDetails.query.filter_by(email=email.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Email taken.Please choose different one')
        
    def validate_contactnumber(self,contactnumber):

      if len(str(contactnumber.data))!=10:
        raise ValidationError("Contact Number should be of 10 digits.")
      else:
        user1= MemberDetails.query.filter_by(contactnumber=contactnumber.data).first()
        user2= EmployeeDetails.query.filter_by(contactnumber=contactnumber.data).first()
        user3= DoctorDetails.query.filter_by(contactnumber=contactnumber.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Contact number taken.Please choose different one')

      

class SignupFormDoctor(FlaskForm):
    firstname = StringField('First name',
                           validators=[DataRequired()])
    lastname = StringField('Last name',validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    contactnumber=IntegerField('Contact Number',validators=[DataRequired(message="Data required and should be digits.")])

    role=SelectField('Designation',choices=[('Cardiologist', 'Cardiologist'), ('Neurosurgeon', 'Neurosurgeon'), ('Ophthalmologist', 'Ophthalmologist'),('ENT','ENT'),
      ('Dermatologist','Dermatologist'),('Pediatrician','Pediatrician'),('Psychiatrist','Psychiatrist'),('Dentist','Dentist'),('Gynaechologist','Gynaechologist'),('Orthopedic','Orthopedic'),('Surgeon','Surgeon')], validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_email(self,email):
      user1=MemberDetails.query.filter_by(email=email.data).first()
      user2= MemberDetails.query.filter_by(email=email.data).first()
      user3= MemberDetails.query.filter_by(email=email.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Email taken.Please choose different one')
        
    def validate_contactnumber(self,contactnumber):

      if len(str(contactnumber.data))!=10:
        raise ValidationError("Contact Nuber should be of 10 digits.")
      user1= MemberDetails.query.filter_by(contactnumber=contactnumber.data).first()
      user2= EmployeeDetails.query.filter_by(contactnumber=contactnumber.data).first()
      user3= DoctorDetails.query.filter_by(contactnumber=contactnumber.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Contact number taken.Please choose different one')


class SignupFormMember(FlaskForm):
    firstname = StringField('First name',
                           validators=[DataRequired()])
    lastname = StringField('Last name',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    contactnumber=IntegerField('Contact Number',validators=[DataRequired(message="Data required and should be digits.")])

    role=SelectField('Family Member',choices=[('B', 'Spouse(B)'), ('C', 'Child(C)'), ('D', 'Child(D)'),('E','Parent(E)'),('F','Parent(F)')],
                           validators=[DataRequired()])


    submit = SubmitField('Sign Up')

    def validate_email(self,email):
      user1=MemberDetails.query.filter_by(email=email.data).first()
      user2= MemberDetails.query.filter_by(email=email.data).first()
      user3= MemberDetails.query.filter_by(email=email.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Email taken.Please choose different one')
        
    def validate_contactnumber(self,contactnumber):
      
      if len(str(contactnumber.data))!=10:
        raise ValidationError("Contact Number should be of 10 digits.")

      user1= MemberDetails.query.filter_by(contactnumber=contactnumber.data).first()
      user2= EmployeeDetails.query.filter_by(contactnumber=contactnumber.data).first()
      user3= DoctorDetails.query.filter_by(contactnumber=contactnumber.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Contact number taken.Please choose different one')


class LoginForm(FlaskForm):
    userid = StringField('Userid',
                           validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember= BooleanField('Remember Me')

    submit = SubmitField('Login')

    usertemp=0

    def validate_userid(self,userid):
      global usertemp
      user=LoginDetails.query.filter_by(userid=userid.data).first()
      usertemp=user
      if not user:
        raise ValidationError('Userid does not exist.')

    def validate_password(self,password):
      if usertemp and not bcrypt.check_password_hash(usertemp.password,password.data):
        raise ValidationError('Password Incorrect.Try again.')

class SearchForm(FlaskForm):
    userid = StringField('Userid',
                           validators=[DataRequired()])

    submit = SubmitField('Search')

    global idtemp

    idtemp=userid

    def validate_userid(self,userid):
      user=LoginDetails.query.filter_by(userid=userid.data).first()
      if not user:
        raise ValidationError('Userid does not exist')

class MemberEntryForm(FlaskForm):

    name=StringField('Name',validators=[DataRequired()])

    times=IntegerField('Times', validators=[DataRequired()])

    days=IntegerField('Days', validators=[DataRequired()])

    dose=StringField('Dose', validators=[DataRequired()])

    remarks=StringField('Remarks', validators=[DataRequired()],widget=TextArea())

class Edit(FlaskForm):
  symptoms=TextAreaField('Symptoms',
                          validators=[DataRequired()],widget=TextArea())                      
  diagnosis=TextAreaField('Diagnosis',
                           validators=[DataRequired()],widget=TextArea())
  rows=IntegerField('Number of Medicines',validators=[DataRequired()])
  extras = FieldList(FormField(MemberEntryForm))
  submit=SubmitField('Submit')


class AppointmentForm1(FlaskForm):
  role=SelectField('Specialist',choices=[(1, 'Cardiologist'), (2, 'Neurosurgeon'), (3, 'Ophthalmologist'),(4,'ENT'),
      (5,'Dermatologist'),(6,'Pediatrician'),(7,'Dentist'),(8,'Gynaechologist'),(9,'Orthopedic'),(10,'Surgeon'),(11,'Psychiatrist')])
  name=SelectField('Doctor Name',choices=[])
  submit=SubmitField('Search')

class AppointmentForm2(FlaskForm):
  date=SelectField('Date',choices=[])
  time=SelectField('Time',choices=[])
  submit=SubmitField('Book')

class ModifyName(FlaskForm):
  firstname=StringField('First Name',validators=[DataRequired()])
  lastname=StringField('Last Name',validators=[DataRequired()])
  submit=SubmitField('Modify')

class ModifyContact(FlaskForm):
  contactnumber=StringField('Contact Number',validators=[DataRequired()])
  submit=SubmitField('Modify')

  def validate_contactnumber(self,contactnumber):

      if len(str(contactnumber.data))!=10:
        raise ValidationError("Contact Number should be of 10 digits.")
      else:
        user1= MemberDetails.query.filter_by(contactnumber=contactnumber.data).first()
        user2= EmployeeDetails.query.filter_by(contactnumber=contactnumber.data).first()
        user3= DoctorDetails.query.filter_by(contactnumber=contactnumber.data).first()

      if user1 or user2 or user3:
        raise ValidationError('Contact number taken.Please choose different one')





 