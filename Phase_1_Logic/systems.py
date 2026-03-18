import numpy as np

# 🌌 THE LINEAR SYSTEMS (Ax = b)
# Each system is a unique universe where 3 planes intersect at a single point.


# 1. The Clean System (Integer-Friendly)
# A well-behaved system with a nice integer solution. Perfect for hand-verification.
# Solution: x = [1, 2, 3]
clean_A = np.array([
    [2.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
    [1.0, 0.0, 0.0]
], dtype=float)
clean_b = np.array([7.0, 13.0, 1.0], dtype=float)


# 2. The Skewed System (Non-Orthogonal Chaos)
# Columns are tilted and stretched. Solution has irrational-looking decimals.
# Tests Cramer's power on geometrically ugly systems.
skewed_A = np.array([
    [1.0,  2.0, -1.0],
    [3.0, -1.0,  2.0],
    [2.0,  3.0,  1.0]
], dtype=float)
skewed_b = np.array([4.0, 1.0, 11.0], dtype=float)


# 3. The Singular System (Collapsed Universe)
# det(A) = 0: The parallelepiped has zero volume — the columns are coplanar.
# Cramer's Rule CANNOT solve this. The universe breaks.
singular_A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0]
], dtype=float)
singular_b = np.array([1.0, 2.0, 3.0], dtype=float)


# 4. The Physical System (Engineering: 3-Loop Circuit / Force Balance)
# Models a real-world system: e.g., resistor network with Kirchhoff's Laws.
# Solution represents physical currents or forces.
physical_A = np.array([
    [10.0, -2.0,  0.0],
    [-2.0,  8.0, -3.0],
    [ 0.0, -3.0,  6.0]
], dtype=float)
physical_b = np.array([12.0, 0.0, -6.0], dtype=float)


# 📦 SYSTEM REGISTRY
systems = {
    "clean": {
        "A": clean_A,
        "b": clean_b,
        "label": "Clean System — Integer Solution [1, 2, 3]"
    },
    "skewed": {
        "A": skewed_A,
        "b": skewed_b,
        "label": "Skewed System — Non-Orthogonal Chaos"
    },
    "singular": {
        "A": singular_A,
        "b": singular_b,
        "label": "Singular System — Collapsed Universe (det=0)"
    },
    "physical": {
        "A": physical_A,
        "b": physical_b,
        "label": "Physical System — Kirchhoff's Circuit"
    }
}


def get_system(name):
    """Returns a preset linear system {A, b, label}."""
    if name not in systems:
        raise ValueError(f"Unknown system '{name}'. Available: {list(systems.keys())}")
    return systems[name]


def list_systems():
    """Prints all available preset systems."""
    print("\n📋 AVAILABLE LINEAR SYSTEMS:")
    print("=" * 50)
    for key, sys in systems.items():
        det_val = np.linalg.det(sys["A"])
        status = "🟢 SOLVABLE" if not np.isclose(det_val, 0.0) else "🔴 SINGULAR"
        print(f"  [{key}] {sys['label']}")
        print(f"         det(A) = {det_val:.4f}  {status}")
    print("=" * 50)
