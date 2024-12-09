#helpers.py

from flask import session, redirect, url_for
from functools import wraps

# ديكوراتور للتحقق إذا كان المستخدم مسجلاً
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function



# ديكوراتور للتحقق إذا كان المستخدم هو مدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['role'] != 'admin':
            return redirect(url_for('auth.login'))  # إعادة التوجيه إلى صفحة تسجيل الدخول
        return f(*args, **kwargs)
    return decorated_function
