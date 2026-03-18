import bpy
import numpy as np


def animate_mesh_transformation(obj, target_matrix, frame_start=1, frame_end=180):
    """
    Uses Blender's native C++ Shape Keys to perform mathematically perfect 3D Matrix Lerp.
    Morphs mesh vertices from their current positions to M @ original_position.
    """
    M = np.array(target_matrix)

    # 1: Create the 'Identity' state
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    # 2: Create the 'Transformed' state
    sk_target = obj.shape_key_add(name="Transformed")

    for i, v in enumerate(obj.data.vertices):
        orig_co = np.array([v.co.x, v.co.y, v.co.z])
        new_co = M @ orig_co

        sk_target.data[i].co.x = new_co[0]
        sk_target.data[i].co.y = new_co[1]
        sk_target.data[i].co.z = new_co[2]

    # 3: Animate the Lerp (Shape Key Value 0.0 -> 1.0)
    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=frame_start)

    sk_target.value = 1.0
    sk_target.keyframe_insert(data_path="value", frame=frame_end)


def animate_column_swap(obj, orig_columns, b_vec, col_index, frame_start, frame_end):
    """
    🔄 THE COLUMN SWAP ANIMATION
    Morphs a parallelepiped by replacing one column vector with b.

    For a parallelepiped built from columns [v1, v2, v3]:
    - If col_index=0: morphs all vertices as if v1 → b
    - If col_index=1: morphs all vertices as if v2 → b
    - If col_index=2: morphs all vertices as if v3 → b

    The mesh vertices are at positions c1*v1 + c2*v2 + c3*v3 for c∈{0,1}.
    After swap: c1*v1_new + c2*v2_new + c3*v3_new where one v is replaced by b.
    """
    v1 = np.array(orig_columns[0], dtype=float)
    v2 = np.array(orig_columns[1], dtype=float)
    v3 = np.array(orig_columns[2], dtype=float)
    b = np.array(b_vec, dtype=float)

    # Build the target columns (one replaced with b)
    target_cols = [v1.copy(), v2.copy(), v3.copy()]
    target_cols[col_index] = b.copy()

    # The 8 vertices correspond to binary combos of columns
    coefficients = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]

    # Create shape key for this swap
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    sk_name = f"Swap_Col{col_index + 1}"
    sk_target = obj.shape_key_add(name=sk_name)

    for i, (c1, c2, c3) in enumerate(coefficients):
        new_pos = c1 * target_cols[0] + c2 * target_cols[1] + c3 * target_cols[2]
        sk_target.data[i].co.x = new_pos[0]
        sk_target.data[i].co.y = new_pos[1]
        sk_target.data[i].co.z = new_pos[2]

    # Keyframe: morph in then morph back
    # Stay at 0 until frame_start
    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=1)
    sk_target.keyframe_insert(data_path="value", frame=frame_start)

    # Morph to swapped state
    morph_duration = int((frame_end - frame_start) * 0.4)
    hold_start = frame_start + morph_duration
    hold_end = frame_end - morph_duration

    sk_target.value = 1.0
    sk_target.keyframe_insert(data_path="value", frame=hold_start)
    sk_target.keyframe_insert(data_path="value", frame=hold_end)

    # Morph back to original
    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=frame_end)


def animate_arrow_swap(obj, original_tip, new_tip, frame_start, frame_end):
    """
    Morphs a single arrow (vector line) from original_tip to new_tip.
    The arrow has 2 vertices: [origin, tip].
    """
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    sk_target = obj.shape_key_add(name="Swapped")

    # Vertex 0 = origin (stays at 0,0,0)
    sk_target.data[0].co.x = 0.0
    sk_target.data[0].co.y = 0.0
    sk_target.data[0].co.z = 0.0

    # Vertex 1 = tip (morphs to new_tip)
    sk_target.data[1].co.x = float(new_tip[0])
    sk_target.data[1].co.y = float(new_tip[1])
    sk_target.data[1].co.z = float(new_tip[2])

    # Morph in, hold, morph back
    morph_duration = int((frame_end - frame_start) * 0.4)
    hold_start = frame_start + morph_duration
    hold_end = frame_end - morph_duration

    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=1)
    sk_target.keyframe_insert(data_path="value", frame=frame_start)

    sk_target.value = 1.0
    sk_target.keyframe_insert(data_path="value", frame=hold_start)
    sk_target.keyframe_insert(data_path="value", frame=hold_end)

    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=frame_end)


def animate_appearance(obj, frame_appear, duration=30):
    """Fade-in via scale animation: 0 → 1 over 'duration' frames."""
    obj.scale = (0.0, 0.0, 0.0)
    obj.keyframe_insert(data_path="scale", frame=frame_appear)

    obj.scale = (1.0, 1.0, 1.0)
    obj.keyframe_insert(data_path="scale", frame=frame_appear + duration)


def set_cinematic_interpolation(obj):
    """Converts linear movement into smooth cinematic Bezier curves."""
    # Check shape key animation
    if obj.data.shape_keys and obj.data.shape_keys.animation_data:
        anim_data = obj.data.shape_keys.animation_data
        if anim_data.action:
            action = anim_data.action
            # Blender 4.4+ Action Slots system
            if hasattr(action, 'layers') and action.layers:
                try:
                    for layer in action.layers:
                        for strip in layer.strips:
                            if hasattr(strip, 'fcurves'):
                                for fcurve in strip.fcurves:
                                    for kp in fcurve.keyframe_points:
                                        kp.interpolation = 'BEZIER'
                except Exception:
                    pass
            # Blender 4.3 and earlier
            elif hasattr(action, 'fcurves'):
                for fcurve in action.fcurves:
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = 'BEZIER'

    # Check object-level animation (scale, location, etc.)
    if obj.animation_data and obj.animation_data.action:
        action = obj.animation_data.action
        if hasattr(action, 'layers') and action.layers:
            try:
                for layer in action.layers:
                    for strip in layer.strips:
                        if hasattr(strip, 'fcurves'):
                            for fcurve in strip.fcurves:
                                for kp in fcurve.keyframe_points:
                                    kp.interpolation = 'BEZIER'
            except Exception:
                pass
        elif hasattr(action, 'fcurves'):
            for fcurve in action.fcurves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'BEZIER'


def run_director(obj):
    """The master switch that smooths all animations on an object."""
    set_cinematic_interpolation(obj)
    print(f"🎬 ANIMATOR: Cinematic keyframes locked for {obj.name}")
