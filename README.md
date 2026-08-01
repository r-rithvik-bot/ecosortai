# 🌱 EcoSort AI — Smart Waste Segregation Assistant

A Flask prototype built for the **HCL Jigsaw Innovation Competition (Grades 6–9)**. EcoSort AI helps users identify waste, learn the correct disposal method, and stay motivated to recycle through a gamified **EcoScore** rewards system.

> **Note:** This prototype simulates AI predictions using a predefined lookup table instead of a trained model, so it runs instantly with no GPU, dataset, or internet-based model download required. The code is structured so a real image-classification model can be dropped in later without changing the routes or front end.

---

## ✨ Features

- **Home Page** — animated hero, feature highlights, and live environmental stats
- **Detect Waste** — upload an image (preview only) or pick a category to get an instant simulated identification
- **Recycling Guide** — reference cards for Plastic, Paper, Glass, Metal, Organic, and E-Waste
- **EcoScore** — points, levels, badges, and environmental impact tracking (CO₂ saved, trees protected)
- **Dashboard** — pie / bar / line charts (Chart.js) plus recycling progress bars
- **About** — problem statement, solution, objectives, benefits, and future roadmap
- **Bonus** — dark mode toggle, scroll-to-top button, animated counters, toasts, daily eco tips, and quotes

---

## 🧰 Technology Stack

| Layer       | Tools                                  |
|-------------|-----------------------------------------|
| Backend     | Python 3, Flask                         |
| Frontend    | HTML5, CSS3, Bootstrap 5, JavaScript    |
| Charts      | Chart.js                                |
| Icons       | Font Awesome 6                          |
| Animations  | AOS (Animate on Scroll)                 |
| Fonts       | Fraunces (display), Inter (body), JetBrains Mono (data) |

---

## 📁 Folder Structure

```
EcoSortAI/
│
├── app.py                 # Flask application & routes
├── requirements.txt       # Python dependencies
├── README.md               # This file
│
├── templates/
│   ├── base.html           # Shared navbar / footer layout
│   ├── index.html          # Home page
│   ├── detect.html         # Waste detection page
│   ├── dashboard.html      # Analytics dashboard
│   ├── guide.html          # Recycling guide
│   ├── ecoscore.html       # EcoScore gamification page
│   └── about.html          # About page
│
├── static/
│   ├── css/
│   │   └── style.css       # All custom styling & design tokens
│   ├── js/
│   │   └── script.js       # Dark mode, counters, AJAX detection, toasts
│   └── images/              # (reserved for future image assets)
│
└── uploads/                 # (reserved for future uploaded images)
```

---

## 🚀 Installation & Setup

### 1. Clone or copy the project folder
Make sure all files are inside a single `EcoSortAI/` folder as shown above.

### 2. Create a virtual environment (recommended)

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in your browser
```
http://127.0.0.1:5000
```

---

## 🗺️ Routes

| Route          | Page                    |
|----------------|--------------------------|
| `/`            | Home                     |
| `/detect`      | Detect Waste             |
| `/api/identify`| AJAX endpoint (POST) used by the Detect page |
| `/guide`       | Recycling Guide          |
| `/ecoscore`    | EcoScore                 |
| `/dashboard`   | Dashboard                |
| `/about`       | About                    |

---

## 🔮 Future Improvements

- Replace the simulated lookup table in `identify_waste()` (in `app.py`) with a real trained image-classification model (e.g., a TensorFlow/Keras CNN)
- Persist EcoScore and history per user with a database (SQLite/PostgreSQL) and login system
- Smart Dustbin & IoT sensor integration for automatic sorting
- Municipality-level dashboard for city-wide waste analytics
- School recycling leaderboard / competition mode
- Native Android app with camera-based detection
- QR-code based waste identification for packaged products
- Personal carbon footprint tracking over time

---

## 🛡️ Notes

- This is a **prototype** intended for demonstration purposes at the HCL Jigsaw Innovation Competition.
- All statistics (images processed, EcoScore points, dashboard numbers) are **sample data** for demo purposes.
- Uploaded images in the Detect page are used only for an on-page preview; they are not analysed or stored on the server in this version.

---

Made with 💚 for a greener future.
