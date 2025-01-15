from app import app, db, User, Article

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # 创建测试用户
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    init_db() 