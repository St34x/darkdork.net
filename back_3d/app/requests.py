# app/requests.py

from .models import *

def fetch_token_pricing():
    incoming_pricing = TokenPricing.query.filter_by(type='incoming').first()
    outgoing_pricing = TokenPricing.query.filter_by(type='outgoing').first()
    return incoming_pricing, outgoing_pricing

def calculate_total_cost(incoming_tokens, outgoing_tokens, incoming_pricing, outgoing_pricing):
    if incoming_pricing and outgoing_pricing:
        total_cost = (
            (incoming_tokens * (incoming_pricing.price_per_million / 1e6)) +
            (outgoing_tokens * (outgoing_pricing.price_per_million / 1e6))
        )
        return total_cost
    return 0  # Default to 0 if pricing information is not available


def update_token_transactions_in_db(user_id, incoming, outgoing):
    # Add a new token transaction record in the database
    new_transaction = User(
        user_id=user_id,
        incoming_tokens=incoming,
        outgoing_tokens=outgoing,
    )
    db.session.add(new_transaction)
    db.session.commit()
