from flask import Flask, render_template, request, jsonify
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Function to get the nearest hospitals (Using Google Places API)
def get_nearest_hospitals(location):
    google_places_api_key = 'AIzaSyA_HQsbcV1qwwUlamb0U-lT98gaj_I4caM'  # Replace with your Google Places API Key
    geolocator = Nominatim(user_agent="health_advisor")
    location = geolocator.geocode(location)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=hospital&key={google_places_api_key}'
        response = requests.get(url)
        hospitals = response.json().get('results', [])
        return [{"name": hospital["name"], "address": hospital["vicinity"]} for hospital in hospitals]
    return []

# Function to get prevention advice (based on symptoms - mock data for now)
def get_prevention_advice(symptoms):
    advice = {
        "fever": "Drink plenty of fluids, rest, and take fever-reducing medication like paracetamol.",
        "headache": "Rest in a dark room, drink water, and consider taking ibuprofen.",
        "cough": "Stay hydrated, use honey, and avoid irritants like smoke.",
    }
    response = {}
    for symptom in symptoms:
        response[symptom] = advice.get(symptom, "No advice available.")
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_hospitals', methods=['GET'])
def get_hospitals():
    location = request.args.get('location')
    if location:
        hospitals = get_nearest_hospitals(location)
        return jsonify(hospitals)
    return jsonify({"error": "Location not provided"}), 400

@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    symptoms = data.get("symptoms", [])
    if symptoms:
        advice = get_prevention_advice(symptoms)
        return jsonify(advice)
    return jsonify({"error": "Symptoms not provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
