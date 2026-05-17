from app import create_app, db
from app.models import User

app = create_app()

def initialize_database():
    with app.app_context():
        db.create_all()
        # Initialize default user if not exists
        if not User.query.filter_by(id=1).first():
            default_user = User(username='demo_user', email='demo@example.com', password='password123')
            db.session.add(default_user)
            db.session.commit()
            print("Initialized default demo user.")

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, port=5000)
