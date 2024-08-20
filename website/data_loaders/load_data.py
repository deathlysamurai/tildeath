from .user_loader import load_users

def run_data_loaders(app, db):
    load_users(app, db)