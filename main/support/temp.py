from main import app , db , Models

with app.app_context():
    db.session.rollback()
    
    #db.drop_all()
    #db.create_all() 

