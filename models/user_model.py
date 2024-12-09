# user_model

from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))


    def __init__(self, email, password, name, role):
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    
    def check_password(self, password):
        # إضافة رسائل التتبع هنا لرؤية ما يحدث في عملية التحقق من كلمة المرور
        print(f"Checking password: {self.password}")
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(email, password, name, role):
         hashed_password = generate_password_hash(password)
         print(f"Hashed password for {email}: {hashed_password}")  # طباعة كلمة المرور المشفرة
         new_user = User(email=email, password=hashed_password, name=name, role=role)
         db.session.add(new_user)
         db.session.commit()
         return new_user


   
    @staticmethod
    def validate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user:
         print(f"Stored password hash: {user.password}")  # طباعة كلمة المرور المشفرة
        if user.check_password(password):
           return user
        return None


