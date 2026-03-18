import numpy as np

# 🔮 CRAMER'S RULE ENGINE
# Solves Ax = b using the ancient art of determinant ratios.
# Each determinant is literally the VOLUME of a parallelepiped in 3D space.


def compute_det(A):
    """
    Computes the determinant of matrix A — the SIGNED VOLUME of the parallelepiped
    formed by its column vectors.
    If det ≈ 0, the universe has collapsed (columns are coplanar).
    """
    det = np.linalg.det(A)
    if np.isclose(det, 0.0):
        raise ValueError(
            "CRITICAL ERROR: det(A) ≈ 0 — The parallelepiped has ZERO volume!\n"
            "The column vectors are coplanar. This system has no unique solution.\n"
            "Cramer's Rule cannot operate in a collapsed universe."
        )
    return det


def replace_column(A, b, col_index):
    """
    THE COLUMN SWAP: Creates matrix Aᵢ by replacing column 'col_index' of A with vector b.

    This is the geometric heart of Cramer's Rule:
    - Take the original parallelepiped (3 column vectors of A)
    - Rip out one column and replace it with b
    - The volume of this NEW shape, divided by the ORIGINAL volume, gives the solution coordinate!

    Parameters:
        A: The coefficient matrix (3×3)
        b: The constants vector (3,)
        col_index: Which column to replace (0, 1, or 2)

    Returns:
        A_replaced: The modified matrix with column swapped
    """
    A_replaced = A.copy()
    A_replaced[:, col_index] = b
    return A_replaced


def cramers_solve(A, b):
    """
    🌌 THE GRAND SOLVER: Cramer's Rule in full glory.

    For the system Ax = b:
        x₁ = det(A₁) / det(A)    where A₁ has column 1 replaced with b
        x₂ = det(A₂) / det(A)    where A₂ has column 2 replaced with b
        x₃ = det(A₃) / det(A)    where A₃ has column 3 replaced with b

    Returns a rich dict with ALL intermediate values for visualization:
    {
        "det_A":  float,           # Volume of original parallelepiped
        "det_A1": float,           # Volume after replacing column 1
        "det_A2": float,           # Volume after replacing column 2
        "det_A3": float,           # Volume after replacing column 3
        "A1": np.array,            # Modified matrix A₁
        "A2": np.array,            # Modified matrix A₂
        "A3": np.array,            # Modified matrix A₃
        "solution": np.array,      # The final [x₁, x₂, x₃]
    }
    """
    # STEP 1: Compute the Original Universe Volume
    det_A = compute_det(A)

    # STEP 2: The Three Swaps — Replace each column and measure the new volume
    A1 = replace_column(A, b, 0)
    A2 = replace_column(A, b, 1)
    A3 = replace_column(A, b, 2)

    det_A1 = np.linalg.det(A1)
    det_A2 = np.linalg.det(A2)
    det_A3 = np.linalg.det(A3)

    # STEP 3: The Ratios ARE the Solution
    x1 = det_A1 / det_A
    x2 = det_A2 / det_A
    x3 = det_A3 / det_A

    solution = np.array([x1, x2, x3])

    return {
        "det_A": det_A,
        "det_A1": det_A1,
        "det_A2": det_A2,
        "det_A3": det_A3,
        "A1": A1,
        "A2": A2,
        "A3": A3,
        "solution": solution
    }


def verify_solution(A, b, x, tol=1e-9):
    """
    SANITY CHECK: Does Ax actually equal b?
    Computes ||Ax - b|| and checks if it's essentially zero.
    """
    residual = A @ x - b
    norm = np.linalg.norm(residual)
    is_valid = norm < tol

    if not is_valid:
        print(f"⚠️  VERIFICATION WARNING: ||Ax - b|| = {norm:.2e} (tolerance: {tol:.2e})")
    return is_valid


def print_report(A, b, result):
    """
    📊 DIMENSIONAL ANALYSIS REPORT
    Prints all the intermediate Cramer's Rule calculations in cinematic style.
    """
    print("\n" + "=" * 60)
    print("🔮 CRAMER'S RULE — DIMENSIONAL ANALYSIS REPORT 🔮")
    print("=" * 60)

    print(f"\n📐 System: Ax = b")
    print(f"\n   A = ")
    for row in A:
        print(f"       [{row[0]:8.3f}  {row[1]:8.3f}  {row[2]:8.3f}]")
    print(f"\n   b = [{b[0]:.3f}, {b[1]:.3f}, {b[2]:.3f}]")

    print(f"\n🌌 VOLUME OF ORIGINAL PARALLELEPIPED:")
    print(f"   det(A) = {result['det_A']:.6f}")

    print(f"\n🔄 COLUMN REPLACEMENT VOLUMES:")
    print(f"   det(A₁) = {result['det_A1']:10.6f}  →  x₁ = det(A₁)/det(A) = {result['solution'][0]:.6f}")
    print(f"   det(A₂) = {result['det_A2']:10.6f}  →  x₂ = det(A₂)/det(A) = {result['solution'][1]:.6f}")
    print(f"   det(A₃) = {result['det_A3']:10.6f}  →  x₃ = det(A₃)/det(A) = {result['solution'][2]:.6f}")

    print(f"\n✅ SOLUTION VECTOR:")
    print(f"   x = [{result['solution'][0]:.6f}, {result['solution'][1]:.6f}, {result['solution'][2]:.6f}]")

    is_valid = verify_solution(A, b, result['solution'])
    if is_valid:
        print(f"\n🎯 VERIFICATION: Ax = b  ✅ PERFECT MATCH")
    else:
        print(f"\n⚠️  VERIFICATION: Ax ≠ b — NUMERICAL DRIFT DETECTED")

    print("=" * 60 + "\n")
