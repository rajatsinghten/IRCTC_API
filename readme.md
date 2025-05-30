
# ConfirmTKT Train Availability API

This API provides train availability and details by querying the ConfirmTKT train data API.

## Base URL

`https://traininfo-diik.onrender.com`



## Endpoints

### 1. Health Check

`GET /`

Returns a welcome message and available endpoints.

#### Example Request:

```bash
curl https://traininfo-diik.onrender.com/
```

#### Response:

```json
{
  "message": "ConfirmTKT Train Availability API",
  "endpoints": {
    "GET /search?src=DEOS&dst=GKP&date=02-07-2025": "Search by query params",
    "POST /search": { "src": "DEOS", "dst": "GKP", "date": "02-07-2025", "device_id": "..." }
  }
}
```

---

### 2. Search Trains

#### `GET /search`

Search trains by query parameters.

##### Query Parameters:

| Parameter   | Required | Description                        |
| :---------- | :------- | :--------------------------------- |
| `src`       | Yes      | Source station code (e.g., `DEOS`) |
| `dst`       | Yes      | Destination station code (e.g., `GKP`) |
| `date`      | Yes      | Date of journey (format: `DD-MM-YYYY`) |
| `device_id` | No       | Optional device ID string          |

##### Example GET Request:

```bash
curl "https://traininfo-diik.onrender.com/search?src=DEOS&dst=GKP&date=02-07-2025"
```

#### `POST /search`

Search trains by JSON body.

##### Request Body (JSON):

```json
{
  "src": "DEOS",
  "dst": "GKP",
  "date": "02-07-2025",
  "device_id": "optional-device-id"
}
```

##### Example POST Request:

```bash
curl -X POST https://traininfo-diik.onrender.com/search \
-H "Content-Type: application/json" \
-d '{"src":"DEOS", "dst":"GKP", "date":"02-07-2025"}'
```

---

## Response Format

The response JSON contains train data, including a list of trains and their availability by class.

#### Example (simplified):

```json
{
  "data": {
    "trainList": [
      {
        "trainName": "RAPTI SAGAR EXP",
        "trainNumber": "12521",
        "availabilityCache": {
          "1A": { "availability": "PQWL1/WL1", "fare": "5005" },
          "3A": { "availability": "AVAILABLE-0008", "fare": "2035" }
        },
        "..." : "..."
      }
    ]
  }
}
```

---

## Notes

* **`src`**, **`dst`**, and **`date`** parameters are **mandatory**.
* The **`device_id`** parameter is optional and can be used to set a unique device identifier.
* If parameters are missing or invalid, the API responds with an error and HTTP status code **400**.
* The API forwards any upstream errors with appropriate HTTP status codes.

