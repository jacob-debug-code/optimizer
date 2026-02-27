import streamlit as st
import pandas as pd
import math
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("AI Smart Waste Route Optimizer")

# -----------------------------
# Truck Locations (Fixed)
# -----------------------------
trucks = [
    {"id": "T1", "lat": 11.00, "lon": 77.00},
    {"id": "T2", "lat": 11.06, "lon": 77.05}
]

FULL_THRESHOLD = 80


# -----------------------------
# Distance Function
# -----------------------------
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


# -----------------------------
# AI Route Optimization
# -----------------------------
def optimize_routes(bins):
    full_bins = [b for b in bins if b["fill"] >= FULL_THRESHOLD]
    assignments = {}

    for bin_data in full_bins:
        nearest_truck = None
        min_dist = float("inf")

        for truck in trucks:
            d = distance(
                bin_data["lat"], bin_data["lon"],
                truck["lat"], truck["lon"]
            )
            if d < min_dist:
                min_dist = d
                nearest_truck = truck["id"]

        assignments.setdefault(nearest_truck, []).append(bin_data)

    return assignments


# -----------------------------
# Sidebar – Sensor Input
# -----------------------------
st.sidebar.header("Add Bin Sensor Data")

bin_id = st.sidebar.number_input("Bin ID", step=1)
lat = st.sidebar.number_input("Latitude", value=11.02)
lon = st.sidebar.number_input("Longitude", value=77.03)
fill = st.sidebar.slider("Fill Level (%)", 0, 100)

if "bins" not in st.session_state:
    st.session_state.bins = []

if st.sidebar.button("Add Bin Data"):
    st.session_state.bins.append({
        "id": int(bin_id),
        "lat": lat,
        "lon": lon,
        "fill": fill
    })


# -----------------------------
# Display Bin Data
# -----------------------------
st.subheader("Bin Sensor Data")

if st.session_state.bins:
    df = pd.DataFrame(st.session_state.bins)
    st.dataframe(df)
else:
    st.write("No bin data yet")


# -----------------------------
# Optimize Routes
# -----------------------------
routes = optimize_routes(st.session_state.bins)

st.subheader("AI Optimized Routes")

if routes:
    for truck, bins in routes.items():
        st.write(f"**{truck}** → {[b['id'] for b in bins]}")
else:
    st.write("No bins above threshold (80%)")


# -----------------------------
# OpenStreetMap Visualization
# -----------------------------
st.subheader("OpenStreetMap View")

m = folium.Map(location=[11.02, 77.03], zoom_start=13)

colors = ["red", "blue", "green"]

# Plot Trucks
for i, truck in enumerate(trucks):
    folium.Marker(
        [truck["lat"], truck["lon"]],
        popup=f"Truck {truck['id']}",
        icon=folium.Icon(color="black", icon="truck", prefix="fa")
    ).add_to(m)

# Plot Bins and Routes
for i, (truck_id, bins) in enumerate(routes.items()):
    color = colors[i % len(colors)]
    points = []

    for b in bins:
        loc = [b["lat"], b["lon"]]
        points.append(loc)

        folium.Marker(
            loc,
            popup=f"Bin {b['id']} ({b['fill']}%)",
            icon=folium.Icon(color=color)
        ).add_to(m)

    if len(points) > 1:
        folium.PolyLine(points, color=color).add_to(m)

st_folium(m, width=900, height=500)