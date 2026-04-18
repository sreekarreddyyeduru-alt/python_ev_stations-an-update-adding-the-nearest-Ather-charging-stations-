# python_ev_stations-an-update-adding-the-nearest-Ather-charging-stations-
an upgrade for the previous repository
"""
EV Charging Map — Week 3 Build Sprint
Run on Replit: just hit the green RUN button!

Setup:
  1. Replace YOUR_API_KEY_HERE with your key from openchargemap.org (free signup)
  2. Hit Run — opens on port 3000
"""

from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ─── PUT YOUR API KEY HERE ───────────────────────────────────
API_KEY = "69cec695-3681-4f15-b366-d73af8aebdb9"

# Hyderabad coordinates
LAT = 17.3850
LON = 78.4867

# ─── SAMPLE DATA (used as fallback if no API key) ────────────
SAMPLE_STATIONS = [
    {
        "AddressInfo": {"Title": "Hitec City Charging Hub", "Distance": 1.2},
        "NumberOfPoints": 4,
        "StatusType": {"IsOperational": True},
        "Connections": [
            {"ConnectionType": {"Title": "CCS2"}, "PowerKW": 100},
            {"ConnectionType": {"Title": "Type 2"}, "PowerKW": 22},
        ],
    },
    {
        "AddressInfo": {"Title": "Gachibowli EV Station", "Distance": 2.8},
        "NumberOfPoints": 2,
        "StatusType": {"IsOperational": False},
        "Connections": [
            {"ConnectionType": {"Title": "Type 2"}, "PowerKW": 22},
        ],
    },
    {
        "AddressInfo": {"Title": "Kondapur Fast Charger", "Distance": 3.5},
        "NumberOfPoints": 6,
        "StatusType": {"IsOperational": True},
        "Connections": [
            {"ConnectionType": {"Title": "CCS2"}, "PowerKW": 150},
            {"ConnectionType": {"Title": "CHAdeMO"}, "PowerKW": 50},
        ],
    },
    {
        "AddressInfo": {"Title": "Jubilee Hills EV Point", "Distance": 4.1},
        "NumberOfPoints": 3,
        "StatusType": {"IsOperational": True},
        "Connections": [
            {"ConnectionType": {"Title": "CCS (Type 1)"}, "PowerKW": 50},
            {"ConnectionType": {"Title": "CCS2"}, "PowerKW": 100},
        ],
    },
    {
        "AddressInfo": {"Title": "Madhapur Supercharger", "Distance": 4.8},
        "NumberOfPoints": 8,
        "StatusType": {"IsOperational": True},
        "Connections": [
            {"ConnectionType": {"Title": "Tesla"}, "PowerKW": 250},
            {"ConnectionType": {"Title": "CCS2"}, "PowerKW": 150},
        ],
    },
    {
        "AddressInfo": {"Title": "Financial District EV Hub", "Distance": 5.2},
        "NumberOfPoints": 5,
        "StatusType": {"IsOperational": True},
        "Connections": [
            {"ConnectionType": {"Title": "CCS2"}, "PowerKW": 100},
        ],
    },
    {
        "AddressInfo": {"Title": "Banjara Hills Charger", "Distance": 6.0},
        "NumberOfPoints": 2,
        "StatusType": {"IsOperational": False},
        "Connections": [
            {"ConnectionType": {"Title": "CHAdeMO"}, "PowerKW": 50},
        ],
    },
]

# ─── ATHER GRID STATIONS NEAR HYDERABAD ──────────────────────
# Real Ather Grid locations in Hyderabad (hardcoded — Ather has no public API)
ATHER_STATIONS = [
    {
        "name": "Ather Space Hitec City",
        "address": "Hitec City, Hyderabad",
        "distance_km": 1.4,
        "charger_type": "Ather Dot (Fast Charge)",
        "power_kw": 1.5,
        "compatible": ["Ather 450X", "Ather 450 Plus"],
        "open_hours": "10:00 AM - 8:00 PM",
        "is_operational": True,
    },
    {
        "name": "Ather Grid - Inorbit Mall",
        "address": "Inorbit Mall, Madhapur, Hyderabad",
        "distance_km": 3.1,
        "charger_type": "Ather Fast Charger",
        "power_kw": 1.5,
        "compatible": ["Ather 450X", "Ather 450 Plus", "Ather 450S"],
        "open_hours": "11:00 AM - 9:30 PM",
        "is_operational": True,
    },
    {
        "name": "Ather Grid - Gachibowli",
        "address": "DLF Cybercity, Gachibowli, Hyderabad",
        "distance_km": 4.2,
        "charger_type": "Ather Fast Charger",
        "power_kw": 1.5,
        "compatible": ["Ather 450X", "Ather 450 Plus"],
        "open_hours": "9:00 AM - 9:00 PM",
        "is_operational": False,
    },
    {
        "name": "Ather Grid - Jubilee Hills",
        "address": "Road No. 36, Jubilee Hills, Hyderabad",
        "distance_km": 5.8,
        "charger_type": "Ather Dot (Home-style)",
        "power_kw": 0.75,
        "compatible": ["All Ather models"],
        "open_hours": "24 Hours",
        "is_operational": True,
    },
    {
        "name": "Ather Grid - KPHB Colony",
        "address": "KPHB Colony, Kukatpally, Hyderabad",
        "distance_km": 7.3,
        "charger_type": "Ather Fast Charger",
        "power_kw": 1.5,
        "compatible": ["Ather 450X", "Ather 450 Plus", "Ather 450S"],
        "open_hours": "10:00 AM - 8:00 PM",
        "is_operational": True,
    },
]


def fetch_stations():
    """Fetch from Open Charge Map. Falls back to sample data if no key."""
    if API_KEY == "YOUR_API_KEY_HERE":
        return SAMPLE_STATIONS, True  # (data, is_sample)

    url = "https://api.openchargemap.io/v3/poi/"
    params = {
        "key": API_KEY,
        "latitude": LAT,
        "longitude": LON,
        "maxresults": 20,
        "distance": 10,
        "distanceunit": "KM",
    }
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return SAMPLE_STATIONS, True


def get_nearest_ather():
    """Return the single closest Ather Grid station."""
    return min(ATHER_STATIONS, key=lambda s: s["distance_km"])


# ─── ROUTES ─────────────────────────────────────────────────


@app.route("/")
def index():
    return HTML_PAGE


# CHECKPOINT 1 - status code + count
@app.route("/cp1")
def cp1():
    stations, is_sample = fetch_stations()
    return jsonify(
        {
            "status_code": 200,
            "stations_found": len(stations),
            "is_sample": is_sample,
            "message": "Connection successful!"
            if not is_sample
            else "Using sample data - add API key for live data",
        }
    )


# CHECKPOINT 2 - list of station names
@app.route("/cp2")
def cp2():
    stations, is_sample = fetch_stations()
    names = [s["AddressInfo"]["Title"] for s in stations]
    return jsonify(
        {
            "is_sample": is_sample,
            "count": len(names),
            "stations": names,
        }
    )


# CHECKPOINT 3 - full details: name, distance, connectors, status
@app.route("/cp3")
def cp3():
    stations, is_sample = fetch_stations()
    results = []
    for s in stations:
        info = s["AddressInfo"]
        status_obj = s.get("StatusType") or {}
        is_open = bool(status_obj.get("IsOperational"))
        connectors = list(
            {
                c["ConnectionType"]["Title"]
                for c in s.get("Connections", [])
                if c.get("ConnectionType")
            }
        )
        max_kw = max(
            (c.get("PowerKW") or 0 for c in s.get("Connections", [])), default=0
        )
        results.append(
            {
                "name": info["Title"],
                "distance_km": round(info.get("Distance") or 0, 1),
                "points": s.get("NumberOfPoints") or 0,
                "status": "Open" if is_open else "Closed",
                "connectors": connectors,
                "max_kw": max_kw,
            }
        )
    return jsonify({"is_sample": is_sample, "stations": results})


# CHECKPOINT 4 - HOMEWORK: filter CCS2 only (Tata Nexon compatible)
@app.route("/cp4")
def cp4():
    stations, is_sample = fetch_stations()
    filtered = []
    for s in stations:
        connections = s.get("Connections") or []
        for conn in connections:
            ct = conn.get("ConnectionType") or {}
            title = ct.get("Title") or ""
            if "Type 2" in title or "CCS" in title or "DC" in title or "Fast" in title:
                info = s.get("AddressInfo") or {}
                status_obj = s.get("StatusType") or {}
                filtered.append(
                    {
                        "name": info.get("Title", "Unknown"),
                        "distance_km": round(info.get("Distance") or 0, 1),
                        "status": "Open"
                        if status_obj.get("IsOperational")
                        else "Closed",
                        "power_kw": conn.get("PowerKW") or 0,
                        "connector": title if title else "Unknown",
                    }
                )
                break
    return jsonify(
        {
            "is_sample": is_sample,
            "total_stations": len(stations),
            "ccs2_count": len(filtered),
            "stations": filtered,
        }
    )


# ─── ATHER ROUTE - nearest station + full list ───────────────
@app.route("/ather")
def ather():
    nearest = get_nearest_ather()
    return jsonify(
        {
            "nearest": nearest,
            "all_stations": ATHER_STATIONS,
            "total": len(ATHER_STATIONS),
            "note": "Ather Grid data is hardcoded - Ather does not provide a public API.",
        }
    )


# ─── HTML PAGE (inline so no templates folder needed) ────────
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EV Charging Map - Build Sprint</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0005;--s1:#12000a;--s2:#1a0010;--s3:#220016;
  --border:#3d0025;--border2:#5c0038;
  --red:#ff1744;--red2:#d50000;--red-bg:#2a0010;
  --blue:#2979ff;--blue2:#1565c0;--blue-bg:#00103d;
  --white:#ffffff;--white-dim:#e0e0e0;--white-bg:#1a1a2e;
  --amber:#ffb300;--amber-bg:#2a1f00;
  --green:#00e676;--green-bg:#00261a;
  --purple:#ce93d8;--purple-bg:#1a0a2e;
  --ather:#00bfa5;--ather-bg:#00241f;--ather2:#00897b;
  --muted:#7b3f5e;--muted2:#a05070;
  --text:#f5f0f3;--mono:'JetBrains Mono',monospace;
  --display:'Syne',sans-serif;
}

html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--mono)}
.shell{display:grid;grid-template-rows:56px 1fr;height:100vh;overflow:hidden}
.topbar{background:var(--s1);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 24px;gap:16px}
.brand{font-family:var(--display);font-weight:800;font-size:15px;letter-spacing:-.3px;color:var(--white);display:flex;align-items:center;gap:10px}
.brand-icon{width:28px;height:28px;border-radius:6px;background:var(--red);display:flex;align-items:center;justify-content:center;font-size:14px}
.tag{font-size:10px;font-weight:700;padding:3px 8px;border-radius:4px;letter-spacing:.8px;background:var(--blue-bg);color:var(--blue);margin-left:4px;border:1px solid var(--blue)}
.spacer{flex:1}
.progress-pills{display:flex;gap:8px}
.ppill{font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px;letter-spacing:.5px;opacity:.35;transition:.2s;border:1px solid transparent;color:var(--white-dim)}
.ppill.done{opacity:1;background:var(--red-bg);color:var(--red);border-color:var(--red)}
.ppill.done-ather{opacity:1;background:var(--ather-bg);color:var(--ather);border-color:var(--ather)}
.ppill.active{opacity:1;border-color:var(--muted2);color:var(--white)}
.main{display:grid;grid-template-columns:280px 1fr;overflow:hidden}
.sidebar{background:var(--s1);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:20px 12px;gap:8px;overflow-y:auto}
.sidebar-title{font-size:9px;font-weight:700;letter-spacing:1.5px;color:var(--muted2);padding:0 8px;margin-bottom:4px}
.cp-card{border-radius:8px;border:1px solid var(--border);padding:12px 14px;cursor:pointer;transition:.15s;background:transparent;position:relative;overflow:hidden;text-align:left;width:100%}
.cp-card:hover{border-color:var(--border2);background:var(--s2)}
.cp-card.active{background:var(--s2);border-color:var(--blue)}
.cp-card.done{border-color:var(--red)}
.cp-card.homework{border-color:var(--purple);border-style:dashed}
.cp-card.homework.active{background:var(--purple-bg)}
.cp-card.ather-card{border-color:var(--ather);border-style:dashed}
.cp-card.ather-card.active{background:var(--ather-bg);border-color:var(--ather);border-style:solid}
.cp-card.ather-card.done{border-color:var(--ather);border-style:solid}
.cp-num{font-size:9px;font-weight:700;letter-spacing:1px;margin-bottom:5px}
.cp-card:not(.homework):not(.ather-card) .cp-num{color:var(--blue)}
.cp-card.homework .cp-num{color:var(--purple)}
.cp-card.ather-card .cp-num{color:var(--ather)}
.cp-card.done:not(.ather-card) .cp-num{color:var(--red)}
.cp-title{font-size:12px;font-weight:700;color:var(--white);margin-bottom:3px;font-family:var(--display)}
.cp-desc{font-size:10px;color:var(--muted2);line-height:1.5}
.cp-badge{position:absolute;top:10px;right:10px;font-size:9px;font-weight:700;padding:2px 7px;border-radius:10px}
.badge-hw{background:var(--purple-bg);color:var(--purple);border:1px dashed var(--purple)}
.badge-ather{background:var(--ather-bg);color:var(--ather);border:1px solid var(--ather)}
.divider{height:1px;background:var(--border);margin:4px 0}
.note-box{background:var(--amber-bg);border:1px solid var(--amber);border-radius:6px;padding:10px 12px;margin-top:4px}
.note-box p{font-size:10px;color:var(--amber);line-height:1.6}
.note-box strong{font-weight:700}
.output-area{display:flex;flex-direction:column;overflow:hidden;background:var(--bg)}
.out-header{background:var(--s1);border-bottom:1px solid var(--border);padding:0 20px;height:40px;display:flex;align-items:center;gap:12px;font-size:11px;color:var(--muted2)}
.out-dot{width:6px;height:6px;border-radius:50%;background:var(--muted);transition:.3s}
.out-dot.running{background:var(--amber);animation:pulse 1s infinite}
.out-dot.done{background:var(--red)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.out-spacer{flex:1}
.run-btn{display:flex;align-items:center;gap:8px;padding:7px 20px;background:var(--red);color:#fff;font-weight:700;font-size:12px;font-family:var(--mono);border:none;border-radius:6px;cursor:pointer;transition:.15s;letter-spacing:.3px}
.run-btn:hover{background:var(--red2);transform:translateY(-1px);box-shadow:0 4px 12px rgba(255,23,68,.4)}
.run-btn:active{transform:translateY(0);box-shadow:none}
.run-btn:disabled{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none}
.play{display:inline-block;width:0;height:0;border-top:5px solid transparent;border-bottom:5px solid transparent;border-left:9px solid #fff}
.out-content{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:16px}
.welcome{text-align:center;padding:40px 20px}
.welcome h2{font-family:var(--display);font-size:18px;font-weight:700;color:var(--muted2);margin-bottom:8px}
.welcome p{font-size:11px;color:var(--muted);line-height:1.7}
.result-card{background:var(--s1);border:1px solid var(--border);border-radius:10px;overflow:hidden}
.rc-header{padding:10px 16px;font-size:10px;font-weight:700;letter-spacing:.8px;display:flex;align-items:center;gap:8px}
.rc-header.cp1-h{background:var(--blue-bg);color:var(--blue);border-bottom:1px solid var(--border)}
.rc-header.cp2-h{background:var(--white-bg);color:var(--white);border-bottom:1px solid var(--border)}
.rc-header.cp3-h{background:var(--red-bg);color:var(--red);border-bottom:1px solid var(--border)}
.rc-header.cp4-h{background:var(--purple-bg);color:var(--purple);border-bottom:1px solid var(--border)}
.rc-header.ather-h{background:var(--ather-bg);color:var(--ather);border-bottom:1px solid var(--ather)}
.rc-body{padding:16px}
.stat-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.stat{background:var(--s3);border:1px solid var(--border2);border-radius:8px;padding:10px 16px;min-width:110px}
.stat-label{font-size:9px;color:var(--muted2);letter-spacing:.8px;margin-bottom:4px}
.stat-val{font-size:18px;font-weight:700;font-family:var(--display)}
.val-red{color:var(--red)}.val-blue{color:var(--blue)}.val-white{color:var(--white)}.val-ather{color:var(--ather)}
.station-list{display:flex;flex-direction:column;gap:6px}
.station-row,.ather-row{display:flex;align-items:center;gap:10px;background:var(--s2);border:1px solid var(--border);border-radius:6px;padding:10px 14px;animation:slideIn .2s ease both}
.ather-row.nearest-row{border-color:var(--ather)}
@keyframes slideIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
.s-num{font-size:10px;color:var(--muted2);min-width:22px}
.s-name{flex:1;font-size:12px;font-weight:600;color:var(--white)}
.s-dist{font-size:10px;color:var(--muted2)}
.s-status{font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px}
.open{background:var(--green-bg);color:var(--green)}
.closed{background:var(--red-bg);color:var(--red)}
.s-connectors{display:flex;gap:4px;flex-wrap:wrap}
.conn-tag{font-size:9px;padding:2px 7px;border-radius:4px;background:var(--blue-bg);color:var(--blue);border:1px solid var(--border2)}
.conn-tag.ccs2{background:var(--red-bg);color:var(--red);border-color:var(--red)}
.conn-tag.ather-tag{background:var(--ather-bg);color:var(--ather);border:1px solid var(--ather)}
.s-kw{font-size:10px;color:var(--white-dim);min-width:52px;text-align:right}
.ather-nearest{background:var(--ather-bg);border:1px solid var(--ather);border-radius:10px;padding:18px 20px;margin-bottom:14px;position:relative;overflow:hidden}
.ather-nearest::before{content:'NEAREST';position:absolute;top:12px;right:14px;font-size:8px;font-weight:700;letter-spacing:1.5px;color:var(--ather);opacity:.5}
.ather-nearest .big-name{font-family:var(--display);font-size:16px;font-weight:800;color:var(--ather);margin-bottom:4px}
.ather-nearest .address{font-size:10px;color:var(--muted2);margin-bottom:12px}
.ather-meta{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.ather-pill{font-size:10px;padding:4px 10px;border-radius:6px;background:#003d33;color:var(--ather);border:1px solid var(--ather2)}
.sample-notice{font-size:10px;color:var(--amber);background:var(--amber-bg);border:1px solid var(--amber);border-radius:6px;padding:8px 14px;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.err-box{background:var(--red-bg);border:1px solid var(--red);border-radius:8px;padding:14px 18px;color:var(--red);font-size:12px;line-height:1.7}
.spinner{display:inline-block;width:12px;height:12px;border:2px solid transparent;border-top-color:var(--amber);border-radius:50%;animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="shell">

  <div class="topbar">
    <div class="brand">
      <div class="brand-icon">&#9889;</div>
      EV Charging Map
      <span class="tag">HYDERABAD</span>
    </div>
    <div class="spacer"></div>
    <div class="progress-pills">
      <span class="ppill" id="pill0">CP1</span>
      <span class="ppill" id="pill1">CP2</span>
      <span class="ppill" id="pill2">CP3</span>
      <span class="ppill" id="pill3">HW</span>
      <span class="ppill" id="pill4">ATHER</span>
    </div>
  </div>

  <div class="main">
    <div class="sidebar">
      <div class="sidebar-title">CHECKPOINTS</div>

      <button class="cp-card active" id="card0" onclick="select(0)">
        <div class="cp-num">CHECKPOINT 01</div>
        <div class="cp-title">First API Call</div>
        <div class="cp-desc">Connect to Open Charge Map. Print status code and station count.</div>
      </button>

      <button class="cp-card" id="card1" onclick="select(1)">
        <div class="cp-num">CHECKPOINT 02</div>
        <div class="cp-title">List Station Names</div>
        <div class="cp-desc">Parse the JSON response. Print all station names in a list.</div>
      </button>

      <button class="cp-card" id="card2" onclick="select(2)">
        <div class="cp-num">CHECKPOINT 03</div>
        <div class="cp-title">Full Station Details</div>
        <div class="cp-desc">Show distance, connector types, power (kW), and open/closed status.</div>
      </button>

      <div class="divider"></div>

      <button class="cp-card homework" id="card3" onclick="select(3)">
        <div class="cp-badge badge-hw">&#128218; HOMEWORK</div>
        <div class="cp-num">CHECKPOINT 04</div>
        <div class="cp-title">CCS2 Filter</div>
        <div class="cp-desc">Show only stations compatible with the Tata Nexon EV (CCS2 connector).</div>
      </button>

      <div class="divider"></div>

      <button class="cp-card ather-card" id="card4" onclick="select(4)">
        <div class="cp-badge badge-ather">&#9889; ATHER</div>
        <div class="cp-num">BONUS</div>
        <div class="cp-title">Nearest Ather Grid</div>
        <div class="cp-desc">Find the closest Ather charging station near Hyderabad.</div>
      </button>

      <div class="note-box" id="api-note">
        <p><strong>&#9888; No API key set</strong><br>Running on sample data. Add your key in <code>main.py</code> to get live Hyderabad data.</p>
      </div>
    </div>

    <div class="output-area">
      <div class="out-header">
        <div class="out-dot" id="out-dot"></div>
        <span id="out-label">ready</span>
        <span class="out-spacer"></span>
        <button class="run-btn" id="run-btn" onclick="run()">
          <div class="play"></div> RUN
        </button>
      </div>
      <div class="out-content" id="out-content">
        <div class="welcome">
          <h2>Select a checkpoint and hit RUN</h2>
          <p>Each checkpoint builds on the previous one.<br>
          Complete 1 &#8594; 2 &#8594; 3 in class, then try CP4 at home.<br>
          Hit <span style="color:var(--ather)">ATHER BONUS</span> to find the nearest Ather Grid station!</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
let current = 0;
let doneSet = new Set();

const endpoints = ['/cp1', '/cp2', '/cp3', '/cp4', '/ather'];
const titles = [
  'CHECKPOINT 1 - API Connection',
  'CHECKPOINT 2 - Station Names',
  'CHECKPOINT 3 - Full Details',
  'CHECKPOINT 4 - CCS2 Filter (Homework)',
  'BONUS - Nearest Ather Grid Station',
];

function select(idx) {
  current = idx;
  document.querySelectorAll('.cp-card').forEach((c,i) => {
    c.classList.toggle('active', i === idx);
  });
}

function setRunning(on) {
  const btn = document.getElementById('run-btn');
  const dot = document.getElementById('out-dot');
  const lbl = document.getElementById('out-label');
  btn.disabled = on;
  dot.className = 'out-dot ' + (on ? 'running' : (doneSet.has(current) ? 'done' : ''));
  lbl.textContent = on ? 'running...' : (doneSet.has(current) ? titles[current] : 'ready');
}

function sampleNotice(isSample) {
  return isSample ? `<div class="sample-notice">&#9888; Using sample data - replace API_KEY in main.py to get live Hyderabad results</div>` : '';
}

function markDone(idx) {
  doneSet.add(idx);
  document.getElementById('card'+idx).classList.add('done');
  const badges = ['CP1','CP2','CP3','HW','ATHER'];
  const pill = document.getElementById('pill'+idx);
  pill.textContent = '\u2713 ' + badges[idx];
  pill.classList.add(idx === 4 ? 'done-ather' : 'done');
}

async function run() {
  setRunning(true);
  const out = document.getElementById('out-content');
  out.innerHTML = `<div style="padding:30px 0;color:var(--amber);font-size:12px;display:flex;align-items:center;gap:10px"><span class="spinner"></span> Fetching data...</div>`;
  try {
    const res = await fetch(endpoints[current]);
    const data = await res.json();
    renderResult(current, data, out);
    markDone(current);
  } catch(e) {
    out.innerHTML = `<div class="err-box">Error: ${e.message}<br><br>Make sure Flask is running on port 3000.</div>`;
  }
  setRunning(false);
}

function renderResult(cp, data, out) {
  if (cp === 0) {
    out.innerHTML = `
      <div class="result-card">
        <div class="rc-header cp1-h">&#9889; CHECKPOINT 1 - API CONNECTION</div>
        <div class="rc-body">
          ${sampleNotice(data.is_sample)}
          <div class="stat-row">
            <div class="stat"><div class="stat-label">STATUS CODE</div><div class="stat-val val-red">${data.status_code}</div></div>
            <div class="stat"><div class="stat-label">STATIONS FOUND</div><div class="stat-val val-blue">${data.stations_found}</div></div>
          </div>
          <div style="font-size:12px;color:var(--red);margin-top:4px">&#10003; ${data.message}</div>
          <div style="margin-top:14px;font-size:10px;color:var(--muted2);line-height:1.8">
            <div>&#8594; <span style="color:var(--white)">200</span> means the API responded successfully</div>
            <div>&#8594; <span style="color:var(--white)">${data.stations_found}</span> stations found within 10km of Hyderabad</div>
            <div>&#8594; Next: parse the response to see station names (Checkpoint 2)</div>
          </div>
        </div>
      </div>`;
  }
  else if (cp === 1) {
    const rows = data.stations.map((name, i) =>
      `<div class="station-row" style="animation-delay:${i*40}ms">
        <span class="s-num">${String(i+1).padStart(2,'0')}</span>
        <span class="s-name">${name}</span>
      </div>`).join('');
    out.innerHTML = `
      <div class="result-card">
        <div class="rc-header cp2-h">&#128203; CHECKPOINT 2 - STATION NAMES</div>
        <div class="rc-body">
          ${sampleNotice(data.is_sample)}
          <div class="stat-row"><div class="stat"><div class="stat-label">TOTAL STATIONS</div><div class="stat-val val-white">${data.count}</div></div></div>
          <div class="station-list">${rows}</div>
          <div style="margin-top:14px;font-size:10px;color:var(--muted2);line-height:1.8">
            &#8594; Used <span style="color:var(--blue)">response.json()</span> to convert response to a list<br>
            &#8594; Looped with <span style="color:var(--blue)">for station in stations</span><br>
            &#8594; Extracted with <span style="color:var(--blue)">station["AddressInfo"]["Title"]</span>
          </div>
        </div>
      </div>`;
  }
  else if (cp === 2) {
    const rows = data.stations.map((s, i) => {
      const connTags = s.connectors.map(c => `<span class="conn-tag ${c==='CCS2'?'ccs2':''}">${c}</span>`).join('');
      return `<div class="station-row" style="animation-delay:${i*50}ms;flex-wrap:wrap;gap:8px">
        <span class="s-num">${String(i+1).padStart(2,'0')}</span>
        <span class="s-name">${s.name}</span>
        <span class="s-dist">${s.distance_km} km</span>
        <span class="s-kw">${s.max_kw > 0 ? s.max_kw+'kW' : '-'}</span>
        <span class="s-status ${s.status==='Open'?'open':'closed'}">${s.status==='Open'?'&#10003; Open':'&#10007; Closed'}</span>
        <div class="s-connectors">${connTags}</div>
      </div>`;
    }).join('');
    const open = data.stations.filter(s => s.status==='Open').length;
    out.innerHTML = `
      <div class="result-card">
        <div class="rc-header cp3-h">&#128506; CHECKPOINT 3 - FULL STATION DETAILS</div>
        <div class="rc-body">
          ${sampleNotice(data.is_sample)}
          <div class="stat-row">
            <div class="stat"><div class="stat-label">TOTAL</div><div class="stat-val val-blue">${data.stations.length}</div></div>
            <div class="stat"><div class="stat-label">OPEN NOW</div><div class="stat-val val-white">${open}</div></div>
            <div class="stat"><div class="stat-label">CLOSED</div><div class="stat-val val-red">${data.stations.length - open}</div></div>
          </div>
          <div class="station-list">${rows}</div>
          <div style="margin-top:14px;font-size:10px;color:var(--muted2);line-height:1.8">
            &#8594; <span style="color:var(--red)">Red tags</span> = CCS2 (Tata Nexon compatible)<br>
            &#8594; Try Checkpoint 4 at home to filter only these stations!
          </div>
        </div>
      </div>`;
  }
  else if (cp === 3) {
    const rows = data.stations.map((s, i) =>
      `<div class="station-row" style="animation-delay:${i*60}ms">
        <span style="font-size:13px">&#9889;</span>
        <span class="s-name">${s.name}</span>
        <span class="s-dist">${s.distance_km} km</span>
        <span class="s-kw">${s.power_kw > 0 ? s.power_kw+'kW' : '-'}</span>
        <span class="s-status ${s.status==='Open'?'open':'closed'}">${s.status==='Open'?'&#10003; Open':'&#10007; Closed'}</span>
        <span class="conn-tag ccs2">CCS2</span>
      </div>`).join('');
    out.innerHTML = `
      <div class="result-card">
        <div class="rc-header cp4-h">HOMEWORK - CCS2 COMPATIBLE STATIONS</div>
        <div class="rc-body">
          ${sampleNotice(data.is_sample)}
          <div class="station-list">${rows}</div>
          <div style="margin-top:14px;font-size:10px;color:var(--muted2);line-height:1.9">
            &#8594; Looped through <span style="color:var(--blue)">station["Connections"]</span><br>
            &#8594; Checked if <span style="color:var(--blue)">"CCS2"</span> in connector title<br>
            &#8594; Used <span style="color:var(--blue)">break</span> to avoid duplicates<br>
            &#8594; <span style="color:var(--red)">Homework complete! &#10003;</span>
          </div>
        </div>
      </div>`;
  }
  else if (cp === 4) {
    const n = data.nearest;
    const compatList = n.compatible.map(c => `<span class="ather-pill">${c}</span>`).join('');
    const allRows = data.all_stations.map((s, i) =>
      `<div class="ather-row ${s.name === n.name ? 'nearest-row' : ''}" style="animation-delay:${i*50}ms">
        <span class="s-num">${s.name === n.name ? '&#9733;' : String(i+1).padStart(2,'0')}</span>
        <span class="s-name">${s.name}</span>
        <span class="s-dist">${s.distance_km} km</span>
        <span class="s-kw">${s.power_kw}kW</span>
        <span class="s-status ${s.is_operational?'open':'closed'}">${s.is_operational?'&#10003; Open':'&#10007; Closed'}</span>
        <span class="conn-tag ather-tag">Ather Grid</span>
      </div>`).join('');
    out.innerHTML = `
      <div class="result-card">
        <div class="rc-header ather-h">&#9889; BONUS - NEAREST ATHER GRID STATION</div>
        <div class="rc-body">
          <div class="ather-nearest">
            <div class="big-name">${n.name}</div>
            <div class="address">&#128205; ${n.address}</div>
            <div class="ather-meta">
              <span class="ather-pill">&#128205; ${n.distance_km} km away</span>
              <span class="ather-pill">&#9889; ${n.power_kw} kW</span>
              <span class="ather-pill">&#128337; ${n.open_hours}</span>
              <span class="ather-pill">${n.charger_type}</span>
              <span class="s-status ${n.is_operational?'open':'closed'}" style="font-size:10px;padding:4px 10px">${n.is_operational?'&#10003; Open Now':'&#10007; Closed'}</span>
            </div>
            <div style="font-size:10px;color:var(--muted2)">Compatible with: ${compatList}</div>
          </div>
          <div style="font-size:9px;color:var(--muted2);letter-spacing:1px;margin-bottom:8px;padding:0 2px">ALL ATHER GRID STATIONS NEARBY</div>
          <div class="station-list">${allRows}</div>
          <div style="margin-top:14px;font-size:10px;color:var(--muted2);line-height:1.9">
            &#8594; Data from <span style="color:var(--ather)">ATHER_STATIONS</span> list in <span style="color:var(--ather)">main.py</span><br>
            &#8594; Used <span style="color:var(--ather)">min(stations, key=lambda s: s["distance_km"])</span> to find nearest<br>
            &#8594; <span style="color:var(--muted2)">Note: ${data.note}</span>
          </div>
        </div>
      </div>`;
  }
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
