from .data import users

def load_users(app, db): 
    with app.app_context():
        for user in users:
            db.session.add(user)
        db.session.commit()
        print('Users created.')