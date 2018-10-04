from flask import Flask, request, render_template,flash
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)


class Config(object):
    DEBUG = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/regist'
# 能在终端看到命令的sql语句
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'JSFJDBDJBVKSDFUY'

app.config.from_object(Config)
manager = Manager(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    tel = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(128), nullable=False)


class Register(FlaskForm):
    user_name = StringField('用户名:', validators=[DataRequired()])
    password1 = PasswordField('密码:', validators=[DataRequired()])
    password2 = PasswordField('重复密码:', validators=[DataRequired(), EqualTo('password1')])
    tel = IntegerField('电话号码:', validators=[DataRequired()])
    addr = StringField('家庭住址:', validators=[DataRequired()])
    submit = SubmitField('注册')


class Login(FlaskForm):
    user_name = StringField('用户名:', validators=[DataRequired()])
    password1 = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('登录')


@app.route('/', methods=['GET', 'POST'])
def login():
    myform = Login()
    try:
        if myform.validate_on_submit():
            # print(1)
            name = request.form.get('user_name')
            # print(name)
            user = User.query.filter_by(user_name=name).first()
            pwd=user.password
            if user:
                pwd1 = request.form.get('password1')
                # print(pwd)
                # 注意从输入框获取的内容类型都为字符串
                if pwd == int(pwd1):
                    return '欢迎%s登录' % user.user_name
                else:
                    # print(2)
                    flash('密码错误')
            else:
                # print(1)
                flash('该用户不存在')
        else:
            flash('登录信息有误')
    except:
        print('操作有误')
        flash('操作失败')

    return render_template('login.html', form=myform)


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    myform = Register()
    try:
        if request.method == 'POST':
            if myform.validate_on_submit():
                # print(1)
                name = myform.user_name.data
                password1 = myform.password1.data
                tel1 = myform.tel.data
                address1 = myform.addr.data
                user = User(user_name=name, password=password1, tel=tel1, address=address1)
                db.session.add(user)
                db.session.commit()
                return '注册成功'
    except:
        print('操作有误')
        flash('注册失败')
    return render_template('register.html', form=myform)


if __name__ == '__main__':
    db.create_all()
    manager.run()
