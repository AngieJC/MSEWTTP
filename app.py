from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='hehe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## 注册
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username,password,password2]):
            flash ('参数不完整')
        elif password != password2:
            flash ('两次密码不一致，请重新输入')
        else:
            new_user = Users(username=username,password=password,id=None)
            db.session.add(new_user)
            db.session.commit()
            return ''
    return render_template('register.html')


## 登录
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username,password]):
            flash ('参数不完整')
        user = Users.query.filter(Users.username==username,Users.password==password).first()
        print(user.username)
        print(user.password)
        if user:
            return '登录成功'
        else:
            return "login fail"
    return render_template('login.html')



# 定义一个用户及密码的数据库
class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(16))


if __name__ == '__main__':
    app.run(debug=True)