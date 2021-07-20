# -*- encoding=UTF-8 -*-

from types import MethodDescriptorType
from typing import Hashable


from flask.signals import template_rendered
from sqlalchemy.sql.expression import false, true
from cuccloud import app, db
from cuccloud.models import User
from flask import render_template, redirect, request, jsonify, flash, get_flashed_messages, send_from_directory, url_for
from flask_login import login_required, login_user, logout_user, current_user
import random,os,json,hashlib,re,uuid
from flask_login import LoginManager
from sqlalchemy import and_, or_

# 登录
@app.route('/',methods=['POST','GET'])
@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'GET' and current_user.is_anonymous ==True:
        return render_template('login.html')
    elif current_user.is_anonymous !=True:
        return redirect('/index/')
    elif request.method == 'POST':
        username = request.values.get('username').strip()
        password = request.values.get('password').strip()

        if username == '' or password == '':
            return flash('用户名或密码不能为空', category='error')

        user = User.query.filter_by(username=username).first()

        if user == None:
            return flash('用户名不存在', category='error')

        m = hashlib.md5()
        m.update((password+user.salt).encode('utf-8'))
        if (m.hexdigest() != user.password):
            return flash('用户名或密码错误', category='error')

        login_user(user)

        return redirect('/index/')
    
    return render_template('login.html')

# 退出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')

# 注册
@app.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        usernickname = request.form.get('usernickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('用户已存在', category='error')
        elif username == '' or password1 == '' or password2 == '':
            flash('用户名和密码不能为空', category='error')
        elif len(username) < 5:
            flash('用户名至少5位', category='error')
        elif (detectionname(username) != True):
            flash('用户名格式不正确(只能英文和数字组合)', category='error')
        elif(detectionnick(usernickname)!=True):
            flash('昵称格式不正确', category='error')
        elif password1 != password2:
            flash('输入密码不一致', category='error')
        elif len(password1) < 5:
            flash('密码至少5位', category='error')
        elif detectionpassword(password1) != True:
            flash('密码Low', category='error')
        else:
            salt = ''.join(random.sample(
                '0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
            m = hashlib.md5()
            m.update((password1 + salt).encode('utf-8'))
            password = m.hexdigest()

            new_user = User(
                username=username, usernickname=usernickname, password=password, salt=salt)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('注册成功', category='success')
            return redirect('/index/')

    return render_template("signup.html")

# 用户名检测
def detectionname(username):
    if len(username)<=36:
        return True
    elif username.isalnum:
        return True
    return False

# 昵称检测
def detectionnick(usernickname):
    if usernickname.isprintable:
        return True
    return False

# 密码检测
def detectionpassword(password):
    if re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", password) and len(password) >= 8:
        return True
    return False



# 文件上传
@app.route('/upload/', methods={"GET","POST"})
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_ext = ''
        # 每一个用户一个文件夹
        save_dir = app.config['UPLOAD_DIR']
        current_user_dir=save_dir + str(current_user.id)
        if not os.path.exists(current_user_dir):
            os.mkdir(current_user_dir)        
        if file.filename.find('.') > 0:
            file_ext = file.filename.rsplit('.')[1].strip().lower()
        if file_ext in app.config['ALLOWED_EXT']:
            file_name = str(uuid.uuid4()).replace('-', '') + '.' + file_ext
            #url = save_to_local(file, file_name)
            file.save(os.path.join(current_user_dir,file_name))
            # if url != None:
            #     db.session.add(Image(url, current_user.id))
            #     db.session.commit()
        
        return redirect('/index/')
    else:
        return render_template('upload.html')




# 主页
@app.route('/index/')
@login_required
def index():
    
    return render_template('index.html')
