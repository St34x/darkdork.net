from app.models import User, TokenPricing  
from app import db, create_app
app = create_app()

with app.app_context():
    db.create_all()
    new_user = User(username='St34x', is_admin=True)
    new_user.set_password('Unseeing4-Sage1-Prepaid9-Enticing5-Unseated2-Dispute7-Hardwired1-Sushi1')  # Set a secure password
    db.session.add(new_user)
    incoming_price = TokenPricing(type='incoming', price_per_million=7.5)
    outgoing_price = TokenPricing(type='outgoing', price_per_million=2.5)
    db.session.add(incoming_price)
    db.session.add(outgoing_price)
    db.session.commit()
