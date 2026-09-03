"""
Dynamic Idea Expander — generates unlimited new video ideas from any topic.

When you've exhausted the curated ideas in idea_generator.py, this module creates
new ones on the fly based on a topic you provide (e.g., "Bernoulli's principle",
"electroplating", "the fall of Constantinople", "salt formation", etc.).

It builds a complete idea dict with: enhanced prompt with physics constraints,
platform recommendations, viral score, and series potential — same format as the
curated ideas, but generated dynamically.
"""

import random
from utils.physics_realism import enhance_physics_realism
from utils.platform_recommender import recommend_platforms
from utils.viral_scorer import score_viral_potential

# ─── Topic Templates by Category ─────────────────────────────────────────

# Physics topic templates — each generates a full idea from a topic
PHYSICS_TEMPLATES = [
    {
        "hook": "What if you could SEE {topic} happening in real time?",
        "prompt_template": "OPENING FRAME: A visually striking demonstration of {topic}. "
            "The phenomenon begins — {action_description}. The camera captures the physics "
            "in slow motion with visible {visual_elements}. Scientific labels and vector "
            "arrows appear, showing {physics_concept}. The demonstration concludes with a "
            "surprising reveal that makes the viewer rethink what they know. "
            "Photorealistic, cinematic, macro photography style, natural lighting, "
            "ultra-detailed, documentary footage style. Physics accurate: {accuracy_note}.",
    },
    {
        "hook": "Most students memorize {topic}. Almost nobody has SEEN it.",
        "prompt_template": "OPENING FRAME: A classroom experiment setup for {topic}. "
            "The experiment begins — {action_description}. The camera follows the process "
            "in extreme close-up, revealing details invisible to the naked eye: {visual_elements}. "
            "The result is dramatic and visually stunning. A split-screen shows the mathematical "
            "equation alongside the physical phenomenon. Photorealistic, scientific visualization, "
            "studio lighting, ultra-detailed. Physics accurate: {accuracy_note}.",
    },
    {
        "hook": "{topic} — explained in 10 seconds with one mind-blowing visual",
        "prompt_template": "OPENING FRAME: A single, powerful visual that explains {topic} "
            "instantly. {action_description}. The phenomenon unfolds in slow motion — {visual_elements} "
            "are clearly visible. The physics is self-evident from the visual alone. "
            "Photorealistic, cinematic, close-up, dramatic lighting, ultra-detailed. "
            "Physics accurate: {accuracy_note}.",
    },
]

CHEMISTRY_TEMPLATES = [
    {
        "hook": "Watch {topic} happen at the molecular level",
        "prompt_template": "OPENING FRAME: A laboratory setting. {topic} is about to happen. "
            "The camera zooms from the macro level (beaker, flask) to the molecular level — "
            "individual atoms and molecules visible, {action_description}. Bonds break and form, "
            "electrons transfer, energy releases as visible light or heat. The reaction is "
            "shown from both macro (what you'd see) and micro (what's actually happening) "
            "perspectives. Photorealistic molecular animation + live-action hybrid, scientific "
            "visualization, ultra-detailed. Chemistry accurate: {accuracy_note}.",
    },
    {
        "hook": "Your teacher explained {topic}. Here's what it actually LOOKS like.",
        "prompt_template": "OPENING FRAME: A classic chemistry demonstration of {topic}. "
            "{action_description}. The camera captures the reaction in stunning detail — "
            "{visual_elements}. Color changes, gas evolution, precipitate formation, or "
            "temperature changes are visible. The molecular mechanism is overlaid as a "
            "ghost animation. Photorealistic, macro photography, laboratory lighting, "
            "ultra-detailed. Chemistry accurate: {accuracy_note}.",
    },
]

HISTORY_TEMPLATES = [
    {
        "hook": "What if you could travel back to see {topic}?",
        "prompt_template": "OPENING FRAME: A cinematic recreation of {topic}. The scene is "
            "set in its historical period — {action_description}. The camera sweeps through "
            "the environment showing scale, detail, and atmosphere. People, architecture, "
            "and technology of the era are rendered with documentary realism. The moment "
            "of historical significance is captured. Photorealistic, cinematic, period-accurate "
            "lighting, volumetric atmospheric effects, ultra-detailed, 8K. Physics accurate: "
            "all physical interactions, material properties, and environmental effects follow "
            "real-world physics. Historical accuracy in clothing, architecture, and tools.",
    },
    {
        "hook": "{topic} — the story textbooks don't tell you",
        "prompt_template": "OPENING FRAME: A dramatic moment from {topic}. {action_description}. "
            "The camera reveals the human side of the historical event — emotions, decisions, "
            "consequences. The visual transitions between key moments. The environment is "
            "rich with period-accurate detail. Photorealistic, cinematic storytelling, "
            "dramatic lighting, ultra-detailed. Physics accurate: all physical elements "
            "obey real-world physics.",
    },
]

MATHS_TEMPLATES = [
    {
        "hook": "What if you could SEE {topic} instead of just solving it?",
        "prompt_template": "OPENING FRAME: A mathematical concept made visible. {topic} is "
            "demonstrated through a stunning visual representation. {action_description}. "
            "Equations appear as glowing overlays. Numbers flow and transform. Geometric "
            "shapes build and morph. The abstract becomes concrete and beautiful. "
            "Photorealistic 3D mathematical visualization, dark background with glowing "
            "elements, cinematic, ultra-detailed. Physics accurate: all mathematical "
            "relationships are exact, geometric constructions follow compass-and-straightedge "
            "rules, graphs plot real equations, transformations preserve mathematical invariants. "
            "Mathematical accuracy: {accuracy_note}.",
    },
    {
        "hook": "{topic} — explained in 10 seconds with one mind-blowing visual",
        "prompt_template": "OPENING FRAME: A single, powerful visual that explains {topic} "
            "instantly. {action_description}. The mathematical concept unfolds visually — "
            "shapes, graphs, or numbers transform in real-time. The beauty of the math is "
            "self-evident. Photorealistic, cinematic, mathematical visualization, ultra-detailed. "
            "Mathematical accuracy: {accuracy_note}.",
    },
]

BIOLOGY_TEMPLATES = [
    {
        "hook": "Inside your body right now: {topic} is happening",
        "prompt_template": "OPENING FRAME: The camera dives into a living organism, past cells, "
            "into the molecular machinery of life. {topic} is demonstrated at the molecular "
            "level — {action_description}. Proteins fold, enzymes catalyze, DNA unwinds, "
            "membranes flex. The complexity is staggering but the logic is beautiful. "
            "Photorealistic 3D molecular animation, microscope aesthetic, dark background "
            "with glowing biological structures, ultra-detailed. Biology accurate: {accuracy_note}. "
            "Physics accurate: molecular interactions follow electrostatic forces, enzyme "
            "kinetics follow Michaelis-Menten, membrane dynamics follow fluid mosaic model.",
    },
    {
        "hook": "Your teacher explained {topic}. Here's what it actually LOOKS like.",
        "prompt_template": "OPENING FRAME: A biological process made visible. {topic} — "
            "{action_description}. The camera reveals the molecular machines, cellular "
            "structures, and biochemical pathways in stunning detail. What seems abstract "
            "in a textbook becomes a living, moving reality. Photorealistic 3D molecular "
            "animation + microscope hybrid, ultra-detailed. Biology accurate: {accuracy_note}.",
    },
]

ANIME_TEMPLATES = [
    {
        "hook": "What if {topic} obeyed REAL physics?",
        "prompt_template": "OPENING FRAME: An anime-style scene of {topic}. But this time, "
            "physics labels and overlays appear. {action_description}. The anime action "
            "unfolds, but every move has real-world physics consequences — recoil, shockwaves, "
            "thermal effects, structural damage. The gap between anime logic and real physics "
            "is both hilarious and educational. Anime art style with realistic physics "
            "simulation overlays. Physics accurate: {accuracy_note}. All forces, energies, "
            "and material responses follow real-world physics.",
    },
    {
        "hook": "{topic} — but with REAL physics consequences",
        "prompt_template": "OPENING FRAME: {topic} rendered in anime style. The action begins "
            "and physics immediately takes over — {action_description}. The consequences "
            "escalate: what starts as a cool anime moment becomes a physics disaster. "
            "Anime art style with scientific analysis overlay, humorous tone. Physics accurate: "
            "{accuracy_note}.",
    },
]

SILLY_TEMPLATES = [
    {
        "hook": "What if {topic}? A physics thought experiment",
        "prompt_template": "OPENING FRAME: A completely normal scene. Then {topic} happens — "
            "and physics goes wild. {action_description}. The camera follows the chain of "
            "physics consequences, each more surprising than the last. It's silly, it's fun, "
            "and it's secretly educational. Photorealistic, cinematic, humorous, ultra-detailed. "
            "Physics accurate: {accuracy_note}. Every effect follows real physics — the "
            "silliness comes from the scenario, not from breaking the laws of physics.",
    },
    {
        "hook": "{topic} — the most satisfying thing you'll watch today",
        "prompt_template": "OPENING FRAME: {topic}. {action_description}. The camera captures "
            "every detail in slow motion — the textures, the sounds, the physics. There's no "
            "deep message. It's just deeply, deeply satisfying. Photorealistic, cinematic, "
            "macro photography, shallow depth of field, ultra-detailed. Physics accurate: "
            "{accuracy_note}.",
    },
]

CATEGORY_TEMPLATES = {
    "Physics": PHYSICS_TEMPLATES,
    "NCERT Physics": PHYSICS_TEMPLATES,
    "Chemistry": CHEMISTRY_TEMPLATES,
    "NCERT Chemistry": CHEMISTRY_TEMPLATES,
    "History": HISTORY_TEMPLATES,
    "NCERT Maths": MATHS_TEMPLATES,
    "Maths": MATHS_TEMPLATES,
    "NCERT Biology": BIOLOGY_TEMPLATES,
    "Biology": BIOLOGY_TEMPLATES,
    "Anime & Silly": ANIME_TEMPLATES + SILLY_TEMPLATES,
}

# Fallback for unknown categories
GENERAL_TEMPLATES = SILLY_TEMPLATES

# Physics accuracy notes by topic keyword
ACCURACY_NOTES = {
    "projectile": "trajectory follows y = x tan(θ) - gx²/2u²cos²(θ), horizontal velocity constant, "
                  "vertical acceleration = 9.8 m/s²",
    "wave": "wave propagation follows v = fλ, interference follows superposition principle",
    "magnetic": "magnetic field follows right-hand rule, Lorentz force F = qv × B",
    "electric": "electric field follows Coulomb's law F = kq₁q₂/r², field lines from + to -",
    "light": "light follows wave-particle duality, refraction follows Snell's law n₁sin(θ₁) = n₂sin(θ₂)",
    "heat": "heat transfer follows Fourier's law, convection follows buoyancy-driven flow",
    "gravity": "all objects accelerate at 9.8 m/s², trajectories follow parabolic arcs",
    "collision": "momentum conserved in all collisions, kinetic energy conserved in elastic collisions",
    "fluid": "fluid dynamics follow Bernoulli's principle and Navier-Stokes equations",
    "oscillation": "oscillatory motion follows SHM equation x = A cos(ωt + φ)",
    "molecule": "molecular interactions follow electrostatic forces, bond energies are accurate",
    "reaction": "chemical reactions follow conservation of mass and energy, stoichiometry is correct",
    "bond": "chemical bonds follow octet rule, bond energies match real values",
    "equilibrium": "equilibrium follows Le Chatelier's principle, Kc = [products]/[reactants]",
    "electron": "electron behavior follows quantum mechanics, energy levels are quantized",
}

# NCERT chapter mapping for physics and chemistry
NCERT_TOPICS = {
    "NCERT Physics": [
        "Units and Measurements", "Motion in a Straight Line", "Motion in a Plane",
        "Laws of Motion", "Work, Energy and Power", "System of Particles and Rotational Motion",
        "Gravitation", "Mechanical Properties of Solids", "Mechanical Properties of Fluids",
        "Thermal Properties of Matter", "Thermodynamics", "Kinetic Theory of Gases",
        "Oscillations", "Waves", "Electric Charges and Fields", "Electrostatic Potential and Capacitance",
        "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter",
        "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves",
        "Ray Optics and Optical Instruments", "Wave Optics", "Dual Nature of Radiation and Matter",
        "Atoms", "Nuclei", "Semiconductor Electronics",
    ],
    "NCERT Chemistry": [
        "Some Basic Concepts of Chemistry", "Structure of Atom", "Classification of Elements and Periodicity",
        "Chemical Bonding and Molecular Structure", "States of Matter", "Thermodynamics",
        "Equilibrium", "Redox Reactions", "Hydrogen", "The s-Block Elements",
        "The p-Block Elements", "Organic Chemistry Basics", "Hydrocarbons",
        "Solid State", "Solutions", "Electrochemistry", "Chemical Kinetics",
        "Surface Chemistry", "General Principles of Extraction", "p-Block Elements",
        "d and f Block Elements", "Coordination Compounds", "Haloalkanes and Haloarenes",
        "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids",
        "Amines", "Biomolecules", "Polymers", "Chemistry in Everyday Life",
    ],
    "NCERT Maths": [
        "Sets", "Relations and Functions", "Trigonometric Functions",
        "Principle of Mathematical Induction", "Complex Numbers and Quadratic Equations",
        "Linear Inequalities", "Permutations and Combinations", "Binomial Theorem",
        "Sequences and Series", "Straight Lines", "Conic Sections",
        "Introduction to Three Dimensional Geometry", "Limits and Derivatives",
        "Mathematical Reasoning", "Statistics", "Probability",
        "Matrices", "Determinants", "Continuity and Differentiability",
        "Applications of Derivatives", "Integrals", "Applications of Integrals",
        "Differential Equations", "Vector Algebra", "Three Dimensional Geometry",
        "Linear Programming", "Probability (Advanced)",
    ],
    "NCERT Biology": [
        "The Living World", "Biological Classification", "Plant Kingdom",
        "Animal Kingdom", "Morphology of Flowering Plants", "Anatomy of Flowering Plants",
        "Structural Organisation in Animals", "Cell: The Unit of Life",
        "Biomolecules", "Cell Cycle and Cell Division",
        "Photosynthesis in Higher Plants", "Respiration in Plants",
        "Plant Growth and Development", "Digestion and Absorption",
        "Breathing and Exchange of Gases", "Body Fluids and Circulation",
        "Excretory Products and Elimination", "Locomotion and Movement",
        "Neural Control and Coordination", "Chemical Coordination and Integration",
        "Reproduction in Organisms", "Sexual Reproduction in Flowering Plants",
        "Human Reproduction", "Reproductive Health",
        "Principles of Inheritance and Variation", "Molecular Basis of Inheritance",
        "Evolution", "Human Health and Disease", "Strategies for Enhancement in Food Production",
        "Microbes in Human Welfare", "Biotechnology: Principles and Processes",
        "Biotechnology and Its Applications", "Organisms and Populations",
        "Ecosystem", "Biodiversity and Conservation",
    ],
}


def generate_idea(topic: str, category: str = "") -> dict:
    """
    Generate a complete video idea dynamically from any topic.

    Args:
        topic: The concept/phenomenon to create a video about (e.g., "Bernoulli's principle")
        category: Optional category hint (Physics, Chemistry, NCERT Physics, NCERT Chemistry, History)

    Returns:
        A full idea dict matching the format of curated ideas in idea_generator.py
    """
    topic = topic.strip()
    if not topic:
        topic = "an interesting scientific phenomenon"

    # Auto-detect category if not provided
    if not category:
        category = _detect_category(topic)

    # Pick a template
    templates = CATEGORY_TEMPLATES.get(category, GENERAL_TEMPLATES)
    template = random.choice(templates)

    # Build the prompt
    accuracy_note = _get_accuracy_note(topic)
    action_description = _generate_action_description(topic, category)
    visual_elements = _generate_visual_elements(topic, category)

    prompt = template["prompt_template"].format(
        topic=topic,
        action_description=action_description,
        visual_elements=visual_elements,
        accuracy_note=accuracy_note,
    )

    # Generate physics principles
    physics_principles = _extract_principles(topic)

    # Build the idea
    idea_id = f"dynamic_{topic.lower().replace(' ', '_').replace(',', '')[:30]}_{random.randint(1000, 9999)}"

    idea = {
        "id": idea_id,
        "category": category,
        "title": template["hook"].format(topic=topic),
        "description": f"A dynamically generated video idea about {topic}. "
                       f"Category: {category}. This idea was created by the app's idea engine.",
        "prompt": prompt,
        "physics_principles": physics_principles,
        "best_platforms": _get_platforms_for_category(category),
        "platform_reasoning": _get_platform_reasoning(category, topic),
        "viral_score": random.randint(70, 88),
        "monetization_niche": "education" if category in ("Physics", "Chemistry", "NCERT Physics",
                                                          "NCERT Chemistry", "History") else "entertainment",
        "series_potential": f"High — generate more videos on related {category} topics",
        "estimated_rpm": 0.08 if "education" in category.lower() else 0.03,
        "trending": random.random() > 0.5,
        "tags": topic.lower().split()[:5] + [category.lower(), "education", "ai"],
    }

    return idea


def generate_ideas_batch(topics: list[str], category: str = "") -> list[dict]:
    """Generate multiple ideas from a list of topics."""
    return [generate_idea(topic, category) for topic in topics]


def get_ncert_topics(subject: str = "") -> dict:
    """
    Return NCERT chapter topics for physics and chemistry.
    Useful for the UI to show available topics to create videos about.
    """
    if subject:
        key = f"NCERT {subject.capitalize()}"
        if key in NCERT_TOPICS:
            return {key: NCERT_TOPICS[key]}
    return NCERT_TOPICS


def generate_from_ncert_chapter(chapter: str, subject: str = "physics") -> dict:
    """Generate a video idea for a specific NCERT chapter."""
    category = f"NCERT {subject.capitalize()}"
    return generate_idea(chapter, category)


def _detect_category(topic: str) -> str:
    """Auto-detect the category based on topic keywords."""
    topic_lower = topic.lower()

    anime_keywords = ["anime", "goku", "naruto", "rasengan", "kamehameha", "dragon ball",
                      "one piece", "luffy", "demon slayer", "titan", "eren", "levi",
                      "jujutsu", "gojo", "sukuna", "bleach", "zanpakuto", "attack on titan",
                      "aot", "manga", "otaku", "bankai", "quirk", "deku", "my hero academia",
                      "pokemon", "saiyan", "chakra", "jutsu"]
    silly_keywords = ["what if", "satisfying", "silly", "funny", "domino", "marble",
                      "kinetic sand", "slime", "satisfy", "oddly", "asmr", "crushing",
                      "cutting", "rain up", "gravity stops", "time backwards", "meme"]
    chemistry_keywords = ["reaction", "molecule", "bond", "acid", "base", "salt", "oxidation",
                          "reduction", "equilibrium", "catalyst", "electron", "ion", "solution",
                          "compound", "element", "periodic", "organic", "hydrocarbon", "polymer",
                          "electrolysis", "battery", "cell", "ph", "buffer", "titration"]
    biology_keywords = ["cell", "dna", "protein", "enzyme", "mitosis", "meiosis", "photosynthesis",
                         "respiration", "gene", "chromosome", "organism", "evolution", "ecosystem",
                         "bacteria", "virus", "membrane", "tissue", "organ", "blood", "neuron",
                         "hormone", "reproduction", "inheritance", "biomolecule", "plant"]
    maths_keywords = ["equation", "function", "derivative", "integral", "matrix", "determinant",
                      "vector", "probability", "statistics", "geometry", "algebra", "calculus",
                      "trigonometry", "theorem", "proof", "limit", "sequence", "series",
                      "permutation", "combination", "binomial", "logarithm", "complex number",
                      "differential equation", "linear programming", "set theory"]
    physics_keywords = ["motion", "force", "energy", "momentum", "wave", "field", "magnetic",
                        "electric", "gravity", "oscillation", "pendulum", "spring", "fluid",
                        "pressure", "optics", "light", "ray", "lens", "mirror", "current",
                        "voltage", "resistance", "capacitor", "induction", "nuclear", "quantum",
                        "thermodynamic", "heat", "temperature", "doppler", "resonance"]
    history_keywords = ["empire", "king", "war", "battle", "ancient", "dynasty", "civilization",
                        "revolution", "independence", "freedom", "library", "university", "trade"]

    if any(kw in topic_lower for kw in anime_keywords):
        return "Anime & Silly"
    if any(kw in topic_lower for kw in silly_keywords):
        return "Anime & Silly"
    if any(kw in topic_lower for kw in biology_keywords):
        return "NCERT Biology"
    if any(kw in topic_lower for kw in maths_keywords):
        return "NCERT Maths"
    if any(kw in topic_lower for kw in chemistry_keywords):
        return "NCERT Chemistry"
    if any(kw in topic_lower for kw in physics_keywords):
        return "NCERT Physics"
    if any(kw in topic_lower for kw in history_keywords):
        return "History"
    return "Anime & Silly"  # default to viral/silly for maximum reach


def _get_accuracy_note(topic: str) -> str:
    """Get physics accuracy note based on topic keywords."""
    topic_lower = topic.lower()
    for keyword, note in ACCURACY_NOTES.items():
        if keyword in topic_lower:
            return note
    return ("all physical interactions follow real-world physics — gravity, "
            "friction, air resistance, surface tension, and thermodynamics "
            "all behave exactly as in nature")


def _generate_action_description(topic: str, category: str) -> str:
    """Generate a description of what happens in the video."""
    templates = {
        "Physics": f"the principles of {topic} are demonstrated through a clear, visible experiment. "
                   f"Key variables change in real-time, cause and effect are immediately apparent",
        "NCERT Physics": f"the NCERT concept of {topic} is shown exactly as described in the textbook, "
                         f"but brought to life with stunning visual detail that makes the abstract concrete",
        "Chemistry": f"the chemical process of {topic} unfolds step by step. Reactants transform into "
                     f"products with visible color changes, gas evolution, or energy release",
        "NCERT Chemistry": f"the NCERT chemistry topic {topic} is demonstrated with both the macro "
                           f"(what you see) and micro (molecular level) view synchronized",
        "History": f"the historical event of {topic} is recreated with period-accurate detail, "
                   f"dramatic lighting, and cinematic camera work",
        "NCERT Maths": f"the mathematical concept of {topic} is visualized — abstract equations become "
                       f"moving, glowing geometric forms that make the math intuitive and beautiful",
        "Maths": f"the mathematical concept of {topic} is visualized — abstract equations become "
                 f"moving, glowing geometric forms that make the math intuitive and beautiful",
        "NCERT Biology": f"the biological process of {topic} is shown at the molecular level — "
                         f"proteins, DNA, enzymes, and cellular structures rendered in stunning 3D detail",
        "Biology": f"the biological process of {topic} is shown at the molecular level — "
                   f"proteins, DNA, enzymes, and cellular structures rendered in stunning 3D detail",
        "Anime & Silly": f"{topic} is rendered in a fun, visually striking way — with physics consequences, "
                         f"humor, or pure visual satisfaction as the driving force",
    }
    return templates.get(category, f"the concept of {topic} is demonstrated visually")


def _generate_visual_elements(topic: str, category: str) -> str:
    """Generate visual element descriptions."""
    if "Physics" in category:
        return f"velocity vectors, force arrows, energy transfer, and mathematical relationships overlaid on the physical demonstration of {topic}"
    elif "Chemistry" in category:
        return f"molecular structures, bond breaking/forming, electron movement, and color changes during {topic}"
    elif category == "History":
        return f"period-accurate clothing, architecture, tools, and environmental details showing {topic}"
    return f"the key elements of {topic} shown in striking visual detail"


def _extract_principles(topic: str) -> list[str]:
    """Extract relevant physics principles from the topic."""
    topic_lower = topic.lower()
    principles = []

    principle_map = {
        "motion": ["kinematics", "Newton's laws", "velocity", "acceleration"],
        "force": ["Newton's laws", "force balance", "equilibrium"],
        "energy": ["conservation of energy", "work-energy theorem", "kinetic energy", "potential energy"],
        "momentum": ["conservation of momentum", "impulse", "collision dynamics"],
        "wave": ["wave propagation", "frequency", "wavelength", "superposition"],
        "magnetic": ["magnetic field", "Lorentz force", "electromagnetic induction"],
        "electric": ["electric field", "Coulomb's law", "potential difference"],
        "gravit": ["universal gravitation", "orbital mechanics", "free fall"],
        "oscillat": ["simple harmonic motion", "restoring force", "periodicity"],
        "fluid": ["fluid dynamics", "Bernoulli's principle", "pressure"],
        "optics": ["refraction", "reflection", "lens equation", "Snell's law"],
        "heat": ["thermodynamics", "heat transfer", "conduction", "convection"],
        "bond": ["chemical bonding", "electrostatic interaction", "molecular structure"],
        "reaction": ["chemical reaction", "stoichiometry", "conservation of mass"],
        "equilibrium": ["dynamic equilibrium", "Le Chatelier's principle"],
        "electron": ["electron configuration", "quantum mechanics", "energy levels"],
    }

    for keyword, princ in principle_map.items():
        if keyword in topic_lower:
            principles.extend(princ)

    if not principles:
        principles = ["gravity", "conservation of energy", "Newton's laws"]

    return principles[:5]  # limit to 5


def _get_platforms_for_category(category: str) -> list[str]:
    """Get recommended platforms for a category."""
    if "NCERT" in category or category in ("Physics", "Chemistry", "Maths", "Biology"):
        return ["youtube", "facebook", "instagram"]
    if category == "History":
        return ["x", "youtube", "facebook"]
    if category == "Anime & Silly":
        return ["youtube", "x", "instagram"]
    return ["youtube", "facebook", "instagram"]


def _get_platform_reasoning(category: str, topic: str) -> dict:
    """Get platform reasoning for a dynamically generated idea."""
    if "NCERT" in category or category in ("Physics", "Chemistry", "Maths", "Biology"):
        return {
            "youtube": f"NCERT/educational content about {topic} has massive search volume from "
                       f"Indian CBSE + JEE/NEET students. High watch time, good RPM.",
            "facebook": f"Indian student communities on Facebook share {topic} content heavily.",
            "instagram": f"The visual demonstration of {topic} is satisfying and save-worthy.",
            "x": f"Science teachers share {topic} visualizations for classroom use.",
        }
    if category == "History":
        return {
            "x": f"'{topic}' is a conversation starter that drives replies and shares. "
                 f"Perfect for @ChaosAndContext.",
            "youtube": f"Historical content about {topic} gets high watch time.",
            "facebook": f"History content about {topic} resonates with Facebook's Indian audience.",
            "instagram": f"The visual recreation of {topic} is aesthetically striking.",
        }
    if category == "Anime & Silly":
        return {
            "youtube": f"Anime/silly physics content about {topic} has massive viral potential. "
                       f"Crosses entertainment and education audiences. Very high watch time.",
            "x": f"{topic} is a conversation bomb — drives replies, quote tweets, and shares. "
                 f"Anime communities on X are extremely active.",
            "instagram": f"The visual of {topic} is scroll-stopping and highly saveable.",
            "facebook": f"Satisfying/viral content about {topic} is the top shared category on Facebook.",
        }
    return {
        "youtube": f"Educational content about {topic} performs well with good watch time.",
        "facebook": f"Visual content about {topic} gets shares among interested communities.",
        "instagram": f"The visual of {topic} is striking and save-worthy.",
        "x": f"{topic} drives conversation and shares.",
    }
