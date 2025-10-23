from models import db, User

SEED_USERS = [
    {
        'username': 'user', 
        'email': 'user@example.com',
        'password': 'Pass123!'
    },
    {
        'username': 'admin', 
        'email': 'admin@example.com',
        'password': 'Pass456!'
    }
]

def seed_db():
    
    users_added = 0

    print("\n--- Inizio Seeding Utenti ---")

    for data in SEED_USERS:
        username = data['username']
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            new_user = User(
                username=username, 
                email=data['email'],
                password=data['password']
            )
            db.session.add(new_user)
            users_added += 1
            print(f"Utente '{username}' aggiunto.")
        else:
            print(f"Utente '{username}' già presente. Salto.")

    try:
        db.session.commit()
        print(f"Seeding Utenti completato. ({users_added} nuovi utenti inseriti)")
    except Exception as e:
        db.session.rollback()
        print(f"ERRORE irreversibile durante il commit del seeding: {e}")
