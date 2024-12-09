#app.py

from models import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import Blueprint

# تهيئة التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# إعدادات الاتصال بقاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite قاعدة البيانات
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # إيقاف تتبع التعديلات

# تهيئة SQLAlchemy
# db = SQLAlchemy(app)

db.init_app(app)
# راوت للصفحة الرئيسية (index)
@app.route('/')
def index():
    return render_template('index.html')  # عرض القالب index.html




# استيراد الـ Blueprints
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp





# تسجيل الـ Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(task_bp, url_prefix='/task')
app.register_blueprint(user_bp, url_prefix='/user')


# إنشاء الجداول في قاعدة البيانات عند بدء التطبيق لأول مرة
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
