"""
EcoSort AI - Smart Waste Segregation Assistant
------------------------------------------------
A Flask prototype built for the HCL Jigsaw Innovation Competition.

This app SIMULATES an AI waste-classification model using a predefined
lookup table (WASTE_DATABASE). The architecture is intentionally kept
simple so a real trained model (e.g. a TensorFlow/Keras CNN) can later
be dropped into the `identify_waste()` function without changing any
routes, templates, or front-end code.

Author: EcoSort AI Team
"""

import random
from datetime import datetime
from threading import Lock

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = "ecosort-ai-secret-key-2026"  # only used for flashing/session in this demo


# ==========================================================
# LIVE APP STATISTICS (real, in-memory tracking)
# ==========================================================
# This is a lightweight, in-memory counter that reflects REAL activity in
# this running app: every page visit and every waste identification updates
# it immediately, so the Dashboard always shows real numbers instead of
# fixed demo values.
#
# NOTE: Because this is a simple prototype (no database), these counters
# reset whenever the Flask server restarts. For a production version, swap
# this dictionary for a real database table.
_stats_lock = Lock()

APP_STATS = {
    "total_visits": 0,
    "images_uploaded": 0,
    "waste_identified": 0,
    "categories": {
        "Plastic": 0,
        "Paper": 0,
        "Glass": 0,
        "Metal": 0,
        "Organic": 0,
        "E-Waste": 0,
    },
}

# Endpoints that count as a real "site visit" for the traffic counter.
# API calls and static files are intentionally excluded.
TRACKED_PAGE_ENDPOINTS = {"home", "detect", "guide", "ecoscore", "dashboard", "about"}


@app.before_request
def track_site_traffic():
    """Increments the live visit counter for every real page view."""
    if request.endpoint in TRACKED_PAGE_ENDPOINTS:
        with _stats_lock:
            APP_STATS["total_visits"] += 1


# ==========================================================
# TEAM DETAILS
# ==========================================================
PROJECT_NAME = "EcoSort AI – Smart Waste Segregation Assistant"
SCHOOL_NAME = "KMK HR.SEC & MONTESSORI SCHOOL, KARAIKAL"
TEAM_CLASS = "9th Standard"
TEAM_MEMBERS = [
    {"name": "R. Sai Karthik", "icon": "fa-user-graduate"},
    {"name": "B. Bala Raakesh", "icon": "fa-user-graduate"},
    {"name": "S. Rakesh", "icon": "fa-user-graduate"},
    {"name": "R. Santhosh", "icon": "fa-user-graduate"},
]


@app.context_processor
def inject_team_details():
    """
    Makes team/school details available in every template automatically,
    without needing to pass them from each individual route.
    """
    return dict(
        project_name=PROJECT_NAME,
        school_name=SCHOOL_NAME,
        team_class=TEAM_CLASS,
        team_members=TEAM_MEMBERS,
    )


# ==========================================================
# SIMULATED "AI" WASTE DATABASE
# ==========================================================
# In a production version, this dictionary would be replaced by the
# output of an image-classification model. Each entry describes the
# information the front-end needs to render a result card.
WASTE_DATABASE = {
    "plastic": {
        "label": "Plastic Bottle",
        "category": "Plastic",
        "bin_color": "Blue Bin",
        "bin_hex": "#2f6fed",
        "recyclable": "Yes",
        "disposal": "Rinse and send to the Plastic Recycling Facility.",
        "fact": "Recycling one plastic bottle saves enough energy to power a light bulb for 3 hours.",
        "points": 10,
        "icon": "fa-bottle-water",
    },
    "paper": {
        "label": "Paper / Cardboard",
        "category": "Paper",
        "bin_color": "Green Bin",
        "bin_hex": "#2e9e5b",
        "recyclable": "Yes",
        "disposal": "Flatten and place in the Paper Recycling Bin.",
        "fact": "Recycling 1 tonne of paper saves about 17 trees and 26,000 litres of water.",
        "points": 8,
        "icon": "fa-newspaper",
    },
    "glass": {
        "label": "Glass Jar",
        "category": "Glass",
        "bin_color": "Green Bin",
        "bin_hex": "#2e9e5b",
        "recyclable": "Yes",
        "disposal": "Rinse thoroughly and place in the Glass Collection Bin.",
        "fact": "Glass is 100% recyclable and can be recycled endlessly without losing quality.",
        "points": 9,
        "icon": "fa-wine-bottle",
    },
    "metal": {
        "label": "Metal Can",
        "category": "Metal",
        "bin_color": "Grey Bin",
        "bin_hex": "#6b7280",
        "recyclable": "Yes",
        "disposal": "Rinse and place in the Metal Recycling Bin.",
        "fact": "Recycling aluminium cans uses 95% less energy than making new ones.",
        "points": 10,
        "icon": "fa-jar",
    },
    "organic": {
        "label": "Organic / Food Waste",
        "category": "Organic",
        "bin_color": "Brown Bin",
        "bin_hex": "#8a5a2b",
        "recyclable": "Compostable",
        "disposal": "Send to the compost pit or Brown Organic Waste Bin.",
        "fact": "Composted food waste enriches soil and cuts methane emissions from landfills.",
        "points": 5,
        "icon": "fa-leaf",
    },
    "ewaste": {
        "label": "E-Waste (Battery/Phone)",
        "category": "E-Waste",
        "bin_color": "Red Bin",
        "bin_hex": "#d63b3b",
        "recyclable": "Special Handling",
        "disposal": "Drop off at an authorised E-Waste Collection Center. Never bin electronics with regular trash.",
        "fact": "E-waste contains valuable metals like gold and copper worth recovering, plus toxins that must be handled safely.",
        "points": 15,
        "icon": "fa-laptop",
    },
}

# Daily eco quotes / tips shown on the dashboard & home page
ECO_QUOTES = [
    "The earth does not belong to us; we belong to the earth.",
    "Reduce, Reuse, Recycle - in that order of priority.",
    "Every small act of recycling is a big step for the planet.",
    "Waste segregation today is a greener tomorrow.",
    "There is no such thing as 'away'. When you throw something away, it must go somewhere.",
    "Small daily habits create big environmental change.",
]

DAILY_TIPS = [
    "Rinse containers before recycling to avoid contaminating a whole batch.",
    "Flatten cardboard boxes to save space in your recycling bin.",
    "Keep a separate small bin for e-waste like batteries and cables.",
    "Compost fruit and vegetable peels instead of throwing them away.",
    "Carry a reusable bag to avoid single-use plastic altogether.",
]


def identify_waste(waste_type: str):
    """
    Simulates an AI model's prediction.

    In the future, replace the lookup below with a call to a real model, e.g.:
        prediction = model.predict(image)
        waste_type = decode_prediction(prediction)

    The rest of the app does not need to change because it only depends on
    the dictionary shape returned here.
    """
    key = waste_type.lower().strip().replace("-", "").replace(" ", "")
    return WASTE_DATABASE.get(key)


# ==========================================================
# ROUTES
# ==========================================================

@app.route("/")
def home():
    """Landing page with hero section, features, and animated stats."""
    return render_template("index.html", quote=random.choice(ECO_QUOTES))


@app.route("/detect", methods=["GET"])
def detect():
    """Waste detection page (upload or dropdown simulated identification)."""
    return render_template("detect.html", waste_types=WASTE_DATABASE)


@app.route("/api/identify", methods=["POST"])
def api_identify():
    """
    AJAX endpoint used by detect.html.
    Accepts a JSON payload: { "waste_type": "plastic" }
    (An uploaded image, if present, is accepted but not analysed in this
    prototype - it is only used to simulate a short "AI analysing" delay
    on the front-end.)
    """
    data = request.get_json(silent=True) or {}
    waste_type = data.get("waste_type", "")

    result = identify_waste(waste_type)
    if not result:
        return jsonify({"success": False, "message": "Could not identify this waste type."}), 400

    # Update REAL live statistics — this is what the Dashboard reads from.
    with _stats_lock:
        APP_STATS["images_uploaded"] += 1
        APP_STATS["waste_identified"] += 1
        category = result["category"]
        if category in APP_STATS["categories"]:
            APP_STATS["categories"][category] += 1

    response = dict(result)
    response["success"] = True
    response["timestamp"] = datetime.now().strftime("%H:%M:%S")
    return jsonify(response)


@app.route("/guide")
def guide():
    """Recycling guide page with a card per waste category."""
    guide_data = [
        {
            "category": "Plastic",
            "icon": "fa-bottle-water",
            "color": "#2f6fed",
            "examples": ["Bottle", "Container", "Cover"],
            "bin": "Blue Bin",
            "disposal": "Clean and place in the Blue Bin for plastic recycling.",
        },
        {
            "category": "Paper",
            "icon": "fa-newspaper",
            "color": "#2e9e5b",
            "examples": ["Books", "Cardboard", "Notebook"],
            "bin": "Green Bin",
            "disposal": "Keep dry and flat, then place in the Green Bin.",
        },
        {
            "category": "Glass",
            "icon": "fa-wine-bottle",
            "color": "#16a596",
            "examples": ["Bottle", "Jar", "Mirror"],
            "bin": "Green Bin",
            "disposal": "Rinse and place carefully in the Green Bin.",
        },
        {
            "category": "Metal",
            "icon": "fa-jar",
            "color": "#6b7280",
            "examples": ["Can", "Tin", "Foil"],
            "bin": "Grey Bin",
            "disposal": "Rinse and place in the Grey Bin for metal recycling.",
        },
        {
            "category": "Organic",
            "icon": "fa-leaf",
            "color": "#8a5a2b",
            "examples": ["Leaves", "Vegetables", "Food Waste"],
            "bin": "Brown Bin",
            "disposal": "Compost or place in the Brown organic-waste Bin.",
        },
        {
            "category": "E-Waste",
            "icon": "fa-laptop",
            "color": "#d63b3b",
            "examples": ["Battery", "Phone", "Laptop"],
            "bin": "Red Bin",
            "disposal": "Drop off at a certified E-Waste Collection Center.",
        },
    ]
    return render_template("guide.html", guide_data=guide_data, tip=random.choice(DAILY_TIPS))


@app.route("/ecoscore")
def ecoscore():
    """Simple EcoScore page — points earned per waste category."""
    points_table = [
        {"category": "Plastic", "points": 10, "icon": "fa-bottle-water", "color": "#2f6fed"},
        {"category": "Paper", "points": 8, "icon": "fa-newspaper", "color": "#2e9e5b"},
        {"category": "Glass", "points": 9, "icon": "fa-wine-bottle", "color": "#16a596"},
        {"category": "Organic", "points": 5, "icon": "fa-leaf", "color": "#8a5a2b"},
        {"category": "Metal", "points": 10, "icon": "fa-jar", "color": "#6b7280"},
        {"category": "E-Waste", "points": 15, "icon": "fa-laptop", "color": "#d63b3b"},
    ]

    return render_template("ecoscore.html", points_table=points_table)


@app.route("/dashboard")
def dashboard():
    """
    Live analytics dashboard — reflects REAL activity in this running app.

    Total Visits, Images Uploaded, Waste Identified, and every category
    count come straight from APP_STATS, which is updated in real time by
    track_site_traffic() (on every page view) and api_identify() (on every
    successful waste identification). Nothing on this page is hardcoded
    demo data.
    """
    category_meta = {
        "Plastic": {"icon": "fa-bottle-water", "color": "#2f6fed"},
        "Paper": {"icon": "fa-newspaper", "color": "#2e9e5b"},
        "Glass": {"icon": "fa-wine-bottle", "color": "#16a596"},
        "Metal": {"icon": "fa-jar", "color": "#6b7280"},
        "Organic": {"icon": "fa-leaf", "color": "#8a5a2b"},
        "E-Waste": {"icon": "fa-laptop", "color": "#d63b3b"},
    }

    with _stats_lock:
        stats = {
            "total_visits": APP_STATS["total_visits"],
            "images_uploaded": APP_STATS["images_uploaded"],
            "waste_identified": APP_STATS["waste_identified"],
        }
        category_counts = dict(APP_STATS["categories"])

    categories = [
        {
            "category": name,
            "count": category_counts[name],
            "icon": category_meta[name]["icon"],
            "color": category_meta[name]["color"],
        }
        for name in category_meta
    ]
    max_count = max((c["count"] for c in categories), default=0) or 1

    return render_template(
        "dashboard.html",
        stats=stats,
        categories=categories,
        max_count=max_count,
    )


@app.route("/about")
def about():
    """About page: problem statement, solution, objectives, future scope."""
    future_features = [
        {"title": "Real AI Image Recognition", "icon": "fa-brain"},
        {"title": "Smart Dustbin Integration", "icon": "fa-trash-arrow-up"},
        {"title": "IoT Sensors", "icon": "fa-microchip"},
        {"title": "Municipality Dashboard", "icon": "fa-city"},
        {"title": "School Recycling Competition", "icon": "fa-medal"},
        {"title": "Android App", "icon": "fa-mobile-screen-button"},
        {"title": "QR Code Waste Identification", "icon": "fa-qrcode"},
        {"title": "Carbon Footprint Tracking", "icon": "fa-cloud"},
    ]
    return render_template("about.html", future_features=future_features)


if __name__ == "__main__":
    # debug=True is fine for local prototyping / competition demo purposes
    app.run(debug=True, port=5000)
