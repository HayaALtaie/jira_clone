#user_routes

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user_model import User
from werkzeug.security import generate_password_hash
from helper import admin_required  # التأكد من أن المسؤول فقط يمكنه إضافة مستخدمين
from models import db

user_bp = Blueprint('user', __name__)


# مسار لإضافة مستخدم جديد
@user_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('البريد الإلكتروني موجود بالفعل', 'danger')
            return redirect(url_for('user.add_user'))

    
        User.create_user(email, password, name, role)
        flash('تم إضافة المستخدم بنجاح', 'success')
        return redirect(url_for('admin.manage_users'))  # إعادة التوجيه بعد إضافة المستخدم بنجاح

    return render_template('add_user.html')

# مسار لتعديل بيانات مستخدم
@user_bp.route('/edit_user/<email>', methods=['GET', 'POST'])
@admin_required
def edit_user(email):
    user = User.query.filter_by(email=email).first()
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.role = request.form.get('role')

        db.session.commit()
        flash('تم تعديل بيانات المستخدم بنجاح', 'success')
        return redirect(url_for('admin.manage_users'))  # إعادة التوجيه بعد تعديل البيانات بنجاح

    return render_template('edit_user.html', user=user)

# مسار لحذف مستخدم
@user_bp.route('/delete_user/<email>', methods=['GET', 'POST'])
@admin_required
def delete_user(email):
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('تم حذف المستخدم بنجاح', 'success')

        return redirect(url_for('admin.manage_users'))  # إعادة التوجيه بعد الحذف

    return render_template('delete_user.html', user=user)


# # مسار لإضافة مستخدم جديد
# @user_bp.route('/add_user', methods=['GET', 'POST'])
# @admin_required  # التأكد من أن فقط المسؤولين يمكنهم إضافة مستخدمين
# def add_user():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         name = request.form.get('name')
#         role = request.form.get('role')

#         # تأكد من أن البريد الإلكتروني غير مكرر
#         if User.query.filter_by(email=email).first():
#             abort(400, description="البريد الإلكتروني موجود بالفعل")  # إرجاع خطأ إذا كان البريد موجودًا


#         # إضافة المستخدم إلى قاعدة البيانات
#         User.create_user(email,password, name, role)

#         return redirect(url_for('user.manage_users'))  # إعادة التوجيه بعد إضافة المستخدم بنجاح

#     return render_template('add_user.html')

# # مسار لتعديل بيانات مستخدم
# @user_bp.route('/edit_user/<email>', methods=['GET', 'POST'])
# @admin_required  # التأكد من أن فقط المسؤولين يمكنهم تعديل بيانات المستخدمين
# def edit_user(email):
#     user = User.query.filter_by(email=email).first()
    
#     if request.method == 'POST':
#         user.name = request.form.get('name')
#         user.email = request.form.get('email')
#         user.role = request.form.get('role')

#         db.session.commit()  # حفظ التغييرات في قاعدة البيانات

#         return redirect(url_for('user.manage_users'))  # إعادة التوجيه بعد تعديل البيانات بنجاح

#     return render_template('edit_user.html', user=user)

# # مسار لحذف مستخدم
# @user_bp.route('/delete_user/<email>', methods=['GET', 'POST'])
# @admin_required  # التأكد من أن فقط المسؤولين يمكنهم حذف مستخدمين
# def delete_user(email):
#     user = User.query.filter_by(email=email).first()

#     if request.method == 'POST':
#         if user:
#             db.session.delete(user)  # حذف المستخدم من قاعدة البيانات
#             db.session.commit()

#         return redirect(url_for('user.manage_users'))  # إعادة التوجيه بعد الحذف

#     return render_template('delete_user.html', user=user)




