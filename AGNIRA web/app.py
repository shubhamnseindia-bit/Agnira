from flask import Flask, render_template , jsonify , request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def calculate_rate(vehicle, weight, distance, diesel_price=90):
    vehicles = {
        "7ft":  {"c": 1.5, "r": 18,  "m": 35},
        "8ft":  {"c": 2.5, "r": 22,  "m": 18},
        "10ft": {"c": 3.5, "r": 28,  "m": 14},
        "14ft": {"c": 7,   "r": 36,  "m": 7},
        "17ft": {"c": 9,   "r": 42,  "m": 6},
        "19ft": {"c": 12,  "r": 48,  "m": 5.5},
        "22ft": {"c": 15,  "r": 58,  "m": 5},
        "24ft": {"c": 18,  "r": 62,  "m": 4.5},
        "32sxl":{"c": 20,  "r": 78,  "m": 3.5},
        "32mxl":{"c": 24,  "r": 82,  "m": 3.5},
        "40odc":{"c": 30,  "r": 120, "m": 2.8},
    }

    if vehicle not in vehicles:
        return {"error": "Select vehicle"}
    if weight <= 0 or distance <= 0:
        return {"error": "Invalid input"}
    if weight > vehicles[vehicle]["c"]:
        return {"error": "Weight exceeds capacity"}

    v = vehicles[vehicle]
    diesel = (distance / v["m"]) * diesel_price
    driver = 3500 if distance <= 800 else 7000
    toll = 3000 if distance <= 800 else 7000
    operating = diesel + driver + toll + (distance * 4)
    final = max(operating * 1.17, distance * v["r"])

    return {
        "finalFreight": round(final),
        "breakdown": {
            "diesel": round(diesel),
            "driver": driver,
            "toll": toll,
            "marketFreight": round(distance * v["r"]),
        },
    }






uri = "mongodb+srv://AGNIRA_L:Subhamsingh2004@agniradb.j82svtd.mongodb.net/?appName=AGNIRADB"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


app = Flask(__name__)



@app.route("/api/calculate-freight", methods=["POST"])
def api_calculate_freight():
    payload = request.get_json() or {}
    vehicle = payload.get("vehicle")
    weight = float(payload.get("weight", 0))
    distance = float(payload.get("distance", 0))
    diesel_price = float(payload.get("dieselPrice", 90))

    result = calculate_rate(vehicle, weight, distance, diesel_price)
    return jsonify(result), 200

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/freight-calculator')
def freight_calculator():
    return render_template('freightcalculator.html')

@app.route('/vendorcorner')
def vendorcorner():
    return render_template('vendor.html')

@app.route("/fleetownerdb", methods=["POST"])
def fleetownerdb():
    # If you send JSON from frontend (fetch with body: JSON.stringify(...))
    data = request.get_json()  # parses JSON into a Python dict

    db = client.get_database('VENDORS')
    collection = db.get_collection('FLEET OWNERS')
    collection.insert_one(data)

    return jsonify({
        "status": "success",
        "message": "Data received in backend",
    }), 200

@app.route("/transporterdb", methods=["POST"])
def transporterdb():
    # If you send JSON from frontend (fetch with body: JSON.stringify(...))
    data = request.get_json()  # parses JSON into a Python dict

    db = client.get_database('VENDORS')
    collection = db.get_collection('TRANSPORTERS')
    collection.insert_one(data)

    return jsonify({
        "status": "success",
        "message": "Data received in backend",
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 
