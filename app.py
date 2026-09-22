#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from billing.stripe_hooks import handle_webhook

load_dotenv()
app = Flask(__name__)


@app.get("/health")
def health():
    return {"ok": True, "station": os.getenv("STATION_NAME", "PerpTV")}


@app.post("/stripe/webhook")
def stripe_webhook():
    return jsonify(handle_webhook(request.data, request.headers.get("Stripe-Signature", "")))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8088)
