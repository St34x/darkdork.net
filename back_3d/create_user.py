from app.models import User, TokenPricing  
from app import db, create_app
app = create_app()

with app.app_context():
    db.create_all()
    new_user = User(username='MasterOfUnivers', is_admin=True)
    new_user.set_password('Probation6?Polygon80Hydroxide6$Collected2^Ranking18Enticing7@Why96Erased5=Senorita2+Woven1')  # Set a secure password
    db.session.add(new_user)
    incoming_price = TokenPricing(type='incoming', price_per_million=7.5)
    outgoing_price = TokenPricing(type='outgoing', price_per_million=2.5)
    db.session.add(incoming_price)
    db.session.add(outgoing_price)
    db.session.commit()
