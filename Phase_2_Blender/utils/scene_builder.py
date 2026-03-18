import bpy
import math
import numpy as np


def clear_scene():
    """Nukes everything in the current Blender scene and prevents Memory Leaks."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)

    for ng in bpy.data.node_groups:
        if ng.name.startswith("TubeGen_"):
            bpy.data.node_groups.remove(ng)

    print("🧹 SCENE BUILDER: Dark Void Cleared.")


def setup_world_lighting():
    """Sets render engine and dark void background."""
    if (4, 2, 0) <= bpy.app.version < (5, 0, 0):
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    bpy.context.scene.render.fps = 60  # 60 FPS Locked

    world = bpy.data.worlds.get("World")
    if world and world.use_nodes:
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0.005, 0.005, 0.01, 1.0)

    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'RENDERED'
                            space.shading.use_scene_lights = True
                            space.shading.use_scene_world = True
    except Exception:
        pass


def give_thickness(obj, thickness=0.015):
    """Converts 1D math lines into solid 3D tubes using Geometry Nodes."""
    mod = obj.modifiers.new(name="Neon_Tube", type='NODES')
    tree = bpy.data.node_groups.new(name=f"TubeGen_{obj.name}", type='GeometryNodeTree')
    mod.node_group = tree

    tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    nodes = tree.nodes
    links = tree.links

    in_node = nodes.new('NodeGroupInput')
    out_node = nodes.new('NodeGroupOutput')
    m2c = nodes.new('GeometryNodeMeshToCurve')
    c2m = nodes.new('GeometryNodeCurveToMesh')
    circle = nodes.new('GeometryNodeCurvePrimitiveCircle')
    set_mat = nodes.new('GeometryNodeSetMaterial')

    circle.inputs['Radius'].default_value = thickness
    circle.inputs['Resolution'].default_value = 8

    if obj.data.materials:
        set_mat.inputs['Material'].default_value = obj.data.materials[0]

    links.new(in_node.outputs[0], m2c.inputs[0])
    links.new(m2c.outputs[0], c2m.inputs[0])
    links.new(circle.outputs[0], c2m.inputs[1])
    links.new(c2m.outputs[0], set_mat.inputs[0])
    links.new(set_mat.outputs[0], out_node.inputs[0])


def build_arrow(name, material, tip_coord):
    """Builds a thick 3D vector arrow from origin to tip_coord."""
    x = float(tip_coord[0])
    y = float(tip_coord[1])
    z = float(tip_coord[2])

    verts = [(0.0, 0.0, 0.0), (x, y, z)]
    edges = [(0, 1)]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    give_thickness(obj, thickness=0.06)

    return obj


def build_lattice(name, material, size=3, step=1):
    """Constructs a 3D Space Lattice (Cube Grid)."""
    verts = []
    edges = []

    for y in range(-size, size + 1, step):
        for z in range(-size, size + 1, step):
            v_start = len(verts)
            verts.append((-size, y, z))
            verts.append((size, y, z))
            edges.append((v_start, v_start + 1))

    for x in range(-size, size + 1, step):
        for z in range(-size, size + 1, step):
            v_start = len(verts)
            verts.append((x, -size, z))
            verts.append((x, size, z))
            edges.append((v_start, v_start + 1))

    for x in range(-size, size + 1, step):
        for y in range(-size, size + 1, step):
            v_start = len(verts)
            verts.append((x, y, -size))
            verts.append((x, y, size))
            edges.append((v_start, v_start + 1))

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    give_thickness(obj, thickness=0.005)

    return obj


def build_parallelepiped(name, v1, v2, v3, material):
    """
    🧊 THE VOLUME MAKER: Constructs a parallelepiped from 3 column vectors.

    The 8 vertices are all combinations of 0/1 coefficients of v1, v2, v3:
        vertex = c1*v1 + c2*v2 + c3*v3   where c1, c2, c3 ∈ {0, 1}

    This is the geometric object whose VOLUME = |det([v1, v2, v3])|
    """
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    v3 = np.array(v3, dtype=float)

    # 8 vertices: all binary combinations of the 3 vectors
    coefficients = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]
    verts = []
    for c1, c2, c3 in coefficients:
        point = c1 * v1 + c2 * v2 + c3 * v3
        verts.append(tuple(point))

    # 6 faces of the parallelepiped
    # Vertex indices based on the order above:
    # 0=(0,0,0), 1=(1,0,0), 2=(0,1,0), 3=(0,0,1),
    # 4=(1,1,0), 5=(1,0,1), 6=(0,1,1), 7=(1,1,1)
    faces = [
        (0, 1, 4, 2),  # bottom (z=0 plane spanned by v1, v2)
        (3, 5, 7, 6),  # top (shifted by v3)
        (0, 1, 5, 3),  # front (spanned by v1, v3)
        (2, 4, 7, 6),  # back (shifted by v2)
        (0, 2, 6, 3),  # left (spanned by v2, v3)
        (1, 4, 7, 5),  # right (shifted by v1)
    ]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    return obj


def build_parallelepiped_wireframe(name, v1, v2, v3, material):
    """
    Constructs the EDGES ONLY of a parallelepiped — glowing wireframe outline.
    Same 8 vertices as build_parallelepiped, but only edges, no faces.
    """
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    v3 = np.array(v3, dtype=float)

    coefficients = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]
    verts = []
    for c1, c2, c3 in coefficients:
        point = c1 * v1 + c2 * v2 + c3 * v3
        verts.append(tuple(point))

    # 12 edges of a parallelepiped
    edges = [
        (0, 1), (0, 2), (0, 3),    # from origin
        (1, 4), (1, 5),             # from v1
        (2, 4), (2, 6),             # from v2
        (3, 5), (3, 6),             # from v3
        (4, 7), (5, 7), (6, 7)     # to v1+v2+v3
    ]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    give_thickness(obj, thickness=0.02)

    return obj


def build_solution_marker(name, position, material, radius=0.12):
    """🎯 Glowing sphere at the solution point."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=tuple(position),
        segments=24,
        ring_count=16
    )
    obj = bpy.context.active_object
    obj.name = name

    obj.data.materials.append(material)

    return obj


def setup_camera(frame_start=1, frame_end=960):
    """
    📷 CINEMATIC ORBIT CAMERA
    - 50° elevation for dramatic eye-level 3D
    - Tracks origin via Empty + Track To constraint
    - Slow 30° orbit over the full timeline
    """
    cam_data = bpy.data.cameras.new("Main_Cam")
    
    # 👁️ Perspective with 32mm wide-angle for dramatic depth
    cam_data.type = 'PERSP' 
    cam_data.lens = 32.0

    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # 🎯 TRACKING TARGET: invisible Empty at world origin
    target = bpy.data.objects.new("Cam_Target", None)
    target.location = (0.0, 0.0, 0.0)
    target.empty_display_size = 0.01  # effectively invisible
    bpy.context.collection.objects.link(target)

    # 🔗 Track To constraint — camera always looks at center
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # 📐 ORBIT RIG: parent camera to target, position on a diagonal
    cam_obj.parent = target

    # Distance ~15 units from origin, 50° elevation (eye-level dramatic)
    # Using spherical → cartesian: r=15, elevation=50°, azimuth=45°
    elev = math.radians(50.0)
    azim_start = math.radians(45.0)
    r = 15.0
    
    cam_x = r * math.cos(elev) * math.cos(azim_start)
    cam_y = r * math.cos(elev) * math.sin(azim_start) * -1  # Blender -Y = forward
    cam_z = r * math.sin(elev)
    cam_obj.location = (cam_x, cam_y, cam_z)

    # 🎬 SLOW ORBIT: rotate the target empty 30° over the full timeline
    # This sweeps the camera around the scene smoothly
    target.rotation_euler = (0.0, 0.0, 0.0)
    target.keyframe_insert(data_path="rotation_euler", frame=frame_start)

    target.rotation_euler = (0.0, 0.0, math.radians(30.0))
    target.keyframe_insert(data_path="rotation_euler", frame=frame_end)

    # Smooth the orbit (linear for steady sweep, falls back to Bezier in Blender 5.0+)
    try:
        if target.animation_data and target.animation_data.action:
            for fc in target.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
    except AttributeError:
        pass  # Blender 5.0+ uses layered actions — default Bezier easing is fine

    #NEON IMPACT OVERRIDE (Turn on Bloom for glowing materials)
    try:
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_intensity = 0.04
    except Exception:
        pass  # Ignored if using Blender 4.2+ EEVEE Next (handles glow natively)

    return cam_obj

