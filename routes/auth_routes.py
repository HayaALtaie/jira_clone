#auth_routes


from flask import Blueprint, render_template, request, redirect, url_for, session,abort
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User  # استيراد نموذج المستخدم

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        # تحقق إذا كان البريد الإلكتروني موجوداً مسبقاً في قاعدة البيانات
        if User.query.filter_by(email=email).first():
            return "البريد الإلكتروني موجود مسبقاً", 400

        # تعيين الدور إلى 'admin'
        role = 'admin'
        

        # إضافة المستخدم إلى قاعدة البيانات
        new_user = User.create_user(email,password, name, role)

        # تسجيل الدخول تلقائياً
        session['user'] = email
        session['role'] = role

        # التوجيه إلى لوحة تحكم الإدمن
        return redirect(url_for('auth.login'))  # التوجيه إلى لوحة تحكم الإدمن

    return render_template('register_admin.html')  # عرض صفحة التسجيل للإدمن فقط


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # طباعة البريد وكلمة المرور المدخلة للمساعدة في تتبع المشكلة
        print(f"Login attempt with email: {email} and password: {password}")

        # استخدام validate_user للتحقق من البريد الإلكتروني وكلمة المرور
        user = User.validate_user(email, password)

        if user:
            # إذا كانت كلمة المرور صحيحة، نقوم بتسجيل الدخول
            session['user'] = email
            session['role'] = user.role  # تخزين الدور (إدمن أو مستخدم عادي)

            # توجيه المستخدم إلى لوحة التحكم بناءً على الدور
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))  # لوحة تحكم الإدمن
            else:
                return redirect(url_for('dashboard.user_dashboard'))  # لوحة تحكم المستخدم العادي
        else:
            print("Password is incorrect or user not found")

        return "البريد الإلكتروني أو كلمة المرور غير صحيحة", 400  # رسالة في حالة الفشل

    return render_template('login.html')  # عرض نموذج تسجيل الدخول عند الطلب GET






@auth_bp.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        # تأكد من أن البريد الإلكتروني غير مكرر
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            abort(400, description="البريد الإلكتروني موجود بالفعل")  # إرجاع خطأ إذا كان البريد موجودًا


        # إضافة المستخدم إلى قاعدة البيانات
        user = User.create_user(email, password, name, 'user')

        # تسجيل الدخول مباشرة بعد التسجيل
        session['user'] = user.email
        session['role'] = user.role

        # إعادة التوجيه إلى صفحة تسجيل الدخول بعد التسجيل بنجاح
        return redirect(url_for('auth.login'))

    return render_template('register_user.html')  # عرض نموذج التسجيل

# مسار تسجيل الخروج
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))
