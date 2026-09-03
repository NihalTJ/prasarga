"""
Physics Realism Enhancer — ensures generated video prompts produce output where
all objects obey the laws of physics.

Adds physics-accurate direction to prompts: gravity, fluid dynamics, thermodynamics,
light behavior, material properties, motion accuracy, and natural effects.

This is critical because AI video models can produce physically impossible results
(objects floating, water flowing upward, light ignoring refraction) that instantly
break realism. This module injects explicit physics constraints into the prompt.
"""

# Physics domain keywords that enforce realism
PHYSICS_DIRECTIVES = {
    "gravity": "objects obey gravity: falling objects accelerate at 9.8 m/s², "
               "nothing floats without support, thrown objects follow parabolic arcs",
    "fluid_dynamics": "liquids flow downhill and follow surface contours, water "
                      "splashes realistically with droplet formation, viscous fluids "
                      "move slowly and form smooth surfaces, liquids maintain volume",
    "thermodynamics": "heat rises as visible convection currents, hot objects glow "
                      "according to blackbody radiation (dull red → bright white), "
                      "steam forms from condensation patterns, heat transfer is gradual",
    "optics": "light follows inverse-square law for intensity, reflections match "
              "surface geometry, refraction follows Snell's law, shadows are cast "
              "in correct directions from light source, transparent materials bend light",
    "material_science": "glass shatters into sharp irregular shards following stress "
                        "lines, metals deform plastically before breaking, ice cracks "
                        "along crystal boundaries, wood splinters along grain",
    "motion": "acceleration is gradual not instantaneous, momentum is conserved in "
              "collisions, heavier objects move slower with same force, rotational "
              "motion follows angular momentum conservation",
    "atmospheric": "atmospheric perspective makes distant objects lighter and bluer, "
                   "fog diffuses light realistically, rain falls at terminal velocity "
                   "angle, wind affects light objects more than heavy ones",
    "surface_tension": "water droplets form beads on hydrophobic surfaces, capillary "
                       "action draws liquid upward in narrow spaces, surface tension "
                       "creates meniscus curves at container edges",
}

# Map physics principles to specific directives
PRINCIPLE_MAP = {
    "compressive stress": ["material_science", "motion"],
    "tensile stress": ["material_science", "motion"],
    "tempered glass": ["material_science", "optics"],
    "rapid cooling": ["thermodynamics", "material_science"],
    "stress waves": ["material_science", "motion"],
    "shear thickening": ["fluid_dynamics", "motion"],
    "non-Newtonian fluid dynamics": ["fluid_dynamics", "motion"],
    "viscosity": ["fluid_dynamics"],
    "impact force": ["motion", "material_science"],
    "pressure waves": ["motion", "fluid_dynamics"],
    "standing waves": ["motion", "surface_tension"],
    "resonance": ["motion"],
    "nodal lines": ["motion", "surface_tension"],
    "frequency": ["motion"],
    "vibration modes": ["motion"],
    "electromagnetic interaction": ["optics", "atmospheric"],
    "solar wind": ["atmospheric", "optics"],
    "atmospheric excitation": ["optics", "thermodynamics"],
    "magnetic field lines": ["optics", "motion"],
    "photon emission": ["optics"],
    "catalytic decomposition": ["thermodynamics", "fluid_dynamics"],
    "exothermic reaction": ["thermodynamics", "optics"],
    "gas evolution": ["fluid_dynamics", "thermodynamics"],
    "surface tension": ["surface_tension", "fluid_dynamics"],
    "thermal expansion": ["thermodynamics", "material_science"],
    "chemiluminescence": ["optics"],
    "energy transfer": ["thermodynamics", "optics"],
    "electron excitation": ["optics"],
    "fluorescence": ["optics"],
    "crystal growth": ["material_science", "thermodynamics"],
    "hopper crystal formation": ["material_science"],
    "thin-film interference": ["optics"],
    "oxidation": ["thermodynamics", "optics"],
    "melting point": ["thermodynamics"],
    "bioluminescence": ["optics"],
    "luciferin-luciferase reaction": ["optics", "thermodynamics"],
    "mechanical stimulation": ["motion"],
    "blue light spectrum": ["optics"],
    "triboelectric charging": ["optics", "atmospheric"],
    "charge separation": ["optics", "motion"],
    "electrical discharge": ["optics", "atmospheric"],
    "plume dynamics": ["fluid_dynamics", "atmospheric"],
    "static electricity": ["optics", "motion"],
    "capillary action": ["surface_tension", "fluid_dynamics"],
    "freezing point depression": ["thermodynamics"],
    "ice nucleation": ["thermodynamics", "material_science"],
    "supercooling": ["thermodynamics"],
    "crystallization": ["material_science", "thermodynamics"],
    "glass fracture mechanics": ["material_science", "optics"],
    "cleavage planes": ["material_science"],
    "light refraction": ["optics"],
    "caustics": ["optics"],
    "stress propagation": ["material_science", "motion"],
    "magnetic field interaction": ["motion", "optics"],
    "Rosensweig instability": ["fluid_dynamics", "surface_tension"],
    "ferromagnetism": ["motion", "material_science"],
    "nanoparticle dynamics": ["fluid_dynamics", "motion"],
    "cohesive forces": ["surface_tension", "fluid_dynamics"],
    "granular physics": ["fluid_dynamics", "material_science"],
    "light attenuation": ["optics", "atmospheric"],
    "hydrostatic pressure": ["fluid_dynamics", "motion"],
    "Beer-Lambert law": ["optics"],
    "deep-sea biology": ["optics", "atmospheric"],
    "scale invariance": ["optics", "motion"],
    "atomic structure": ["optics"],
    "orbital mechanics": ["motion", "gravity"],
    "galactic structure": ["optics", "atmospheric"],
    "cosmic web topology": ["optics"],
    "thermodynamics": ["thermodynamics"],
    "combustion": ["thermodynamics", "fluid_dynamics", "optics"],
    "mechanical engineering": ["motion", "material_science"],
    "4-stroke cycle": ["thermodynamics", "motion", "fluid_dynamics"],
    "energy conversion": ["thermodynamics", "motion"],
}


def enhance_physics_realism(
    prompt: str,
    physics_principles: list[str] | None = None,
    maximize_realism: bool = True,
) -> dict:
    """
    Enhance a prompt with physics-accurate directives to ensure realistic output.

    Args:
        prompt: The base prompt text.
        physics_principles: List of specific physics principles to enforce.
        maximize_realism: If True, adds maximum physics directives.

    Returns:
        {
            "enhanced_prompt": str — the prompt with physics constraints added,
            "physics_notes": list[str] — human-readable notes about what was added,
        }
    """
    enhanced = prompt.strip()
    notes = []

    # Always add core physics directives
    core_directives = ["gravity", "optics", "motion"]
    added_directives = set()

    for key in core_directives:
        if key not in added_directives:
            enhanced += f". {PHYSICS_DIRECTIVES[key]}"
            added_directives.add(key)
            notes.append(f"Added {key.replace('_', ' ')} constraints")

    # Add principle-specific directives
    if physics_principles:
        for principle in physics_principles:
            mapped_keys = PRINCIPLE_MAP.get(principle, [])
            for key in mapped_keys:
                if key not in added_directives:
                    enhanced += f". {PHYSICS_DIRECTIVES[key]}"
                    added_directives.add(key)
                    notes.append(f"Added {key.replace('_', ' ')} for {principle}")

    if maximize_realism:
        # Add remaining directives for maximum realism
        for key, directive in PHYSICS_DIRECTIVES.items():
            if key not in added_directives:
                enhanced += f". {directive}"
                added_directives.add(key)
                notes.append(f"Added {key.replace('_', ' ')} for maximum realism")

    # Add explicit physics enforcement instruction
    enhanced += (
        ". All objects must obey the laws of physics: no floating, no impossible "
        "motion, no physics-breaking interactions. Every natural effect — gravity, "
        "friction, air resistance, surface tension, light scattering — must behave "
        "exactly as in the real world. Output must be indistinguishable from real footage."
    )

    return {
        "enhanced_prompt": enhanced,
        "physics_notes": notes,
    }


def get_physics_directives() -> dict:
    """Return all available physics directives (for UI display)."""
    return PHYSICS_DIRECTIVES
