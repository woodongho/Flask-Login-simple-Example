# Uhotax Nomu program practice
# 동호님 저 신록입니다.


from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy

# 초기화
app = Flask(__name__)

# 초기화 - SQLAlchemy
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uhotax.db'
# 아래 두 줄 넣는게 맞는지?
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


# # Create user table
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(80))
#     cName = db.Column(db.String(80))
#     cUsername = db.Column(db.String(80))
#     cNumber = db.Column(db.String(80))
#     cAddress = db.Column(db.String(80))
#
#     humans = db.relationship('Human', backref='author', lazy=True)
#
#     def __init__(self, username, password, cName, cUsername, cNumber, cAddress):
#          self.username = username
#          self.password = password
#          self.cName = cName
#          self.cUsername = cUsername
#          self.cNumber = cNumber
#          self.cAddress = cAddress


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
    dailyWorkingHourStart = db.Column(db.String)
    dailyWorkingHourEnd = db.Column(db.String)
    breakTimeStart = db.Column(db.String)
    breakTimeEnd = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Human {}>'.format(self.user_id)


# # Create Registrations table
# class Human(db.Model):
#     Registration_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     number = db.Column(db.String(80))
#     address = db.Column(db.String(80))
#     registrationNumber = db.Column(db.String(80))
#     startdate = db.Column(db.String)
#     position = db.Column(db.String(80))
#     task = db.Column(db.String(80))
#     birthday = db.Column(db.String)
#     gender = db.Column(db.String(80))
#     phoneNumber = db.Column(db.String(80))
#     accountNumber = db.Column(db.String)
#     yearSalaryInput = db.Column(db.INTEGER)
#     meal = db.Column(db.INTEGER)
#     carCost = db.Column(db.Integer)
#     childcareAllowance = db.Column(db.INTEGER)
#     otherAllowance = db.Column(db.INTEGER)
#     monthlyWorkingHour = db.Column(db.INTEGER)
#     monthlyOvertime = db.Column(db.INTEGER)
#     dailyWorkingHourStart = db.Column(db.String)
#     dailyWorkingHourEnd = db.Column(db.String)
#     breakTimeStart = db.Column(db.String)
#     breakTimeEnd = db.Column(db.String)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#
#     def __init__(self, name, number, address, registrationNumber, startdate, position, task,
#                  birthday, gender, phoneNumber, accountNumber, yearSalaryInput, meal, carCost,
#                  childcareAllowance, otherAllowance, monthlyWorkingHour, monthlyOvertime,
#                  dailyWorkingHourStart, dailyWorkingHourEnd, breakTimeStart, breakTimeEnd, user_id):
#         self.name = name
#         self.number = number
#         self.address = address
#         self.registrationNumber = registrationNumber
#         self.startdate = startdate
#         self.position = position
#         self.task = task
#         self.birthday = birthday
#         self.gender = gender
#         self.phoneNumber = phoneNumber
#         self.accountNumber = accountNumber
#         self.yearSalaryInput = yearSalaryInput
#         self.meal = meal
#         self.carCost = carCost
#         self.childcareAllowance = childcareAllowance
#         self.otherAllowance = otherAllowance
#         self.monthlyWorkingHour = monthlyWorkingHour
#         self.monthlyOvertime = monthlyOvertime
#         self.dailyWorkingHourStart = dailyWorkingHourStart
#         self.dailyWorkingHourEnd = dailyWorkingHourEnd
#         self.breakTimeStart = breakTimeStart
#         self.breakTimeEnd = breakTimeEnd
#         self.user_id = user_id


# route

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hInformationInput')
def hInformationInput():
    return render_template('hInformationInput.html')


# 메인페이지 로그인 상태일 때랑 아닐 때 참조용
# @app.route('/', methods=['GET', 'POST'])
# def home():
# 	""" Session control"""
# 	if not session.get('logged_in'):
# 		return render_template('index.html')
# 	else:
# 		if request.method == 'POST':
# 			username = getName(request.form['username'])
# 			return render_template('index.html', data=getFollowedBy(username))
# 		return render_template('index.html')


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


# relationship은 맺었는데, 아래처럼 request를 통해 html에서 받아온 데이터를 db에 add하는 중, user_id는 form이 없으니
# 다른 인자들과 같이 써주면 에러나고..그래서 user_id를 기존 db에서 찾는 형태로 해 본 것인데..이건 아님..
# 신규사원등록
@app.route('/registrations/', methods=['POST'])
def registrations():
        new_human = Human(name=request.form['hName'], number=request.form['hNumber'],
                          address=request.form['hAddress'], registrationNumber=request.form['hRegistrationNumber'],
                          startdate=request.form['hStartDate'], position=request.form['hPosition'],
                          task=request.form['hTask'], birthday=request.form['hBirthday'],
                          gender=request.form['hGender'], phoneNumber=request.form['hPhoneNumber'],
                          accountNumber=request.form['hAccountNumber'], yearSalaryInput=request.form['hYearSalaryInput'],
                          meal=request.form['hMeal'], carCost=request.form['hCarCost'],
                          childcareAllowance=request.form['hChildcareAllowance'],
                          otherAllowance=request.form['hOtherAllowance'],
                          monthlyWorkingHour=request.form['hMonthlyWorkingHour'],
                          monthlyOvertime=request.form['hMonthlyOvertime'],
                          dailyWorkingHourStart=request.form['hDailyWorkingHourStart'],
                          dailyWorkingHourEnd=request.form['hDailyWorkingHourEnd'],
                          breakTimeStart=request.form['hBreakTimeStart'], breakTimeEnd=request.form['hBreakTimeEnd'],
                          )
        db.session.add(new_human)
        db.session.commit()
        return render_template('hInformationInput.html')


# @app.route('/registrations/', methods=['GET'])
# def read_registrations():
#     registrations = list(db.Human.find({}, {'_id': 0}))
#     return jsonify({'result': 'success', 'registrations': registrations})

# @app.route('/registrations/', methods=['GET'])
# def read_registrations():
#     registrations = list(db.Human.find({}, {'_id': 0}))
#     return jsonify({'result': 'success', 'registrations': registrations})


# Logout Form
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))



# # 이거 가지고 특정 유저만 뜨는 거 해보자
# @app.route('/<username>')
# def user_timeline(username):
#     """Display's a users tweets."""
#     profile_user = query_db('select * from user where username = ?',
#                             [username], one=True)
#     if profile_user is None:
#         abort(404)
#     followed = False
#     if g.user:
#         followed = query_db('''select 1 from follower where
#             follower.who_id = ? and follower.whom_id = ?''',
#             [session['user_id'], profile_user['user_id']],
#             one=True) is not None
#     return render_template('timeline.html', messages=query_db('''
#             select message.*, user.* from message, user where
#             user.user_id = message.author_id and user.user_id = ?
#             order by message.pub_date desc limit ?''',
#             [profile_user['user_id'], PER_PAGE]), followed=followed,
#             profile_user=profile_user)
#
#
# # 애드 메세지 할 때 특정 아이디 값 주는 것? 릴레이션 연구
# @app.route('/add_message', methods=['POST'])
# def add_message():
#     """Registers a new message for the user."""
#     if 'user_id' not in session:
#         abort(401)
#     if request.form['text']:
#         g.db.execute('''insert into
#             message (author_id, text, pub_date)
#             values (?, ?, ?)''', (session['user_id'],
#                                   request.form['text'],
#                                   int(time.time())))
#         g.db.commit()
#         flash('Your message was recorded')
#     return redirect(url_for('timeline'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
