# 🌌 Cramer's Rule 3D
### Project 04 — Geometric Linear System Solver

> *"The solution is a ratio of volumes."*

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.0+-013243?style=flat-square&logo=numpy)
![Blender](https://img.shields.io/badge/Blender-5.x-E87D0D?style=flat-square&logo=blender&logoColor=white)
![Status](https://img.shields.io/badge/Complete-00ffc8?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-a78bfa?style=flat-square)

---

## 🎬 Cinematic Renders — 1920×1080 · 60fps · EEVEE

| Clean System | Skewed System |
|:---:|:---:|
| ![clean](docs/assets/renders/Project_04_clean.gif) | ![skewed](docs/assets/renders/Project_04_skewed.gif) |
| Integer solution [1, 2, 3] — clean column swaps | Tilted columns — irrational decimals, Cramer still wins |

| Physical System (Kirchhoff's Circuit) |
|:---:|
| ![physical](docs/assets/renders/Project_04_physical.gif) |
| Real-world resistor network — 3 loop currents solved |

---

## 🧠 The Core Insight

```
Cramer's Rule says:

   x₁ = det(A₁) / det(A)
   x₂ = det(A₂) / det(A)
   x₃ = det(A₃) / det(A)

where Aᵢ = matrix A with column i replaced by b.

The determinant of a 3×3 matrix IS the volume of a parallelepiped.
Cramer's Rule is literally: "the solution is a RATIO OF VOLUMES."
```

This project **animates that process** — you see the original parallelepiped, then watch each column swap morph the shape, changing its volume.

---

## 🔬 The 4-Act Cinematic

| Act | What Happens | Duration |
|---|---|---|
| **Act 1** — The System | Original parallelepiped appears (3 column vectors of A + vector b) | 4 sec |
| **Act 2** — Cramer x₁ | Column a₁ morphs into b → new volume = det(A₁) | 4 sec |
| **Act 3** — Cramer x₂ | Column a₂ morphs into b → new volume = det(A₂) | 4 sec |
| **Act 4** — Cramer x₃ | Column a₃ morphs into b → new volume = det(A₃) | 4 sec |
| **Finale** | Solution point appears at intersection | 1 sec |

Camera slowly **orbits 30°** around the scene for cinematic depth.

---

## 🌌 The 3 Solvable Systems

| System | Matrix A | Vector b | Solution | det(A) |
|---|---|---|---|---|
| **Clean** | Well-behaved integers | [7, 13, 1] | [1, 2, 3] | Non-zero |
| **Skewed** | Tilted, non-orthogonal | [4, 1, 11] | Irrational decimals | Non-zero |
| **Physical** | Kirchhoff's circuit | [12, 0, -6] | Loop currents | Non-zero |

There's also a **Singular** system (det = 0) — Cramer's Rule correctly **refuses to solve it** because the parallelepiped has zero volume.

---

## 🏗️ Architecture

```
project_4_Cramers_Rule/
│
├── 📄 README.md
│
├── 🐍 Phase_1_Logic/
│   ├── cramers_rule.py       ← Cramer's engine: column swap, det ratio, verification
│   └── systems.py            ← 4 preset linear systems (clean, skewed, singular, physical)
│
├── 🎨 Phase_2_Blender/
│   ├── scenes/
│   │   └── cramers_solve.py  ← Entry point — set SYSTEM_NAME and run in Blender
│   └── utils/
│       ├── materials.py      ← RGB neon palette + translucent parallelepiped fills
│       ├── scene_builder.py  ← Grid, arrows, parallelepiped, orbit camera, solution marker
│       └── animator.py       ← Column swap Shape Keys + cinematic interpolation
│
└── 📸 docs/assets/renders/
    ├── Project_04_clean.gif
    ├── Project_04_skewed.gif
    └── Project_04_physical.gif
```

---

## 🚀 Quick Start

### Phase 1 — Python Logic
```bash
pip3 install -r requirements.txt
cd Phase_1_Logic
python3 -c "import systems, cramers_rule; s = systems.get_system('clean'); r = cramers_rule.cramers_solve(s['A'], s['b']); cramers_rule.print_report(s['A'], s['b'], r)"
```

### Phase 2 — Blender Cinematic
```
1. Open Blender 5.x
2. Scripting tab → Open → Phase_2_Blender/scenes/cramers_solve.py
3. Set SYSTEM_NAME = "clean"  (or "skewed" / "physical")
4. ▶ Run Script
5. Render → Render Animation  (Ctrl+F12)
```

**3 solvable presets:**
```
clean     → Integer solution [1, 2, 3] — hand-verifiable
skewed    → Non-orthogonal columns — irrational solution
physical  → Kirchhoff's circuit — real-world engineering
```

---

## ✅ Verification

For the `clean` system, a successful Phase 1 run should:
- print a non-zero `det(A)`
- print the solution vector `[1.000000, 2.000000, 3.000000]`
- end with `VERIFICATION: Ax = b  ✅ PERFECT MATCH`

For the `singular` system, the solver should refuse to solve because `det(A) ≈ 0`.

---

## 📐 Part of the Simulation Architect Path

| # | Project | Status |
|---|---|---|
| 01 | 2D Linear Transform Animator | ✅ Complete |
| 02 | 3D Linear Transform Animator | ✅ Complete |
| 03 | Basis Translator 3D | ✅ Complete |
| **04** | **Cramer's Rule 3D** ← *here* | ✅ Complete |
| 05 | Eigenvector Explorer | ✅ Complete |
| 06A | Solar System Simulator | ⏳ |
| **06B** | **PROJECT VOID** | ⏳ |
| 07 | Neural Network Visual Simulator | ⏳ |
| 08 | Optical Fiber Simulator | ⏳ |
| 09 | VOID AI — RL Navigator | ⏳ |
| 10 | Omniverse Digital Twin | ⏳ |

---

## 👨‍💻 Author

**Divyansh Ailani** — Simulation Architect in progress

*BCA Student · Kanpur, India → The World*

> "Mathematics is the language of the universe. I am learning to read it."

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/divyansh-ailani-225925380/)
[![GitHub](https://img.shields.io/badge/GitHub-divyanshailani-181717?style=flat-square&logo=github)](https://github.com/divyanshailani)

---

*Part of the **Simulation Architect Path** — from linear algebra to NVIDIA Omniverse. 🌌*
