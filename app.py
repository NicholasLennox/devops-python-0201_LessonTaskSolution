import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
environment = os.environ.get("ENVIRONMENT")
debug = os.environ.get("DEBUG", "false").lower() == "true"

contacts = [
    {"id": 1, "name": "Alice Bloom", "phone": "555-0101"},
    {"id": 2, "name": "Bob Crane", "phone": "555-0102"}
]

next_contact_id = 3

@app.route("/health")
def health():
    return {
        "status": "ok",
        "environment": environment,
        "port": port
    }

@app.route("/contacts", methods=["GET"])
def get_contacts():
    return contacts

@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    return {"error": "Contact not found"}, 404

@app.route("/contacts", methods=["POST"])
def create_contact():
    global next_contact_id
    data = request.get_json()
    if not data or "name" not in data or "phone" not in data:
        return {"error": "Missing required fields: name and phone"}, 400
    contact = {
        "id": next_contact_id,
        "name": data["name"],
        "phone": data["phone"]
    }
    next_contact_id += 1
    contacts.append(contact)
    return contact, 201

if __name__ == "__main__":
    app.run(port=port, debug=debug)