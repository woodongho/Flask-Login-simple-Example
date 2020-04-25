# Uhotax Nomu program practice


from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy

# 초기화
app = Flask(__name__)

# 초기화 - SQLAlchemy
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uhotax.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# Create user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    cName = db.Column(db.String(80))
    cUsername = db.Column(db.String(80))
    cNumber = db.Column(db.String(80))
    cAddress = db.Column(db.String(80))

    humans = db.relationship('Human', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# Create Registrations table
class Human(db.Model):
    Registration_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    number = db.Column(db.String(80))
    address = db.Column(db.String(80))
    registrationNumber = db.Column(db.String(80))
    startdate = db.Column(db.String)
    position = db.Column(db.String(80))
    task = db.Column(db.String(80))
    birthday = db.Column(db.String)
    gender = db.Column(db.String(80))
    phoneNumber = db.Column(db.String(80))
    accountNumber = db.Column(db.String)
    yearSalaryInput = db.Column(db.INTEGER)
    meal = db.Column(db.INTEGER)
    carCost = db.Column(db.Integer)
    childcareAllowance = db.Column(db.INTEGER)
    otherAllowance = db.Column(db.INTEGER)
    monthlyWorkingHour = db.Column(db.INTEGER)
    monthlyOvertime = db.Column(db.INTEGER)
    dailyWorkingHour = db.Column(db.String(80))
    breakTime = db.Column(db.String(80))
    hourlyWage = db.Column(db.INTEGER)
    monthlyBasicSalary = db.Column(db.INTEGER)
    monthlyOvertimeAllowance = db.Column(db.INTEGER)
    monthlyTotalSalrary = db.Column(db.INTEGER)
    yearSalary = db.Column(db.INTEGER)
    mothlySalary = db.Column(db.INTEGER)
    monthlyTotalWorkingHour = db.Column(db.INTEGER)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Human {}>'.format(self.user_id)


# 최저시급 상수로 함, 상수 선언은 따로 안함
minimumHourlyWage = 8590

# route

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hInformationInput')
def hInformationInput():
    return render_template('hInformationInput.html')

@app.route('/laborManagement')
def laborManagement():
    return render_template('laborManagement.html')

@app.route('/salaryContract')
def salaryContract():
    return render_template('salaryContract.html')


# Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['user_id'] = data.id
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return '아이디 또는 비밀번호가 잘못 되었습니다.'
        except:
            return "Can`t Login"


# Register Form
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'],
                        cName=request.form['cName'], cUsername=request.form['cUsername'],
                        cNumber=request.form['cNumber'], cAddress=request.form['cAddress'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


# 신규사원등록
@app.route('/registrations/', methods=['POST', 'GET'])
def registrations():
    yearSalaryInput = int(request.form['hYearSalaryInput'])
    meal = int(request.form['hMeal'])
    carCost = int(request.form['hCarCost'])
    childcareAllowance = int(request.form['hChildcareAllowance'])
    otherAllowance = int(request.form['hOtherAllowance'])
    monthlyWorkingHour = int(request.form['hMonthlyWorkingHour'])
    monthlyOvertime = int(request.form['hMonthlyOvertime'])
    hourlyWage = int(((yearSalaryInput / 12) - meal - carCost - childcareAllowance - otherAllowance) / (
            monthlyWorkingHour + monthlyOvertime * 1.5))
    monthlyBasicSalary = hourlyWage * monthlyWorkingHour
    monthlyOvertimeAllowance = hourlyWage * monthlyOvertime * 1.5
    monthlyTotalSalrary = monthlyBasicSalary + monthlyOvertimeAllowance + meal + carCost + childcareAllowance + \
                          otherAllowance
    yearSalary = monthlyTotalSalrary * 12
    mothlySalary = monthlyTotalSalrary
    monthlyTotalWorkingHour = monthlyWorkingHour + monthlyOvertime

    if hourlyWage < minimumHourlyWage:
        return ("최저시급 위반입니다! 다시 등록해주세요. 2020년 최저시급은 8,590원이고, 최저시급을 늘리기 위해서는 식대,"
                " 자가차량유지비, 출산 및 육아수당을 빼주거나, 월고정연장시간을 줄이세요.")
    else:
        new_human = Human(yearSalaryInput=request.form['hYearSalaryInput'], meal=request.form['hMeal'],
                          carCost=request.form['hCarCost'], childcareAllowance=request.form['hChildcareAllowance'],
                          otherAllowance=request.form['hOtherAllowance'], hourlyWage=hourlyWage,
                          monthlyBasicSalary=monthlyBasicSalary, monthlyOvertimeAllowance=monthlyOvertimeAllowance,
                          monthlyTotalSalrary=monthlyTotalSalrary, yearSalary=yearSalary, mothlySalary=mothlySalary,
                          monthlyTotalWorkingHour=monthlyTotalWorkingHour, name=request.form['hName'],
                          number=request.form['hNumber'],
                          address=request.form['hAddress'], registrationNumber=request.form['hRegistrationNumber'],
                          startdate=request.form['hStartDate'], position=request.form['hPosition'],
                          task=request.form['hTask'], birthday=request.form['hBirthday'],
                          gender=request.form['hGender'], phoneNumber=request.form['hPhoneNumber'],
                          accountNumber=request.form['hAccountNumber'],
                          monthlyWorkingHour=request.form['hMonthlyWorkingHour'],
                          monthlyOvertime=request.form['hMonthlyOvertime'],
                          dailyWorkingHour=request.form['hDailyWorkingHour'],
                          breakTime=request.form['hBreakTime'],
                          user_id=session['user_id'])
        db.session.add(new_human)
        db.session.commit()
    return render_template('hInformationInput.html')

# @app.route('/registrations/', methods=['GET'])
# def read_registrations():
#     registrations = list(db.Human.find({}, {'_id': 0}))
#     return jsonify({'result': 'success', 'registrations': registrations})


# Logout Form
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('home'))

# # 회사명과 주소 user db로부터 땡겨오는 것
# @app.route("/users/<cid>/companyName")
# def get_users(id):
#     user_data = User.query.filter_by(company_id=id).all()
#     users = []
#     for u in user_data:
#         data = {
#             "cid": u.id,
#             "cName": u.cName,
#             "cUsername": u.cUsername,
#             "cNumber": u.cNumber,
#             "cAddress": u.cAddress,
#         }
#         users.append(data)
#     return jsonify(users)

# # 회사명과 주소 user db로부터 땡겨오는 것
# @app.route("/users/companyName")
# def get_users(id):
#     user_data = User.query.filter_by(company_name=cName)
#     users = []
#     for u in user_data:
#         data = {
#             "cName": u.cName,
#         }
#         users.append(data)
#     return jsonify(users)

# 회사명과 주소 user db로부터 가져와 출력
# @app.route("/companyName")
# def show_tables():
#     queries = db.session.query(User)
#     cName = [dict(cName=cName)]
#     print(cName)


# 신규 등록한 사원명 human db로부터 땡겨오는 것
@app.route("/users/<id>/humans")
def get_humans(id):
    human_data = Human.query.filter_by(user_id=id).all()
    humans = []
    for h in human_data:
        data = {
            "id": h.Registration_id,
            "name": h.name,
            "number": h.number,
            "address": h.address,
            "registrationNumber": h.registrationNumber,
            "startdate": h.startdate,
            "position": h.position,
            "task": h.task,
            "birthday": h.birthday,
            "gender": h.gender,
            "phoneNumber": h.phoneNumber,
            "accountNumber": h.accountNumber,
            "yearSalaryInput": h.yearSalaryInput,
            "meal": h.meal,
            "carCost": h.carCost,
            "childcareAllowance": h.childcareAllowance,
            "otherAllowance": h.otherAllowance,
            "monthlyWorkingHour": h.monthlyWorkingHour,
            "monthlyOvertime": h.monthlyOvertime,
            "dailyWorkingHour": h.dailyWorkingHour,
            "breakTime": h.breakTime,
            "hourlyWage": h.hourlyWage,
            "monthlyBasicSalary": h.monthlyBasicSalary,
            "monthlyOvertimeAllowance": h.monthlyOvertimeAllowance,
            "monthlyTotalWorkingHour": h.monthlyTotalWorkingHour
        }
        humans.append(data)
    return jsonify(humans)



if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
