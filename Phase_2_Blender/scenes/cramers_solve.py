import bpy
import sys
import os
import importlib
import numpy as np


# 🧹 FORCE-RELOAD all custom modules (prevents Blender's stale cache)
for module_name in list(sys.modules.keys()):
    if module_name in ['systems', 'cramers_rule', 'materials', 'scene_builder', 'animator'] or module_name.startswith('utils.'):
        del sys.modules[module_name]


# 🌉 THE DIMENSIONAL BRIDGE
path_phase2 = "/Users/divyanshailani/Desktop/project_4_Cramers_Rule/Phase_2_Blender"
path_phase1 = "/Users/divyanshailani/Desktop/project_4_Cramers_Rule/Phase_1_Logic"

if path_phase2 not in sys.path: sys.path.insert(0, path_phase2)
if path_phase1 not in sys.path: sys.path.insert(0, path_phase1)

from utils import materials, scene_builder, animator
import systems, cramers_rule




#  ⚙️  MISSION CONTROL

SYSTEM_NAME = "clean"       # 🟢 Try 'skewed' or 'physical' next!
GRID_SIZE = 3

# 4-Act Animation Timeline (@ 60fps) — ~17 seconds, 1020 frames
ACT1_START = 1              # The System appears
ACT1_END = 240              # Hold the original (4 sec)
ACT2_START = 241            # Cramer x₁ (swap column 1)
ACT2_END = 480
ACT3_START = 481            # Cramer x₂ (swap column 2)
ACT3_END = 720
ACT4_START = 721            # Cramer x₃ (swap column 3)
ACT4_END = 960
SOLUTION_APPEAR = 961       # Solution marker pops in
FRAME_FINAL = 1020          # End of the cinematic (~17 sec)




#  🚀  LAUNCH SEQUENCE
# 
print(f"\n🚀 INITIATING PROJECT 04: CRAMER'S RULE → {SYSTEM_NAME.upper()}")

# FETCH THE SOURCE CODE
sys_data = systems.get_system(SYSTEM_NAME)
A = sys_data["A"]
b = sys_data["b"]

# Solve with Cramer's Rule (all intermediate values)
result = cramers_rule.cramers_solve(A, b)
solution = result["solution"]

# Extract column vectors from A
col1 = A[:, 0]  # First column of A
col2 = A[:, 1]  # Second column of A
col3 = A[:, 2]  # Third column of A
columns = [col1, col2, col3]




#  🧹  CLEAR THE VOID

scene_builder.clear_scene()
scene_builder.setup_world_lighting()

# LOAD THE PALETTE
mats = materials.setup_cramers_materials()




#  🔲  ACT 0: THE GHOST GRID (Silent Reference)

ghost_grid = scene_builder.build_lattice("Ghost_Grid", mats['grid'], size=GRID_SIZE)




#  📐  ACT 1: THE SYSTEM (Build the original parallelepiped)

# Column vectors as arrows
arrow_col1 = scene_builder.build_arrow("Col1_Arrow", mats['col1'], tuple(col1))
arrow_col2 = scene_builder.build_arrow("Col2_Arrow", mats['col2'], tuple(col2))
arrow_col3 = scene_builder.build_arrow("Col3_Arrow", mats['col3'], tuple(col3))

# The b vector (the target)
arrow_b = scene_builder.build_arrow("B_Vec_Arrow", mats['b_vec'], tuple(b))

# Original parallelepiped (translucent fill)
orig_piped = scene_builder.build_parallelepiped(
    "Orig_Piped", col1, col2, col3, mats['orig_piped']
)

# Original parallelepiped (glowing wireframe)
orig_wire = scene_builder.build_parallelepiped_wireframe(
    "Orig_Wire", col1, col2, col3, mats['col1']
)

# Fade everything in during Act 1
for obj in [arrow_col1, arrow_col2, arrow_col3, orig_piped, orig_wire]:
    animator.animate_appearance(obj, frame_appear=1, duration=60)
animator.animate_appearance(arrow_b, frame_appear=40, duration=60)




#  🔄  ACT 2-4: THE THREE COLUMN SWAPS

# Build 3 swap parallelepipeds (one per Cramer substitution)
# Each starts identical to the original, then morphs when its column is swapped

swap_materials = [mats['swap1_piped'], mats['swap2_piped'], mats['swap3_piped']]
swap_arrows = [arrow_col1, arrow_col2, arrow_col3]
act_ranges = [
    (ACT2_START, ACT2_END),
    (ACT3_START, ACT3_END),
    (ACT4_START, ACT4_END)
]

for i in range(3):
    frame_start, frame_end = act_ranges[i]

    # Build a swap parallelepiped (starts as original shape)
    swap_piped = scene_builder.build_parallelepiped(
        f"Swap{i+1}_Piped", col1, col2, col3, swap_materials[i]
    )

    # Animate the column swap: morph column i into b, then back
    animator.animate_column_swap(swap_piped, columns, b, i, frame_start, frame_end)

    # Fade in at the start of this act, fade out at the end
    animator.animate_appearance(swap_piped, frame_appear=frame_start, duration=30)

    # Hide it before and after its act (scale to 0)
    swap_piped.scale = (0.0, 0.0, 0.0)
    swap_piped.keyframe_insert(data_path="scale", frame=1)

    swap_piped.scale = (1.0, 1.0, 1.0)
    swap_piped.keyframe_insert(data_path="scale", frame=frame_start + 30)
    swap_piped.keyframe_insert(data_path="scale", frame=frame_end - 10)

    swap_piped.scale = (0.0, 0.0, 0.0)
    swap_piped.keyframe_insert(data_path="scale", frame=frame_end)

    # Animate the column arrow morphing into b
    animator.animate_arrow_swap(
        swap_arrows[i], columns[i], b, frame_start, frame_end
    )

    # Smooth all keyframes
    animator.run_director(swap_piped)
    animator.run_director(swap_arrows[i])

    print(f"🔄 ACT {i+2}: Column a{i+1} → b  |  det(A{i+1}) = {result[f'det_A{i+1}']:.4f}  |  x{i+1} = {solution[i]:.6f}")




#  🎯  FINALE: THE SOLUTION POINT

sol_marker = scene_builder.build_solution_marker(
    "SOLUTION_POINT", solution, mats['solution']
)
animator.animate_appearance(sol_marker, frame_appear=SOLUTION_APPEAR, duration=30)
animator.run_director(sol_marker)

# Smooth the fade-ins too
for obj in [arrow_col1, arrow_col2, arrow_col3, arrow_b, orig_piped, orig_wire, ghost_grid]:
    animator.run_director(obj)




#  📷  CAMERA

camera = scene_builder.setup_camera(frame_start=1, frame_end=FRAME_FINAL)
bpy.context.scene.frame_end = FRAME_FINAL




#  📊  THE DEEP MATH OUTPUT (Terminal Report)

cramers_rule.print_report(A, b, result)
print(f"🎬 4-ACT CINEMATIC ONLINE: {FRAME_FINAL} frames @ 60fps = {FRAME_FINAL/60:.1f}s")



# ═══════════════════════════════════════════════════════════
#  📦  EXPORT PROTOCOL
# ═══════════════════════════════════════════════════════════
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", f"Project_04_{SYSTEM_NAME}.mp4")
bpy.context.scene.render.filepath = desktop_path

if hasattr(bpy.context.scene.render.image_settings, 'media_type'):
    bpy.context.scene.render.image_settings.media_type = 'VIDEO'
else:
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec = 'H264'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.fps = 60
