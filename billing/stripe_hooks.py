import os


def handle_webhook(payload: bytes, signature: str) -> dict:
    # Scaffolding only. Verify with stripe.Webhook.construct_event
    # then meter usage against STRIPE_CUSTOMER_ID / HOST_PLAN.
    _ = payload, signature, os.getenv("STRIPE_WEBHOOK_SECRET")
    return {"received": True}
