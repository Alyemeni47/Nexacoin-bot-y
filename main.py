from flask import Flask, jsonify, request
from solana.rpc.api import Client
import os

app = Flask(__name__)

# Initialize Solana client (connect to mainnet by default)
solana_client = Client("https://api.mainnet-beta.solana.com")

@app.route("/")
def home():
    return "Solana Flask Server is running! Check /balance?wallet=<address>"

@app.route("/balance")
def get_balance():
    wallet_address = request.args.get("wallet")
    if not wallet_address:
        return jsonify({"error": "Missing wallet address"}), 400
    
    try:
        balance = solana_client.get_balance(wallet_address)
        return jsonify({"wallet": wallet_address, "balance": balance["result"]["value"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
