import random
import math
import matplotlib.pyplot as plt

# -----------------------------
# 1. Simulate IoT Smart Bins
# -----------------------------
NUM_BINS = 15
BIN_THRESHOLD = 70  # percent

bins = []

for i in range(NUM_BINS):
    bin_data = {
        "id": i,
        "x": random.randint(0, 100),
        "y": random.randint(0, 100),
        "fill": random.randint(10, 100)
    }
    bins.append(bin_data)

# Truck starting point (depot)
truck_start = {"x": 50, "y": 50}

# -----------------------------
# 2. Intelligent Bin Filtering
# -----------------------------
priority_bins = [b for b in bins if b["fill"] >= BIN_THRESHOLD]

print(f"Total bins: {len(bins)}")
print(f"Bins selected for collection: {len(priority_bins)}")

# -----------------------------
# 3. Distance Function
# -----------------------------
def distance(a, b):
    return math.sqrt((a["x"] - b["x"])*2 + (a["y"] - b["y"])*2)

# -----------------------------
# 4. Route Optimization
#    (Nearest Neighbor Algorithm)
# -----------------------------
def optimize_route(start, bins):
    route = []
    current = start
    remaining = bins.copy()

    while remaining:
        nearest = min(remaining, key=lambda b: distance(current, b))
        route.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return route

optimized_route = optimize_route(truck_start, priority_bins)

# -----------------------------
# 5. Visualization Dashboard
# -----------------------------
plt.figure(figsize=(8, 8))

# Plot all bins
for b in bins:
    if b["fill"] >= BIN_THRESHOLD:
        plt.scatter(b["x"], b["y"], c="red", s=100)
        plt.text(b["x"]+1, b["y"]+1, f'{b["fill"]}%', fontsize=9)
    else:
        plt.scatter(b["x"], b["y"], c="green", s=60)

# Plot truck start
plt.scatter(truck_start["x"], truck_start["y"], c="blue", s=200, marker="s")
plt.text(truck_start["x"]+1, truck_start["y"]+1, "Truck Start", fontsize=10)

# Plot optimized route
route_x = [truck_start["x"]] + [b["x"] for b in optimized_route]
route_y = [truck_start["y"]] + [b["y"] for b in optimized_route]

plt.plot(route_x, route_y)

plt.title("AI-Based Smart Waste Collection Route")
plt.xlabel("City X")
plt.ylabel("City Y")
plt.grid(True)
plt.show()