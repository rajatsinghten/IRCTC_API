from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# ----- Scraper logic -----
def fetch_trains(src, dst, date, device_id=None):
    url = "https://cttrainsapi.confirmtkt.com/api/v1/trains/search"
    params = {
        "sourceStationCode": src,
        "destinationStationCode": dst,
        "addAvailabilityCache": "true",
        "excludeMultiTicketAlternates": "false",
        "excludeBoostAlternates": "false",
        "sortBy": "DEFAULT",
        "dateOfJourney": date,
        "enableNearby": "true",
        "enableTG": "true",
        "tGPlan": "CTG-3",
        "showTGPrediction": "false",
        "tgColor": "DEFAULT",
        "showPredictionGlobal": "true"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "ApiKey": "ct-web!2$",
        "ClientId": "ct-web",
        "Content-Type": "application/json",
        "DNT": "1",
        "DeviceId": device_id or "abaa1d23-f1b4-4ef7-bd77-dfa7e67779bd",
        "Origin": "https://www.confirmtkt.com",
        "Referer": "https://www.confirmtkt.com/",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

# ----- API endpoints -----
@app.route("/search", methods=["GET", "POST"])
def search_trains():
    try:
        if request.method == "GET":
            src = request.args.get("src", "").upper()
            dst = request.args.get("dst", "").upper()
            date = request.args.get("date", "")
            device_id = request.args.get("device_id", None)
        else:  # POST
            body = request.get_json() or {}
            src = body.get("src", "").upper()
            dst = body.get("dst", "").upper()
            date = body.get("date", "")
            device_id = body.get("device_id", None)

        if not all([src, dst, date]):
            return jsonify({"error": "Missing required parameters: src, dst, date"}), 400

        full_data = fetch_trains(src, dst, date, device_id)

        trains_raw = []
        if (
            full_data.get("data") 
            and isinstance(full_data["data"], dict)
            and "trainList" in full_data["data"]
        ):
            trains_raw = full_data["data"]["trainList"]

        # Build simplified train list with availability
        trains = []
        for t in trains_raw:
            train_info = {
                "trainNumber": t.get("trainNumber"),
                "trainName": t.get("trainName"),
                "departureTime": t.get("departureTime"),
                "arrivalTime": t.get("arrivalTime"),
                "distance": t.get("distance"),
                "availability": {}
            }

            # Extract availabilityCache info per class (just availability string)
            availability_cache = t.get("availabilityCache", {})
            for cls, avail_data in availability_cache.items():
                # You can customize fields returned here
                train_info["availability"][cls] = avail_data.get("availability")

            trains.append(train_info)

        return jsonify({
            "src": src,
            "dst": dst,
            "date": date,
            "train_count": len(trains),
            "trains": trains
        })

    except requests.exceptions.HTTPError as he:
        logging.exception("HTTP error fetching trains")
        return jsonify({"error": f"Upstream API error: {he}"}), 502
    except requests.exceptions.RequestException as re:
        logging.exception("Network error fetching trains")
        return jsonify({"error": f"Network error: {re}"}), 503
    except Exception as e:
        logging.exception("Internal server error")
        return jsonify({"error": f"Server error: {e}"}), 500

# ----- Health check -----
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ConfirmTKT Train Availability API",
        "endpoints": {
            "GET /search?src=DEOS&dst=GKP&date=02-07-2025": "Search by query params",
            "POST /search": { "src": "DEOS", "dst": "GKP", "date": "02-07-2025", "device_id": "..." }
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
