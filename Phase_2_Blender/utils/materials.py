import bpy


def create_emission_material(name, color_rgba, color_strength=5.0):
    """Creates a glowing neon material using Blender's C++ shader nodes."""
    if name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[name])

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Color'].default_value = color_rgba
    node_emission.inputs['Strength'].default_value = color_strength

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    return mat


def create_translucent_material(name, color_rgba, emission_strength=3.0, alpha=0.3):
    """Creates a glowing, translucent material for parallelepiped faces."""
    if name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[name])

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Color'].default_value = color_rgba
    node_emission.inputs['Strength'].default_value = emission_strength

    node_transparent = nodes.new(type='ShaderNodeBsdfTransparent')

    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_mix.inputs[0].default_value = alpha  # Fac: 0 = fully transparent, 1 = fully emission

    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    links.new(node_transparent.outputs['BSDF'], node_mix.inputs[1])
    links.new(node_emission.outputs['Emission'], node_mix.inputs[2])
    links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])

    return mat


def setup_cramers_materials():
    """
    🎨 THE CRAMER'S PALETTE
    Spawns all materials needed for the geometric Cramer's Rule visualization.
    """

    # 🔴🟢🔵 COLUMN VECTORS of A (The 3 edges of the parallelepiped)
    col1_color = (1.0, 0.15, 0.1, 1.0)    # Neon Red — Column a₁
    col2_color = (0.1, 1.0, 0.15, 1.0)    # Neon Green — Column a₂
    col3_color = (0.15, 0.3, 1.0, 1.0)    # Neon Blue — Column a₃

    # ⚪ THE b VECTOR (The target — what we're solving for)
    b_color = (1.0, 1.0, 1.0, 1.0)        # Pure White

    # 🟦 ORIGINAL PARALLELEPIPED FILL (det(A) volume)
    orig_fill = (0.0, 0.6, 0.8, 1.0)      # Cyan

    # 🟨 REPLACEMENT PARALLELEPIPED FILLS (det(Aᵢ) volumes)
    swap1_fill = (1.0, 0.3, 0.2, 1.0)     # Red-Orange (a₁ → b)
    swap2_fill = (0.3, 1.0, 0.2, 1.0)     # Lime (a₂ → b)
    swap3_fill = (0.3, 0.4, 1.0, 1.0)     # Royal Blue (a₃ → b)

    # 🟣 SOLUTION POINT
    sol_color = (1.0, 0.0, 1.0, 1.0)      # Magenta

    # 🔲 GHOST GRID
    grid_color = (0.0, 0.3, 0.4, 1.0)     # Faint Teal

    mats = {
        # Column vector arrows
        'col1':     create_emission_material("Mat_Col1", col1_color, 12.0),
        'col2':     create_emission_material("Mat_Col2", col2_color, 12.0),
        'col3':     create_emission_material("Mat_Col3", col3_color, 12.0),

        # b vector
        'b_vec':    create_emission_material("Mat_B_Vec", b_color, 20.0),

        # Parallelepiped faces (translucent)
        'orig_piped':  create_translucent_material("Mat_Orig_Piped", orig_fill, 3.0, 0.25),
        'swap1_piped': create_translucent_material("Mat_Swap1_Piped", swap1_fill, 6.0, 0.35),
        'swap2_piped': create_translucent_material("Mat_Swap2_Piped", swap2_fill, 6.0, 0.35),
        'swap3_piped': create_translucent_material("Mat_Swap3_Piped", swap3_fill, 6.0, 0.35),

        # Solution point
        'solution': create_emission_material("Mat_Solution", sol_color, 25.0),

        # Ghost grid
        'grid':     create_emission_material("Mat_Grid", grid_color, 2.0),
    }

    print("🎨 CRAMER'S PAINT SHOP: All materials loaded!")
    return mats
