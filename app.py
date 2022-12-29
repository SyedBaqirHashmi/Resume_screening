from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, BLOB, VARCHAR, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True
app = Flask(__name__)
app.secret_key = 'the random string'
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


'''hello'''
engine = create_engine(
    'mysql:///?user=root&password=&database=resumescreening&server=127.0.0.1&port=3306')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


class seeker_signin(db.Model):
    seeker_id = db.Column(db.Integer, primary_key=True)
    seeker_name = db.Column(db.String(20), unique=True, nullable=False)
    seeker_email = db.Column(db.String(30), unique=True, nullable=False)
    seeker_pass = db.Column(db.String(20), unique=True, nullable=False)


class seeker(db.Model):
    seeker_id = db.Column(db.Integer, primary_key=True)
    seeker_name = db.Column(db.String(20), unique=False, nullable=False)
    seeker_email = db.Column(db.String(30), unique=True, nullable=False)
    seeker_pass = db.Column(db.String(20), unique=False, nullable=False)


class seeker_apply(db.Model):
    seeker_id = db.Column(db.Integer, primary_key=True)
    seeker_name = db.Column(db.String(20), unique=True, nullable=False)
    seeker_email = db.Column(db.String(30), unique=True, nullable=False)
    seeker_portfolio = db.Column(db.String(20), unique=True, nullable=False)
    seeker_cv = db.Column(db.String(120), unique=False, nullable=False)
    seeker_coverlet = db.Column(db.String(120), unique=False, nullable=False)


class S_contact(db.Model):
    seeker_id = db.Column(db.Integer, primary_key=True)
    S_name = db.Column(db.String(30), unique=False, nullable=False)
    S_email = db.Column(db.String(30), unique=True, nullable=False)
    S_subject = db.Column(db.String(120), unique=True, nullable=False)
    S_msg = db.Column(db.String(120), unique=True, nullable=False)


class rec_jobpost(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    rec_cname = db.Column(db.String(20), unique=True, nullable=False)
    rec_loc = db.Column(db.String(30), unique=True, nullable=False)
    rec_email = db.Column(db.String(30), unique=True, nullable=False)
    rec_phone = db.Column(db.String(20), unique=True, nullable=False)
    rec_jobtitle = db.Column(db.String(120), unique=False, nullable=False)
    rec_dop = db.Column(db.String(120), unique=False, nullable=False)
    rec_vac = db.Column(db.String(120), unique=False, nullable=False)
    rec_nature = db.Column(db.String(120), unique=False, nullable=False)
    rec_salary = db.Column(db.Integer, unique=False, nullable=False)
    rec_desc = db.Column(db.String(120), unique=False, nullable=False)
    rec_jobresonsibilty = db.Column(
        db.String(120), unique=False, nullable=False)
    rec_jobrequirements = db.Column(
        db.String(120), unique=False, nullable=False)
    rec_logo = db.Column(db.String(120), unique=False, nullable=False)


class seeker_profile(db.Model):
    seeker_id = db.Column(db.Integer, primary_key=True)
    seeker_uname = db.Column(db.String(30), unique=False,  nullable=False)
    seeker_address = db.Column(db.String(30), unique=True, nullable=False)
    seeker_email = db.Column(db.String(120), unique=True,  nullable=False)
    seeker_phone = db.Column(db.String(120), unique=True,  nullable=False)
    seeker_rdetails = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_aoe = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_exp = db.Column(db.String(1200), unique=False, nullable=False)
    seeker_deg = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_uni = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_loc = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_yod = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_skills = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_eca = db.Column(db.String(120), unique=False,  nullable=False)
    seeker_pic = db.Column(db.String(220), unique=False, nullable=False)
    seeker_resume = db.Column(db.String(150), unique=True, nullable=False)


class Recruiter_profile(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    rec_cname = db.Column(db.String(20), unique=True, nullable=False)
    rec_loc = db.Column(db.String(30), unique=True, nullable=False)
    rec_email = db.Column(db.String(30), unique=True, nullable=False)
    rec_phone = db.Column(db.String(20), unique=True, nullable=False)
    rec_desc = db.Column(db.String(120), unique=False, nullable=False)
    rec_history = db.Column(db.String(120), unique=False, nullable=False)
    rec_objectives = db.Column(db.String(120), unique=False, nullable=False)
    rec_services = db.Column(db.String(120), unique=False, nullable=False)
    rec_pic = db.Column(db.String(150), unique=True, nullable=False)


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template('login.html')


@app.route("/index", methods=['POST', 'GET'])
def index():
    return render_template('index.html', params=params)


@app.route("/index_rec", methods=['POST', 'GET'])
def index_rec():
    return render_template('index_rec.html', params=params)


@app.route("/layout_rec", methods=['POST', 'GET'])
def layout_rec():
    return render_template('layout_rec.html', params=params)


@app.route("/Portfoliojs", methods=['GET', 'POST'])
def Portfoliojs():
    if (request.method == 'POST'):
        uname = request.form.get('Jobseeker_name')
        address = request.form.get('JobSeeker_address')
        email = request.form.get('JobSeeker_email')
        phone = request.form.get('JobSeeker_phone')
        rdetails = request.form.get('JobSeeker_Descrip')
        aoe = request.form.get('JobSeeker_experties')
        exp = request.form.get('JobSeeker_experience')
        deg = request.form.get('JobSeeker_qualification')
        uni = request.form.get('JobSeeker_university')
        loc = request.form.get('JobSeeker_university_adress')
        yod = request.form.get('JobSeeker_degree_date')
        skills = request.form.get('JobSeeker_skills')
        eca = request.form.get('JobSeeker_Curricular')
        pic = request.form.get('Jobseeker_picture')
        resume = request.form.get('Jobseeker_cv')

        entry1 = seeker_profile(
            seeker_uname=uname,
            seeker_address=address,
            seeker_email=email,
            seeker_phone=phone,
            seeker_rdetails=rdetails,
            seeker_aoe=aoe,
            seeker_exp=exp,
            seeker_deg=deg,
            seeker_uni=uni,
            seeker_loc=loc,
            seeker_yod=yod,
            seeker_skills=skills,
            seeker_eca=eca,
            seeker_pic=pic,
            seeker_resume=resume
        )
        db.session.add(entry1)
        db.session.commit()
    return render_template('Portfoliojs.html', params=params)


@app.route("/Profile_rec", methods=['GET', 'POST'])
def Profile_rec():
    if (request.method == 'POST'):
        Cname = request.form.get('C_name')
        Caddress = request.form.get('C_address')
        Cemail = request.form.get('C_email')
        Cphone = request.form.get('C_phone')
        Cdescrip = request.form.get('C_Descrip')
        Chistory = request.form.get('C_history')
        Cobj = request.form.get('C_obj')
        Cserv = request.form.get('C_service')
        Cpic = request.form.get('C_picture')

        entry2 = Recruiter_profile(
            rec_cname=Cname,
            rec_loc=Caddress,
            rec_email=Cemail,
            rec_phone=Cphone,
            rec_desc=Cdescrip,
            rec_history=Chistory,
            rec_objectives=Cobj,
            rec_services=Cserv,
            rec_pic=Cpic,
        )
        db.session.add(entry2)
        db.session.commit()
    return render_template('Profile_rec.html', params=params)


@app.route("/Post", methods=['GET', 'POST'])
def Post():
    if (request.method == 'POST'):
        Cname = request.form.get('Company_name')
        Caddress = request.form.get('Company_address')
        Cemail = request.form.get('Company_email')
        Cphone = request.form.get('Company_phone')
        Jobtitle = request.form.get('Job_title')
        publish = request.form.get('Job_publish')
        Vacancy = request.form.get('Vacancy_position')
        Jobnature = request.form.get('Job_nature')
        Salary = request.form.get('Salary')
        Jobdescription = request.form.get('Job_description')
        Jobresponsibility = request.form.get('Job_responsibility')
        requirement = request.form.get('job_requirement')
        clogo = request.form.get('company_logo')

        entry3 = rec_jobpost(
            rec_cname=Cname,
            rec_loc=Caddress,
            rec_email=Cemail,
            rec_phone=Cphone,
            rec_jobtitle=Jobtitle,
            rec_dop=publish,
            rec_vac=Vacancy,
            rec_nature=Jobnature,
            rec_salary=Salary,
            rec_desc=Jobdescription,
            rec_jobresonsibilty=Jobresponsibility,
            rec_jobrequirements=requirement,
            rec_logo=clogo
        )
        db.session.add(entry3)
        db.session.commit()

    return render_template('Post.html', params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = S_contact(S_name=name, S_email=email,
                          S_subject=subject, S_msg=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route("/about", methods=['POST', 'GET'])
def about():
    return render_template('about.html', params=params)


@app.route("/about_rec", methods=['POST', 'GET'])
def about_rec():
    return render_template('about_rec.html', params=params)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if not session.get("ID"):
        if (request.method == 'POST'):
            S_name = request.form.get('seekername')
            S_email = request.form.get('seekeremail')
            S_pass = request.form.get('seekerpassword')
            entry5 = seeker_signin(
                seeker_name=S_name, seeker_email=S_email, seeker_pass=S_pass)
            db.session.add(entry5)
            db.session.commit()
            return render_template("login.html", params=params)
    return redirect('/Post')


@app.route("/seeker/signin", methods=['GET', 'POST'])
def SeekerSignin():
    if request.method == 'POST':
        engine = create_engine(
            "mysql+mysqldb://root:@localhost/resumescreening")
        # mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

        email = request.form['email']
        password = request.form['password']
        # email = "tamur@gmail.com"
        # password = "t123"
        # seeker_table = seeker_signin.metadata.tables["seeker_signin"]
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(seeker_signin).filter(
            seeker_signin.seeker_email == email, seeker_signin.seeker_pass == password)
        result = query.first()
        print(result)
        if result:
            session['logged_in'] = True
            session['role'] = "Seeker"
            session['ID'] = result.seeker_id
            flash("successfully logged in")
            return redirect('/Post')
            # redirect("/Post")
        else:
            flash('wrong password!')
    return render_template('login.html', params=params)


@app.route("/log_rec", methods=['POST', 'GET'])
def log_rec():
    return render_template('log_rec.html', params=params)


@app.route("/job-list", methods=['POST', 'GET'])
def job_list():
    return render_template('job-list.html', params=params)


@app.route("/job-detail", methods=['GET', 'POST'])
def job_detail():
    if (request.method == 'POST'):
        name = request.form.get('seeker_name')
        email = request.form.get('seeker_email')
        portfolio = request.form.get('seeker_portfolio')
        cv = request.form.get('seeker_cv')
        Coverletter = request.form.get('Coverletter')
        entry4 = seeker_apply(seeker_name=name, seeker_email=email,
                              seeker_portfolio=portfolio, seeker_cv=cv, seeker_coverlet=Coverletter)
        db.session.add(entry4)
        db.session.commit()
    return render_template('job-detail.html', params=params)


@app.route("/status", methods=['POST', 'GET'])
def status():
    return render_template('status.html', params=params)


@app.route("/Show_candidates", methods=['POST', 'GET'])
def Show_candidates():
    return render_template('Show_candidates.html', params=params)


@app.route("/Seeker_profile", methods=['POST', 'GET'])
def Seeker_profile():
    return render_template('Seeker_profile.html', params=params)


@app.route("/contact_rec", methods=['POST', 'GET'])
def Contact_rec():
    return render_template('contact_rec.html', params=params)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
