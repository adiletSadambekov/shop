from project_db import Products, Data_users
from settings_project import con, secr_key
from author import UserLogin
from form_users import TempLogin, Register, Test_form
from flask import Flask, render_template, url_for, request, flash, session, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__ )
app.config['SECRET_KEY'] = secr_key

refs = [{'name': 'Главное', 'url': '/'},
{'name': 'Каталог товаров', 'url': '/score'},
{'name': 'В тренде', 'url': '#'},
{'name': 'Профиль', 'url': '/profile'}]

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Чтобы получить доступ к странице, необходимо войти в профиль'
login_manager.login_message_category = 'success'

dbase = None
@app.before_request
def before_request():
    global dbase
    dbase = Data_users(con)

@app.route('/')
def index():
    
    p = Products(con).get_topprod('5')
    return render_template('index.html', products=p, title='Добро пожаловать', refs = refs)

@app.route('/score')
def score():
    
    with con:
        with con.cursor() as cur:
            cur.execute('select id, name, description, price from product;')
            red = cur.fetchall()
            inf = []
            for r in red:
                i = {}
                i['product_id'] = r[0]
                i['name'] = r[1]
                i['description'] = r[2]
                i['price'] = r[3]
                inf.append(i)
    return render_template('catalog.html', title='Магазин', inf=inf, refs = refs)

 
@app.route('/product/<int:product_id>')
def showproduct(product_id):
    id = ((product_id,))
    with con:
        with con.cursor() as cur:
            cur.execute("""select name, description, price from product where id = %s;""",
            (id))
            red = cur.fetchall()
            product = []
            for r in red:
                i = {}
                i['name'] = r[0]
                i['description'] = r[1]
                i['price'] = r[2]
                product.append(i)
    return render_template('product.html', title='The product', product=product, refs=refs)




@app.route('/register', methods=["POST", "GET"])
def register():
    form = Register()
    if form.validate_on_submit():
        password = generate_password_hash(str(form.psw2.data))
        r = dbase.adduser(form.name.data, form.surname.data, form.email.data, form.phone.data, password)
        # if r == True:
        #     flash('Авторизация прошла успешна!')
        #     return redirect(url_for('login'))
    return render_template('authenticated.html', title="Регистрация", refs = refs, form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect('profile')
    form = TempLogin()
    if form.validate_on_submit():
        email = form.email()
        user = dbase.getUseremail(email)
        if user and check_password_hash(user[0]['password'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        flash('не верный пароль или логин')
    return render_template('entrance.html', title='вход', refs=refs, form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html', title='профиль', refs=refs)

@app.route('/testpage', methods=['POST', 'GET'])
def test_page():
    form = Test_form()
    return render_template('test.html', title='test_page', refs=refs, f=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из профиля', 'success')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

@app.errorhandler(404)
def error404(error):
    return render_template('error404.html', refs=refs), 404


if __name__ == '__main__':
    app.run(debug=True)
