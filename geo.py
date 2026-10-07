"""Find nearby hospitals / clinics / doctors.

1. FACILITIES: a built-in sample list (works offline). Coordinates are
   APPROXIMATE - replace with your hospital's real doctors and addresses.
2. live_search(): queries OpenStreetMap (Nominatim + Overpass) using `requests`.
"""
import math
import requests

SPECIALTIES = [
    "General Physician", "Cardiologist", "Pediatrician", "Gynecologist",
    "Pulmonologist", "Endocrinologist", "Dermatologist", "Neurologist", "Emergency",
]

_ALL = SPECIALTIES

# Sample data: edit/extend freely (name, area, lat, lon, specialties)
FACILITIES = [
    {"name": "Aga Khan University Hospital", "area": "Stadium Road", "lat": 24.8921, "lon": 67.0742, "spec": _ALL},
    {"name": "Liaquat National Hospital", "area": "Stadium Road", "lat": 24.8935, "lon": 67.0690, "spec": _ALL},
    {"name": "Jinnah Postgraduate Medical Centre (JPMC)", "area": "Rafiqui Shaheed Road", "lat": 24.8508, "lon": 67.0457, "spec": _ALL},
    {"name": "Civil Hospital Karachi", "area": "Saddar", "lat": 24.8574, "lon": 67.0105, "spec": _ALL},
    {"name": "Abbasi Shaheed Hospital", "area": "North Nazimabad", "lat": 24.9253, "lon": 67.0394, "spec": _ALL},
    {"name": "Ziauddin Hospital", "area": "North Nazimabad", "lat": 24.9300, "lon": 67.0407, "spec": _ALL},
    {"name": "The Indus Hospital", "area": "Korangi", "lat": 24.8326, "lon": 67.1129, "spec": _ALL},
]

DEFAULT_CENTER = (24.8607, 67.0011)  # Karachi
HEADERS = {"User-Agent": "MediBot/1.0 (hospital chatbot student project)"}


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def geocode(place):
    """Return (lat, lon) or None. Needs internet."""
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={"q": place, "format": "json", "limit": 1},
                     headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


def sample_search(lat, lon, radius_km, specialty=None):
    out = []
    for f in FACILITIES:
        if specialty and specialty not in f["spec"]:
            continue
        d = haversine_km(lat, lon, f["lat"], f["lon"])
        if d <= radius_km:
            out.append({"name": f["name"], "area": f["area"], "lat": f["lat"],
                        "lon": f["lon"], "km": round(d, 1), "kind": "hospital"})
    return sorted(out, key=lambda x: x["km"])


def live_search(lat, lon, radius_km):
    q = f"""[out:json][timeout:20];
(
  node["amenity"~"hospital|clinic|doctors"](around:{int(radius_km * 1000)},{lat},{lon});
  way["amenity"~"hospital|clinic|doctors"](around:{int(radius_km * 1000)},{lat},{lon});
);
out center 60;"""
    r = requests.post("https://overpass-api.de/api/interpreter", data={"data": q},
                      headers=HEADERS, timeout=30)
    r.raise_for_status()
    out = []
    for el in r.json().get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        la = el.get("lat") or el.get("center", {}).get("lat")
        lo = el.get("lon") or el.get("center", {}).get("lon")
        if la is None or lo is None:
            continue
        out.append({"name": name,
                    "area": tags.get("addr:suburb") or tags.get("addr:street") or "",
                    "lat": la, "lon": lo,
                    "km": round(haversine_km(lat, lon, la, lo), 1),
                    "kind": tags.get("amenity", "")})
    return sorted(out, key=lambda x: x["km"])[:40]
