from flask import Flask, session, flash, redirect, url_for, escape, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from wtforms import validators
from random import randint
import random
import barcode
from barcode import generate
from barcode.writer import ImageWriter
import flaskpdf



app = Flask(__name__)
flaskpdf.init_app(app)

#Initalize Forms
class MyForm(FlaskForm):
    # course reg form
    registration = StringField(validators=[DataRequired()], render_kw={"placeholder": "Reg Number"})
    fullname = StringField(validators=[DataRequired()], render_kw={"placeholder": "Full Name"})
    dept = StringField(validators=[DataRequired()], render_kw={"placeholder": "Department"})
    passport = StringField(render_kw={"placeholder": "Passport Link"})
    #courses
    course1 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course2 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course3 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course4 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course5 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course6 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    course7 = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Course Code"})
    # reg ammounts
    c1amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c2amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c3amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c4amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c5amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c6amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
    c7amt = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Desired Amount"})
@app.route('/',methods=["GET", "POST"])
def home():
    form = MyForm()
    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/receipt', methods=["GET", "POST"])
def receipt():
    form = MyForm()
    if not form.validate_on_submit():
        flash('All fields are required.')
        return render_template('index.html',form=form)
    else:
        #receipt = request.form

        registration  = request.form['registration']
        fullname  = request.form['fullname']
        dept  = request.form['dept']
        passport = request.form['passport']
        
        if passport == "":
            passport = "data:image/jpeg;base64,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"
        else:
            passport = request.form['passport']
        
        course1  = request.form['course1']
        course2  = request.form['course2']
        course3  = request.form['course3']
        course4  = request.form['course4']
        course5  = request.form['course5']
        course6  = request.form['course6']
        course7  = request.form['course7']
        
        c1amt  = request.form['c1amt']
        c2amt  = request.form['c2amt']
        c3amt  = request.form['c3amt']
        c4amt  = request.form['c4amt']
        c5amt  = request.form['c5amt']
        c6amt  = request.form['c6amt']
        c7amt  = request.form['c7amt']
        total = int(c1amt) + int(c2amt) + int(c3amt) + int(c4amt) + int(c5amt) + int(c6amt) + int(c7amt)
        total = str(total)
        return render_template('receipt.html', registration=registration, fullname=fullname, dept=dept, course1=course1, course2=course2, course3=course3, course4=course4, course5=course5,course6=course6, course7=course7, c1amt=c1amt, c2amt=c2amt, c3amt=c3amt, c4amt=c4amt, c5amt=c5amt, c6amt=c6amt, c7amt=c7amt, passport=passport, total=total)
class Barcode:    
    @app.context_processor
    def my_utility_processor():
        def generate_numbers(self):
            """ returns the formated serials """
            self.serials = ''.join(str(random.randint(0,9)) for _ in range(12))
            return self.serials   

        def generate_barcode(self):
            '''EAN = barcode.get_barcode('code39')
            ean = EAN(u'serials')
            fullname = ean.save('code39_barcode')'''
    
            barcode = generate('code39', self.serials, writer=ImageWriter(), output='static/images/barcode_png')
            barcode_URL = "static/images/barcode_png.png"
            return barcode_URL
        return dict(generate_numbers=generate_numbers, generate_barcode=generate_barcode)

barcode = Barcode()


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)