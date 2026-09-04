"""
Content Idea Generator — the app's "brain" that decides what to create.

Contains a curated library of viral-worthy science, physics, chemistry, nature,
and satisfying phenomenon video ideas, each with:
  - A ready-to-use enhanced prompt optimized for AI video generation
  - The physics/chemistry principles involved (for realism)
  - Recommended platform(s) with reasoning
  - Expected viral potential score
  - Monetization niche classification
  - Series potential (can this become a recurring format?)

Based on 2026 viral content research across Facebook, YouTube Shorts, Instagram Reels, and X.
"""

import random
from utils.viral_scorer import score_viral_potential
from utils.physics_realism import enhance_physics_realism
from utils.platform_recommender import recommend_platforms, PLATFORM_INFO, MONETIZATION_RANK

# ═══ Content Idea Library ═══════════════════════════════════════════

IDEAS = [
    # ─── Physics Phenomena ───────────────────────────────────────
    {
        "id": "phys_prince_rupert",
        "category": "Physics",
        "title": "Prince Rupert's Drop — glass that's indestructible until you snap the tail",
        "description": "A teardrop of molten glass dropped into water creates a shape with "
                       "immense compressive stress. The bulb can withstand a hammer, but "
                       "snapping the tail causes the entire drop to explode.",
        "prompt": "OPENING FRAME: Close-up of a glowing molten glass teardrop being dropped "
                  "into clear water, steam rising. A hardened glass teardrop sits on an anvil. "
                  "A steel hammer strikes the bulb — it bounces off, glass unharmed. "
                  "Then pliers gently squeeze the thin tail — the entire drop explodes "
                  "into shimmering fragments in slow motion. Photorealistic, documentary "
                  "footage style, shallow depth of field, natural lighting, ultra-detailed, "
                  "high production value. Physics accurate: glass shards fly outward from "
                  "the break point following stress release patterns.",
        "physics_principles": ["compressive stress", "tensile stress", "tempered glass",
                               "rapid cooling", "stress waves"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Educational science content has highest RPM. Pairs well with "
                       "long-form explanation. 45% revenue share.",
            "facebook": "The explosion moment is a perfect pattern interrupt. Slow-motion "
                      "satisfying content performs extremely well.",
            "instagram": "Aesthetic visual of glowing glass + dramatic explosion = high "
                         "save and share rate.",
        },
        "viral_score": 85,
        "monetization_niche": "education",
        "series_potential": "High — 'Physics Explained' series with different phenomena each episode",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["physics", "science", "glass", "explosion", "satisfying", "prince ruperts drop"],
    },
    {
        "id": "phys_non_newtonian",
        "category": "Physics",
        "title": "Non-Newtonian Fluid — liquid that becomes solid when you hit it",
        "description": "A cornstarch-water mixture that flows like liquid when poured but "
                       "turns solid when struck. A ball dropped onto the surface bounces, "
                       "but if you slowly push your hand in, it sinks.",
        "prompt": "OPENING FRAME: A hand slams onto a tray of white fluid — the hand bounces "
                  "off as if hitting concrete, fluid doesn't splash. Then the same hand "
                  "slowly pushes into the fluid and sinks like quicksand. A ball is dropped "
                  "from above — it bounces high. A slow-motion shot of a fist punching the "
                  "surface, the fluid solidifies instantly, cracks form like concrete. "
                  "Photorealistic, macro close-up, natural lighting, documentary footage "
                  "style, ultra-detailed. Physics accurate: shear thickening behavior, "
                  "impact creates solid surface, slow force allows flow.",
        "physics_principles": ["shear thickening", "non-Newtonian fluid dynamics",
                               "viscosity", "impact force", "pressure waves"],
        "best_platforms": ["facebook", "instagram", "youtube"],
        "platform_reasoning": {
            "facebook": "Hands-on experiment format gets highest engagement on Facebook. "
                      "The liquid-to-solid transition is a perfect 3-second hook.",
            "instagram": "Visually mesmerizing + satisfying = high save rate. "
                         "Clean aesthetic content.",
            "youtube": "Educational science with clear explanation potential. "
                       "Good RPM in education niche.",
        },
        "viral_score": 88,
        "monetization_niche": "education",
        "series_potential": "High — 'Weird Physics' series exploring counterintuitive phenomena",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["physics", "science", "fluid", "non-newtonian", "satisfying", "experiment"],
    },
    {
        "id": "phys_chladni",
        "category": "Physics",
        "title": "Chladni Plate — sand forms beautiful patterns from sound waves",
        "description": "Sand on a metal plate forms intricate, symmetric patterns when "
                       "a violin bow is drawn across the edge. Different frequencies "
                       "create completely different geometric patterns.",
        "prompt": "OPENING FRAME: White sand scattered on a black metal plate. A violin bow "
                  "draws across the edge — sand instantly jumps and rearranges into a perfect "
                  "symmetric star pattern. The frequency changes — sand shifts into a new "
                  "geometric mandala. Close-up macro shot of individual sand grains bouncing "
                  "and settling into nodes. Photorealistic, top-down camera, studio lighting, "
                  "ultra-detailed, documentary footage. Physics accurate: standing waves "
                  "create nodal lines where sand settles, antinodes displace sand.",
        "physics_principles": ["standing waves", "resonance", "nodal lines",
                               "frequency", "vibration modes"],
        "best_platforms": ["instagram", "facebook", "youtube"],
        "platform_reasoning": {
            "instagram": "Geometric patterns are highly aesthetic and save-worthy. "
                         "Visually stunning content performs best on Instagram.",
            "facebook": "The moment sand jumps into patterns is a visual hook. "
                      "Satisfying content category.",
            "youtube": "Strong educational component. Good for science channel.",
        },
        "viral_score": 82,
        "monetization_niche": "education",
        "series_potential": "High — 'Sound Creates Shape' series with increasing complexity",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["physics", "sound", "waves", "patterns", "satisfying", "cymatics", "science"],
    },
    {
        "id": "phys_aurora",
        "category": "Nature",
        "title": "Northern Lights — how solar wind creates dancing light in the sky",
        "description": "Charged particles from the sun collide with Earth's atmosphere, "
                       "creating rippling curtains of green, purple, and red light across "
                       "the polar sky.",
        "prompt": "OPENING FRAME: A dark Arctic landscape with snow-covered mountains. "
                  "Suddenly, a massive curtain of green light begins rippling across the "
                  "entire sky, shifting to purple and red at the edges. The light dances "
                  "and pulses in waves. A lone figure stands silhouetted against the glow, "
                  "breath visible in the cold. Drone shot ascending above the mountains. "
                  "Photorealistic, cinematic, volumetric lighting, ultra-detailed, 8K, "
                  "natural lighting. Physics accurate: aurora colors correspond to "
                  "atmospheric altitude — green at 100km (oxygen), red at 200km+ (oxygen), "
                  "purple at 90km (nitrogen). Light curtains move with magnetic field lines.",
        "physics_principles": ["electromagnetic interaction", "solar wind",
                               "atmospheric excitation", "magnetic field lines",
                               "photon emission"],
        "best_platforms": ["youtube", "instagram", "x"],
        "platform_reasoning": {
            "youtube": "Nature/science content with cinematic visuals performs well. "
                       "Long-form documentary style earns well.",
            "instagram": "Breathtaking visual = maximum shares and saves. "
                         "Aesthetic nature content is a top category.",
            "x": "Conversation-starting: 'How does this actually work?' drives replies "
                 "and quote tweets. Great for science engagement.",
        },
        "viral_score": 80,
        "monetization_niche": "nature",
        "series_potential": "High — 'Nature's Spectacles' series: aurora, bioluminescence, "
                            "volcanic lightning, blood falls, etc.",
        "estimated_rpm": 0.04,
        "trending": True,
        "tags": ["nature", "aurora", "northern lights", "science", "cinematic", "space weather"],
    },

    # ─── Chemistry Phenomena ─────────────────────────────────────
    {
        "id": "chem_elephant_toothpaste",
        "category": "Chemistry",
        "title": "Elephant Toothpaste — a foam eruption that fills an entire pool",
        "description": "Hydrogen peroxide decomposes rapidly with a catalyst, releasing "
                       "oxygen that gets trapped in soap bubbles, creating a massive "
                       "foam eruption. Scaled up, it fills a swimming pool.",
        "prompt": "OPENING FRAME: A massive concrete swimming pool. A large container is "
                  "poured in — instantly, colorful foam explodes upward in a massive column, "
                  "expanding outward, filling the pool in seconds. The foam cascades over "
                  "the edges in slow motion. Individual bubbles pop and reform. Warm steam "
                  "rises from the reaction. Photorealistic, wide-angle shot, natural daylight, "
                  "ultra-detailed, documentary footage style. Chemistry accurate: exothermic "
                  "decomposition of H2O2 catalyzed by potassium iodide, oxygen gas trapped "
                  "in soap film creates rapid foam expansion.",
        "physics_principles": ["catalytic decomposition", "exothermic reaction",
                               "gas evolution", "surface tension", "thermal expansion"],
        "best_platforms": ["facebook", "youtube", "instagram"],
        "platform_reasoning": {
            "facebook": "Scale + speed of the eruption = perfect viral hook. "
                      "Experiment videos dominate Facebook science.",
            "youtube": "Mark Rober style content. High watch time, high RPM. "
                       "Educational + entertainment.",
            "instagram": "Colorful foam is visually striking. High share potential.",
        },
        "viral_score": 90,
        "monetization_niche": "education",
        "series_potential": "High — 'Giant Science' series scaling up classic experiments",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["chemistry", "science", "experiment", "foam", "satisfying", "elephant toothpaste"],
    },
    {
        "id": "chem_glow_stick",
        "category": "Chemistry",
        "title": "Brightest Chemiluminescence — a reaction that produces blinding light",
        "description": "Dinitrophenyl oxalate + hydrogen peroxide + fluorescent dye creates "
                       "the brightest chemical glow reaction known — brighter than the sun "
                       "on a surface, used in commercial glow sticks.",
        "prompt": "OPENING FRAME: Complete darkness. A clear liquid is poured into a flask "
                  "containing a yellow solution — instantly, blinding yellow-green light "
                  "erupts, illuminating the entire laboratory. The glow is so bright it casts "
                  "sharp shadows. Slowly the glow fades over 30 seconds. Comparison shot: "
                  "a luminol reaction is barely visible next to it. Photorealistic, "
                  "extreme close-up, dark laboratory setting, the only light is from the "
                  "reaction itself. Chemistry accurate: peroxyoxalate chemiluminescence, "
                  "energy transfer to fluorescent dye, photon emission at dye's wavelength.",
        "physics_principles": ["chemiluminescence", "energy transfer", "photon emission",
                               "electron excitation", "fluorescence"],
        "best_platforms": ["facebook", "instagram", "youtube"],
        "platform_reasoning": {
            "facebook": "Darkness-to-blinding-light is the ultimate pattern interrupt. "
                      "Satisfying + surprising = maximum replay.",
            "instagram": "The visual of a glowing flask in darkness is extremely aesthetic. "
                         "High save rate.",
            "youtube": "Chemistry education content. Can explain the reaction mechanism "
                       "in long-form.",
        },
        "viral_score": 87,
        "monetization_niche": "education",
        "series_potential": "Medium — 'Chemistry That Glows' series with different "
                            "chemiluminescent reactions",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["chemistry", "science", "glow", "chemiluminescence", "experiment", "satisfying"],
    },
    {
        "id": "chem_bismuth",
        "category": "Chemistry",
        "title": "Bismuth Crystals — metal that grows into impossible rainbow staircases",
        "description": "When molten bismuth cools, it forms geometric hopper crystals "
                       "with an iridescent oxide layer that creates rainbow colors. "
                       "The staircase-like structures look alien.",
        "prompt": "OPENING FRAME: A crucible of molten silver metal. As it cools, geometric "
                  "staircase crystals begin rising from the surface, growing upward in "
                  "impossible geometric patterns. The surface oxidizes into shimmering "
                  "rainbow colors — gold, blue, purple, pink. Close-up macro shot of "
                  "crystals growing in real-time. Photorealistic, extreme close-up, "
                  "studio lighting with dark background to highlight colors, ultra-detailed. "
                  "Chemistry accurate: hopper crystal growth pattern, bismuth oxide layer "
                  "creates thin-film interference colors.",
        "physics_principles": ["crystal growth", "hopper crystal formation",
                               "thin-film interference", "oxidation", "melting point"],
        "best_platforms": ["instagram", "facebook", "youtube"],
        "platform_reasoning": {
            "instagram": "Rainbow geometric crystals = peak aesthetic content. "
                         "Extremely high save/share rate.",
            "facebook": "The growth process is mesmerizing. Satisfying + surprising.",
            "youtube": "Can explain the science behind the colors and crystal structure.",
        },
        "viral_score": 84,
        "monetization_niche": "education",
        "series_potential": "High — 'Metals That Do Weird Things' series",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["chemistry", "science", "crystals", "bismuth", "rainbow", "satisfying"],
    },

    # ─── Nature Phenomena ────────────────────────────────────────
    {
        "id": "nature_bioluminescence",
        "category": "Nature",
        "title": "Bioluminescent Waves — ocean that glows neon blue at night",
        "description": "Dinoflagellates in coastal waters emit blue light when disturbed. "
                       "Breaking waves, footsteps in wet sand, and moving hands all "
                       "trigger a glowing blue trail.",
        "prompt": "OPENING FRAME: A dark beach at night. A wave crashes — and the breaking "
                  "water glows intense electric blue. A person walks along the wet sand, "
                  "each footprint leaves a glowing blue trail. A hand swiped through a "
                  "tidepool creates a burst of blue light. Drone shot rising to show the "
                  "entire coastline glowing with each wave. Photorealistic, cinematic, "
                  "the only light is the bioluminescence, natural darkness, ultra-detailed. "
                  "Physics accurate: bioluminescent dinoflagellates emit blue light (470nm) "
                  "via luciferin-luciferase reaction triggered by mechanical disturbance.",
        "physics_principles": ["bioluminescence", "luciferin-luciferase reaction",
                               "mechanical stimulation", "photon emission", "blue light spectrum"],
        "best_platforms": ["instagram", "youtube", "facebook"],
        "platform_reasoning": {
            "instagram": "Glowing ocean waves are peak aesthetic nature content. "
                         "One of the most saved categories on Instagram.",
            "youtube": "Cinematic nature documentary style. High watch time, good RPM.",
            "facebook": "The glowing footprint trail is a satisfying visual hook.",
        },
        "viral_score": 86,
        "monetization_niche": "nature",
        "series_potential": "High — 'Nature Glows' series: bioluminescence, foxfire, "
                            "glow worms, firefly squid",
        "estimated_rpm": 0.04,
        "trending": True,
        "tags": ["nature", "bioluminescence", "ocean", "science", "glowing", "cinematic"],
    },
    {
        "id": "nature_lightning_volcano",
        "category": "Nature",
        "title": "Volcanic Lightning — when a volcano creates its own lightning storm",
        "description": "During a volcanic eruption, ash particles rub together creating "
                       "static charge, producing dramatic lightning bolts inside the "
                       "ash cloud. A phenomenon called 'dirty thunderstorms.'",
        "prompt": "OPENING FRAME: A massive volcanic eruption at night. Red-hot lava fountains "
                  "shoot upward. Inside the billowing ash cloud, jagged lightning bolts "
                  "crack across the sky — the volcano is generating its own electrical storm. "
                  "Bolts flash in multiple forks simultaneously. Lava flows down the slope "
                  "in rivers of orange. Photorealistic, wide cinematic shot, telephoto lens, "
                  "natural lighting from the eruption, ultra-detailed, 8K. Physics accurate: "
                  "triboelectric charging from ash particle collisions, charge separation "
                  "in plume, electrical discharge follows charge gradient.",
        "physics_principles": ["triboelectric charging", "charge separation",
                               "electrical discharge", "plume dynamics", "static electricity"],
        "best_platforms": ["youtube", "x", "instagram"],
        "platform_reasoning": {
            "youtube": "Dramatic nature documentary content. Epic scale = high watch time.",
            "x": "Conversation-starting: 'A volcano making its own lightning?!' "
                 "drives massive engagement and shares.",
            "instagram": "The visual is stunning and shareable. Dramatic nature content "
                         "performs well.",
        },
        "viral_score": 83,
        "monetization_niche": "nature",
        "series_potential": "High — 'Nature's Extremes' series: volcanic lightning, "
                            "blood falls, surreal springs",
        "estimated_rpm": 0.04,
        "trending": True,
        "tags": ["nature", "volcano", "lightning", "science", "dramatic", "cinematic"],
    },
    {
        "id": "nature_frost_flower",
        "category": "Nature",
        "title": "Frost Flowers — delicate ice ribbons that grow on frozen plants",
        "description": "When sap freezes and expands in certain plants, it extrudes "
                       "through cracks in the stem, forming impossibly thin, curling "
                       "ribbons of ice that look like glass flowers.",
        "prompt": "OPENING FRAME: A frozen meadow at dawn. On a dead plant stem, a delicate "
                  "ribbon of ice is slowly curling outward, forming a spiral shape like "
                  "shattered glass. More ice ribbons emerge, creating flower-like patterns. "
                  "Macro close-up of ice crystals forming in real-time, frost sparkling "
                  "in golden morning light. Photorealistic, extreme macro, shallow depth "
                  "of field, golden hour lighting, ultra-detailed. Physics accurate: "
                  "capillary action draws liquid water through cracks, freezing at contact "
                  "with air extrudes ice ribbons, ice flower growth follows supercooling "
                  "and nucleation patterns.",
        "physics_principles": ["capillary action", "freezing point depression",
                               "ice nucleation", "supercooling", "crystallization"],
        "best_platforms": ["instagram", "youtube", "facebook"],
        "platform_reasoning": {
            "instagram": "Delicate, beautiful, aesthetic = peak Instagram nature content.",
            "youtube": "Educational nature documentary. Good for science channel.",
            "facebook": "The time-lapse growth is satisfying. Good niche content.",
        },
        "viral_score": 78,
        "monetization_niche": "nature",
        "series_potential": "High — 'Hidden Wonders' series exploring small natural phenomena",
        "estimated_rpm": 0.04,
        "trending": False,
        "tags": ["nature", "ice", "frost", "science", "beautiful", "macro"],
    },

    # ─── AI ASMR / Satisfying ────────────────────────────────────
    {
        "id": "asmr_glass_fruit",
        "category": "Satisfying",
        "title": "Glass Fruit Cutting — slicing impossible crystal fruit in slow motion",
        "description": "A knife slices through fruit rendered as translucent glass. "
                       "Each cut produces a satisfying crystalline crack. The interior "
                       "reveals impossibly beautiful patterns. One of 2026's biggest "
                       "viral formats with billions of views.",
        "prompt": "OPENING FRAME: A translucent blue glass orange sits on a marble slab. "
                  "A chef's knife descends in slow motion and slices through it — a crisp, "
                  "crystalline crack. The two halves fall apart revealing a stunning "
                  "geometric interior pattern. Light refracts through the glass, casting "
                  "rainbow shadows. Another cut — a glass strawberry, red light glowing "
                  "through. Extreme close-up, warm backlight, macro lens, shallow depth "
                  "of field, ultra-detailed, 8K, no music. Physics accurate: glass fracture "
                  "follows cleavage planes, refractive index creates caustic light patterns, "
                  "shard distribution follows stress propagation.",
        "physics_principles": ["glass fracture mechanics", "cleavage planes",
                               "light refraction", "caustics", "stress propagation"],
        "best_platforms": ["facebook", "instagram", "youtube"],
        "platform_reasoning": {
            "facebook": "#1 format for AI ASMR. Billions of views. The crack sound + visual "
                      "= perfect loop content. Highest completion rate format.",
            "instagram": "Aesthetic, satisfying, highly saveable. Visual quality matters most here.",
            "youtube": "ASMR channels are among fastest-growing. Good watch time. "
                       "Can build a dedicated ASMR channel.",
        },
        "viral_score": 92,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Glass Kitchen' series with different foods, "
                            "themes, and colors. Already proven format with massive demand.",
        "estimated_rpm": 0.03,
        "trending": True,
        "tags": ["asmr", "satisfying", "glass", "fruit", "satisfying", "ai", "oddlysatisfying"],
    },
    {
        "id": "asmr_ferrofluid",
        "category": "Satisfying",
        "title": "Ferrofluid — black liquid that comes alive near magnets",
        "description": "A black oil-based fluid containing magnetic nanoparticles. "
                       "When a magnet approaches, the liquid forms spiky peaks and "
                       "structures that move and morph as the magnet moves. Looks alien.",
        "prompt": "OPENING FRAME: A pool of black mirror-like liquid sits in a glass dish. "
                  "A magnet is brought close from below — instantly, the liquid erupts into "
                  "a forest of sharp spiky peaks, each perfectly symmetric. The magnet moves "
                  "and the spikes dance and morph. The peaks grow taller, then collapse as "
                  "the magnet pulls away. Extreme macro close-up, studio lighting, dark "
                  "background, reflective surface. Photorealistic, ultra-detailed, 8K. "
                  "Physics accurate: ferrofluid follows magnetic field lines, spike spacing "
                  "follows Rosensweig instability, surface tension vs magnetic force "
                  "determines peak height.",
        "physics_principles": ["magnetic field interaction", "Rosensweig instability",
                               "surface tension", "ferromagnetism", "nanoparticle dynamics"],
        "best_platforms": ["facebook", "instagram", "youtube"],
        "platform_reasoning": {
            "facebook": "The liquid 'coming alive' is a perfect pattern interrupt. "
                      "Satisfying + alien = high replay rate.",
            "instagram": "The black spikes are visually striking and aesthetic. "
                         "High save rate for satisfying content.",
            "youtube": "Can explain the physics. Growing niche with limited competition.",
        },
        "viral_score": 85,
        "monetization_niche": "education",
        "series_potential": "Medium — 'Magnetic Phenomena' series",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["asmr", "satisfying", "ferrofluid", "magnetic", "science", "mesmerizing"],
    },
    {
        "id": "asmr_kinetic_sand",
        "category": "Satisfying",
        "title": "Kinetic Sand Cutting — oversized blade slices through colored sand",
        "description": "A giant block of colored kinetic sand is sliced by an oversized "
                       "blade. The cut is perfectly clean. The sand holds its shape, "
                       "then slowly flows. One of the most durable ASMR trends.",
        "prompt": "OPENING FRAME: A large rectangular block of vibrant purple kinetic sand "
                  "sits on a clean white surface. An oversized metal blade descends and "
                  "slices through it — the cut is perfectly clean, sand holds its shape "
                  "like a solid. The two halves separate, then slowly the cut edge begins "
                  "to flow and soften. Another slice — this time orange sand, then teal. "
                  "Extreme close-up, soft studio lighting, shallow depth of field, "
                  "ultra-detailed, 8K, no music. Physics accurate: kinetic sand exhibits "
                  "non-Newtonian behavior — solid under pressure, flows under gravity.",
        "physics_principles": ["non-Newtonian behavior", "cohesive forces",
                               "viscosity under pressure", "granular physics"],
        "best_platforms": ["facebook", "instagram", "youtube"],
        "platform_reasoning": {
            "facebook": "One of the most proven ASMR formats. Clean cut + slow flow = "
                      "perfect loop. Daily posting builds dedicated audience.",
            "instagram": "Vibrant colors + satisfying motion = high save rate.",
            "youtube": "ASMR channel content. Consistent views with daily posting.",
        },
        "viral_score": 80,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Sand Kitchen' series with color themes, "
                            "shapes, and cutting patterns",
        "estimated_rpm": 0.03,
        "trending": True,
        "tags": ["asmr", "satisfying", "kinetic sand", "cutting", "oddlysatisfying"],
    },

    # ─── Geography / Scale ───────────────────────────────────────
    {
        "id": "geo_mariana_trench",
        "category": "Geography",
        "title": "Descent into the Mariana Trench — the deepest point on Earth",
        "description": "A continuous descent from the ocean surface to the bottom of "
                       "the Mariana Trench (11km deep). Light fades, creatures become "
                       "stranger, pressure increases. The bottom is pitch black with "
                       "alien life forms.",
        "prompt": "OPENING FRAME: Camera at the ocean surface, sunlight sparkling on blue "
                  "water. The camera begins descending. At 200m, the blue deepens. "
                  "At 1000m, the first bioluminescent creatures appear. At 4000m, a "
                  "sperm whale passes in the darkness. At 8000m, strange translucent fish "
                  "with glowing lures. At 11000m — the seafloor, alien-like, a single "
                  "snailfish swims past. Pitch black except for bioluminescence. "
                  "Photorealistic, continuous descent, cinematic, natural lighting "
                  "transitioning from sunlight to bioluminescence. Physics accurate: "
                  "light attenuation follows Beer-Lambert law, pressure increases 1 atm "
                  "per 10m, deep-sea creatures follow real bathypelagic adaptations.",
        "physics_principles": ["light attenuation", "hydrostatic pressure",
                               "Beer-Lambert law", "bioluminescence", "deep-sea biology"],
        "best_platforms": ["youtube", "instagram", "x"],
        "platform_reasoning": {
            "youtube": "Long-form descent content = high watch time. Educational + "
                       "visually stunning. Good RPM in education/nature.",
            "instagram": "Can be split into a carousel of depth zones. Aesthetic visuals.",
            "x": "'How deep is the ocean really?' is a proven conversation starter.",
        },
        "viral_score": 81,
        "monetization_niche": "education",
        "series_potential": "High — 'Journey to Extremes' series: deepest ocean, "
                            "tallest mountain, hottest volcano, coldest place",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["geography", "ocean", "science", "nature", "deep sea", "cinematic"],
    },
    {
        "id": "geo_scale_universe",
        "category": "Geography",
        "title": "Scale of the Universe — from atom to galaxy in one continuous zoom",
        "description": "Starting at the size of a single atom, the camera continuously "
                       "zooms out — molecule, cell, insect, human, building, city, "
                       "country, planet, star, galaxy, universe. Mind-bending scale.",
        "prompt": "OPENING FRAME: Extreme close-up of a single carbon atom, electrons "
                  "orbiting. Camera zooms out — DNA helix, a human cell, a grain of rice, "
                  "a hand, a person standing in a field, a city from above, a country from "
                  "space, Earth, the Moon orbiting, the Sun, the solar system, the Milky Way "
                  "galaxy, galaxy clusters, the cosmic web. Continuous smooth zoom, "
                  "photorealistic at each scale, cinematic, natural transitions between "
                  "scales. Physics accurate: relative sizes are accurate, orbital mechanics "
                  "correct, galactic structure follows real astronomy data.",
        "physics_principles": ["scale invariance", "atomic structure",
                               "orbital mechanics", "galactic structure",
                               "cosmic web topology"],
        "best_platforms": ["youtube", "facebook", "x"],
        "platform_reasoning": {
            "youtube": "Perfect for long-form. High retention — viewers want to see the "
                       "full zoom. Educational content, good RPM.",
            "facebook": "The continuous zoom is a great hook. Split into parts for a series.",
            "x": "'You are here' perspective drives shares and philosophical discussions.",
        },
        "viral_score": 82,
        "monetization_niche": "education",
        "series_potential": "High — 'Scale' series: zoom into the atom, zoom out to galaxy, "
                            "compare sizes of things",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["science", "space", "scale", "universe", "education", "mindblowing"],
    },

    # ─── Engineering / How Things Work ───────────────────────────
    {
        "id": "eng_engine_explode",
        "category": "Engineering",
        "title": "How an Engine Works — cutaway of a V8 engine in motion",
        "description": "An exploded/animated cutaway view of a V8 engine showing "
                       "every cylinder firing, pistons moving, valves opening and closing, "
                       "fuel injecting, and exhaust flowing. The mechanical choreography "
                       "is mesmerizing.",
        "prompt": "OPENING FRAME: A V8 engine rendered in cross-section, every internal "
                  "part visible. The engine starts — pistons pump in sequence, intake "
                  "valves open, fuel sprays, spark plugs fire, combustion flashes, "
                  "exhaust valves open, gases flow out. The timing belt spins, the "
                  "crankshaft turns. Slow-motion close-up of a single cylinder's four "
                  "strokes. Photorealistic, metallic surfaces, studio lighting, ultra-detailed. "
                  "Physics accurate: 4-stroke cycle (intake, compression, power, exhaust) "
                  "with correct valve timing, combustion physics, thermodynamic efficiency.",
        "physics_principles": ["thermodynamics", "combustion", "mechanical engineering",
                               "4-stroke cycle", "energy conversion"],
        "best_platforms": ["youtube", "x", "facebook"],
        "platform_reasoning": {
            "youtube": "Engineering explained content has loyal audience. High watch time, "
                       "good RPM in tech/education.",
            "x": "Engineering visuals drive conversation among tech/automotive communities.",
            "facebook": "The synchronized mechanical motion is visually satisfying.",
        },
        "viral_score": 75,
        "monetization_niche": "tech",
        "series_potential": "High — 'How Things Work' series: engine, turbine, transmission, "
                            "rocket, lock mechanism",
        "estimated_rpm": 0.10,
        "trending": False,
        "tags": ["engineering", "science", "engine", "how things work", "satisfying"],
    },

    # ─── History & Science Storytelling ─────────────────────────
    {
        "id": "hist_zheng_he_fleet",
        "category": "History",
        "title": "Zheng He's Treasure Fleet — the largest navy the world had ever seen",
        "description": "In the early 1400s, China launched massive treasure ships under Admiral Zheng He, "
                       "sailing as far as Africa. These ships dwarfed European vessels of the era. "
                       "A visualization of this forgotten superpower of the seas.",
        "prompt": "OPENING FRAME: Aerial drone shot of a massive 15th-century Chinese harbor at dawn. "
                  "Dozens of enormous wooden treasure ships, each the size of a football field, sail out "
                  "in formation. Red silk sails catch the wind. The camera sweeps over the fleet showing "
                  "the scale — tiny human figures on deck, cannons, cargo holds. The ships cut through "
                  "ocean waves powerfully. Photorealistic, cinematic, golden hour lighting, volumetric "
                  "atmospheric haze, ultra-detailed, 8K, documentary footage style. Physics accurate: "
                  "ships displace water realistically, sails fill with wind following aerodynamic "
                  "principles, wooden hulls flex with wave motion, wake patterns follow fluid dynamics.",
        "physics_principles": ["fluid dynamics", "buoyancy", "aerodynamics",
                               "wave mechanics", "structural mechanics"],
        "best_platforms": ["x", "youtube", "facebook"],
        "platform_reasoning": {
            "x": "Conversation-starting: 'Why don't we learn about this in school?' drives massive "
                 "replies, quote tweets, and shares. Perfect for @ChaosAndContext's audience.",
            "youtube": "Cinematic history content gets high watch time. Educational niche has good RPM. "
                       "Can expand into long-form documentary.",
            "facebook": "Historical visual content performs well on Facebook. Broad audience appeal.",
            "instagram": "The visual of massive ships at dawn is highly aesthetic and save-worthy.",
        },
        "viral_score": 84,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Forgotten Superpowers' series: Zheng He's fleet, "
                            "Library of Alexandria, Mongol postal system, Indus Valley civilization",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["history", "science", "zheng he", "china", "naval", "cinematic", "chaosandcontext"],
    },
    {
        "id": "hist_butterfly_effect",
        "category": "History",
        "title": "The Butterfly Effect — how one small change creates chaos",
        "description": "Edward Lorenz discovered that tiny differences in initial conditions "
                       "produce wildly different outcomes. A butterfly flaps its wings in Brazil, "
                       "and weeks later a tornado hits Texas. The science of chaos theory, "
                       "made visible.",
        "prompt": "OPENING FRAME: Extreme macro close-up of a butterfly perched on a leaf in a dense "
                  "Brazilian rainforest. It flaps its wings once — a visible ripple of air distorts "
                  "the surrounding leaves. The camera follows the air ripple expanding outward, "
                  "across the forest canopy, over mountains, into cloud formations that build and "
                  "darken. The ripple cascades through weather systems. Final shot: a dramatic "
                  "tornado forming on a Texas plain. Photorealistic, cinematic, seamless camera "
                  "movement, natural lighting transitioning from tropical to storm. Physics accurate: "
                  "air pressure waves propagate at correct speed, butterfly wing vortices follow "
                  "fluid dynamics, cloud formation follows atmospheric thermodynamics, tornado "
                  "follows Coriolis effect and pressure differentials.",
        "physics_principles": ["fluid dynamics", "chaos theory", "atmospheric thermodynamics",
                               "pressure waves", "Coriolis effect", "turbulence"],
        "best_platforms": ["x", "youtube", "instagram"],
        "platform_reasoning": {
            "x": "'A butterfly caused a tornado' is the ultimate conversation starter. Drives "
                 "replies, debates, and shares. Perfect match for @ChaosAndContext's science niche.",
            "youtube": "Science explained visually = high watch time and good RPM in education niche.",
            "instagram": "The butterfly-to-tornado visual journey is visually stunning and save-worthy.",
            "facebook": "Science content with dramatic visuals performs well on Facebook Reels.",
        },
        "viral_score": 87,
        "monetization_niche": "education",
        "series_potential": "High — 'Science That Changed Everything' series: butterfly effect, "
                            "relativity, quantum entanglement, DNA discovery",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["science", "chaos theory", "butterfly effect", "physics", "chaosandcontext"],
    },
    {
        "id": "hist_nalanda_library",
        "category": "History",
        "title": "Nalanda University — the world's first great library, burning",
        "description": "In the 5th century CE, Nalanda housed 10,000 students and a nine-story library. "
                       "When invaders burned it, the library burned for months. A visualization of "
                       "knowledge lost to fire.",
        "prompt": "OPENING FRAME: A sprawling ancient Indian university campus at its peak. Red brick "
                  "buildings, courtyards filled with scholars in robes debating, a towering nine-story "
                  "library structure. The camera slowly rises on a drone shot revealing the massive scale. "
                  "Then transition: flames catch on the library's wooden upper floors. Smoke billows. "
                  "Burning manuscripts fall like fiery snow. Scholars flee. The library collapses inward. "
                  "Photorealistic, cinematic, dramatic lighting from fire, volumetric smoke, ultra-detailed. "
                  "Physics accurate: fire spreads following combustion dynamics, smoke rises with "
                  "convection currents, structural collapse follows gravity and material failure, "
                  "burning paper follows accurate trajectory.",
        "physics_principles": ["combustion", "convection currents", "structural collapse",
                               "gravity", "material failure", "thermal radiation"],
        "best_platforms": ["x", "youtube", "facebook"],
        "platform_reasoning": {
            "x": "'The library that burned for months' is emotionally powerful. Drives replies about "
                 "lost knowledge, what could have been. Perfect for @ChaosAndContext's history niche.",
            "youtube": "Historical documentary content with dramatic visuals = high watch time. "
                       "Education niche RPM is good.",
            "facebook": "Indian historical content resonates strongly with Facebook's large Indian audience.",
            "instagram": "The burning library visual is dramatic and highly shareable.",
        },
        "viral_score": 82,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Lost Knowledge' series: Library of Alexandria, Nalanda, "
                            "House of Wisdom Baghdad, Mayan codices",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["history", "nalanda", "india", "education", "lost knowledge", "chaosandcontext"],
    },
    {
        "id": "hist_madhava_infinity",
        "category": "History",
        "title": "Madhava discovered infinity 200 years before Newton",
        "description": "In 14th-century Kerala, Madhava of Sangamagrama devised infinite series for pi, "
                       "sine, and cosine — discoveries Europe attributed to Newton and Leibniz centuries "
                       "later. A visualization of infinity being tamed.",
        "prompt": "OPENING FRAME: A palm-leaf manuscript in dim lamplight, Sanskrit symbols glowing. "
                  "The camera zooms into the ink — the symbols transform into flowing geometric patterns. "
                  "A circle appears, and infinite polygons spiral inward, their edges approaching the "
                  "circle's curve. Numbers cascade like water. The series converges: 3, 3.1, 3.14, "
                  "3.1415... The screen fills with mathematical beauty. Then pull back: a scholar in "
                  "14th-century Kerala working by oil lamp, ocean visible through the window. "
                  "Photorealistic, cinematic, macro to wide transition. Physics accurate: geometric "
                  "convergence follows mathematical accuracy, light refraction through oil lamp flame, "
                  "palm leaf texture and ink behavior are physically accurate.",
        "physics_principles": ["light refraction", "geometric convergence", "optics",
                               "fluid dynamics of ink", "thermal radiation"],
        "best_platforms": ["x", "youtube", "instagram"],
        "platform_reasoning": {
            "x": "'An Indian mathematician beat Newton by 200 years' is a proven viral format on X. "
                 "Drives debate, national pride, and shares. Perfect for @ChaosAndContext.",
            "youtube": "Math history content has a dedicated audience. High watch time, good RPM.",
            "instagram": "The geometric visualization of infinity is visually mesmerizing and aesthetic.",
            "facebook": "Indian achievement content performs very well on Facebook in India.",
        },
        "viral_score": 83,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Hidden Pioneers' series: Madhava, Aryabhata, Brahmagupta, "
                            "Pāṇini, Charaka, Sushruta",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["history", "mathematics", "madhava", "kerala", "india", "infinity", "chaosandcontext"],
    },
    {
        "id": "hist_panini_grammar",
        "category": "History",
        "title": "Pāṇini wrote 4,000 rules that captured an entire language's logic",
        "description": "In ancient India, Pāṇini created the Aṣṭādhyāyī — 4,000 rules that "
                       "generated correct Sanskrit grammar algorithmically. His system was so precise "
                       "that modern linguists compare it to computer code. He essentially invented "
                       "the concept of a formal grammar, 2,500 years before computers existed.",
        "prompt": "OPENING FRAME: Ancient palm-leaf manuscripts arranged in a grid pattern, Sanskrit "
                  "script flowing across them. The rules begin glowing — each rule lights up in sequence, "
                  "connecting to other rules like a circuit board. The 4,000 rules form a vast "
                  "interconnected network, pulsing with light, resembling a neural network or "
                  "computer algorithm. The camera pulls back to reveal the full structure: a "
                  "knowledge graph of language itself. Transition: a scholar seated under a banyan "
                  "tree, writing methodically. Photorealistic, cinematic, warm golden light, "
                  "ultra-detailed. Physics accurate: ink flows on palm leaf following surface tension, "
                  "light behaves with correct ambient occlusion, material properties of palm leaf "
                  "and ink are accurate.",
        "physics_principles": ["surface tension", "ink flow dynamics", "optics",
                               "material properties", "light scattering"],
        "best_platforms": ["x", "youtube"],
        "platform_reasoning": {
            "x": "'Pāṇini invented the algorithm 2,500 years before computers' is a conversation "
                 "bomb on X. Drives replies from linguists, computer scientists, and history buffs. "
                 "Perfect @ChaosAndContext content.",
            "youtube": "Deep educational content for a dedicated audience. Good watch time and RPM.",
            "facebook": "Indian intellectual history resonates with Facebook's Indian audience.",
            "instagram": "The glowing rule-network visual is aesthetically striking.",
        },
        "viral_score": 79,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Geniuses Erased by History' series: Pāṇini, Hypatia, "
                            "al-Khwarizmi, Ada Lovelace, Srinivasa Ramanujan",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["history", "linguistics", "panini", "sanskrit", "india", "algorithm", "chaosandcontext"],
    },
    {
        "id": "hist_samudragupta_empire",
        "category": "History",
        "title": "Samudragupta — the king who built India's classical age",
        "description": "From his capital Pataliputra, Samudragupta (335-375 CE) unified northern India "
                       "and extended Gupta influence deep into the south. He wasn't just a conqueror — "
                       "he was a poet, musician, and patron of arts who crafted India's golden age.",
        "prompt": "OPENING FRAME: A grand ancient Indian palace at golden hour. A king in regal Gupta-era "
                  "attire sits on a throne, playing the veena. The camera pulls back through towering "
                  "pillars to reveal a vast empire stretching to the horizon — cities, temples, "
                  "trade routes, ships on the Ganges. Armies march in formation. Scholars debate in "
                  "courtyards. The camera sweeps across the golden landscape of the Gupta Empire at "
                  "its zenith. Photorealistic, cinematic, epic scale, golden hour lighting, aerial "
                  "drone style. Physics accurate: fabric drapes with correct gravity and wind interaction, "
                  "march formations follow crowd dynamics, water flow in the Ganges follows fluid "
                  "mechanics, architectural structures follow load-bearing physics.",
        "physics_principles": ["gravity", "fluid dynamics", "structural mechanics",
                               "aerodynamics of fabric", "crowd dynamics"],
        "best_platforms": ["x", "facebook", "youtube"],
        "platform_reasoning": {
            "x": "Indian history content drives strong engagement on X. National pride + educational "
                 "value = high share rate. Perfect for @ChaosAndContext's audience.",
            "facebook": "Indian historical content is extremely popular on Facebook. Large Indian "
                        "diaspora audience. High share rate.",
            "youtube": "Epic historical visualization = high watch time. Can build into long-form "
                       "documentary content.",
            "instagram": "The golden hour empire visual is aesthetically stunning.",
        },
        "viral_score": 80,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Empires That Shaped the World' series: Gupta, Maurya, "
                            "Chola, Mongol, Ottoman, Mali",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["history", "samudragupta", "gupta", "india", "empire", "chaosandcontext"],
    },
    {
        "id": "hist_ganesh_chaturthi",
        "category": "History",
        "title": "How Ganesh Chaturthi became a freedom movement",
        "description": "Ganesh Chaturthi was once a private family festival. During British rule, "
                       "Bal Gangadhar Tilak transformed it into a public celebration — a way to "
                       "unite people, share ideas, and build a freedom movement under the guise "
                       "of religion. A festival that became political resistance.",
        "prompt": "OPENING FRAME: A quiet 19th-century Indian home, a small family clay Ganesha idol "
                  "on a modest shrine. The scene transitions: the idol grows, moves to a public pandal, "
                  "crowds gather. The camera pulls back showing streets filled with people, processions, "
                  "drummers, dancers. Paper lanterns and marigold garlands everywhere. The festival "
                  "spreads from one street to an entire city. British officers watch from a distance. "
                  "The final shot: thousands of people carrying Ganesha idols to a river at sunset, "
                  "a sea of devotion and quiet defiance. Photorealistic, cinematic, warm lighting, "
                  "ultra-detailed. Physics accurate: fabric movement follows wind dynamics, crowd "
                  "behavior follows density flow, water immersion follows fluid displacement, "
                  "fire and lamp light follows thermal radiation.",
        "physics_principles": ["fluid dynamics", "crowd density flow", "thermal radiation",
                               "wind interaction", "buoyancy", "light scattering"],
        "best_platforms": ["facebook", "x", "youtube"],
        "platform_reasoning": {
            "facebook": "Cultural/festival content with emotional resonance performs extremely well "
                        "on Facebook in India. High share and save rate.",
            "x": "The 'festival as political resistance' angle is a powerful conversation starter. "
                 "Perfect for @ChaosAndContext's storytelling style.",
            "youtube": "Cultural history with visual recreation. Good watch time.",
            "instagram": "Festival visuals are inherently aesthetic and highly saveable.",
        },
        "viral_score": 81,
        "monetization_niche": "education",
        "series_potential": "High — 'How Festivals Changed History' series: Ganesh Chaturthi, "
                            "Diwali, Holi, Onam, Durga Puja",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["history", "ganesh chaturthi", "india", "culture", "freedom", "chaosandcontext"],
    },
    {
        "id": "hist_library_alexandria",
        "category": "History",
        "title": "The Library of Alexandria — what was really lost",
        "description": "The greatest library of the ancient world held hundreds of thousands of scrolls. "
                       "When it burned, humanity lost centuries of knowledge — medicine, astronomy, "
                       "engineering, poetry. A visualization of the fire and what we lost.",
        "prompt": "OPENING FRAME: The Great Library of Alexandria in its glory — towering shelves of "
                  "papyrus scrolls, scholars reading by oil lamp, mosaic floors, statues. The camera "
                  "sweeps through grand halls. Then: a flame catches. It spreads rapidly across "
                  "dry scrolls. The fire engulfs entire sections. Burning scrolls fly upward in "
                  "thermal updrafts. The roof collapses. Smoke fills the Mediterranean sky. "
                  "Final shot: the ruins smoldering at dawn, a single intact scroll among the ashes. "
                  "Photorealistic, cinematic, dramatic fire lighting, volumetric smoke. "
                  "Physics accurate: fire propagation follows combustion science, scroll burning "
                  "follows material flammability, thermal updrafts follow convection dynamics, "
                  "structural collapse follows gravity and material failure.",
        "physics_principles": ["combustion", "convection", "structural collapse",
                               "gravity", "thermal radiation", "material flammability"],
        "best_platforms": ["x", "youtube", "facebook"],
        "platform_reasoning": {
            "x": "'What knowledge was lost when Alexandria burned?' is a proven viral question on X. "
                 "Drives massive engagement. Perfect @ChaosAndContext content.",
            "youtube": "Historical disaster content gets high watch time. Education niche RPM.",
            "facebook": "Historical content with dramatic visuals performs well across audiences.",
            "instagram": "The burning library visual is dramatic and highly shareable.",
        },
        "viral_score": 83,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Lost Knowledge' series: Alexandria, Nalanda, "
                            "House of Wisdom Baghdad, Mayan codices",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["history", "alexandria", "library", "lost knowledge", "ancient", "chaosandcontext"],
    },

    # ─── NCERT Physics (Class 11-12, CBSE) ───────────────────────
    {
        "id": "ncert_phys_projectile",
        "category": "NCERT Physics",
        "title": "Projectile Motion — why a thrown ball follows a parabola",
        "description": "NCERT Class 11, Chapter 3: Motion in a Plane. A ball thrown at an angle "
                       "traces a perfect parabola. The horizontal velocity stays constant while "
                       "vertical velocity decelerates due to gravity, then accelerates downward.",
        "prompt": "OPENING FRAME: A cricket ball is thrown at a 45-degree angle on a sunny field. "
                  "The camera follows the ball in slow motion as it traces a perfect parabolic arc. "
                  "A glowing trajectory line appears showing the path. Velocity vectors split into "
                  "horizontal (constant length) and vertical (shrinking going up, growing coming down) "
                  "arrows. The ball lands exactly where physics predicts. Photorealistic, cinematic, "
                  "sports broadcast style, ultra-detailed. Physics accurate: horizontal velocity "
                  "remains constant (no air resistance model), vertical acceleration = 9.8 m/s² "
                  "downward throughout, trajectory follows y = x tan(θ) - gx²/2u²cos²(θ), "
                  "maximum range at 45 degrees.",
        "physics_principles": ["projectile motion", "kinematics", "vector decomposition",
                               "gravity", "parabolic trajectory", "uniform acceleration"],
        "best_platforms": ["youtube", "facebook", "x"],
        "platform_reasoning": {
            "youtube": "NCERT physics content has massive search volume. Millions of CBSE + JEE "
                       "students search for visual explanations. High watch time, good RPM.",
            "facebook": "Indian student audience on Facebook is huge. Physics explainer videos "
                        "get high share rate among student communities.",
            "x": "Physics teachers and students share educational content actively on X.",
            "instagram": "The trajectory visual is clean and aesthetic — good for Reels.",
        },
        "viral_score": 78,
        "monetization_niche": "education",
        "series_potential": "Very High — 'NCERT Physics Visualized' series covering each chapter",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["physics", "ncert", "class 11", "projectile motion", "kinematics", "cbse", "education"],
    },
    {
        "id": "ncert_phys_em_waves",
        "category": "NCERT Physics",
        "title": "Electromagnetic Waves — how light travels through empty space",
        "description": "NCERT Class 12, Chapter 6: Electromagnetic Waves. A changing electric field "
                       "creates a magnetic field, which creates another electric field, and this "
                       "self-propagating chain travels at the speed of light through vacuum.",
        "prompt": "OPENING FRAME: Complete darkness. A single electric charge oscillates. A ripple "
                  "of electric field (shown as a glowing red wave) expands outward. As it moves, "
                  "it generates a perpendicular magnetic field (blue wave) that oscillates at 90 "
                  "degrees. Together they form an electromagnetic wave traveling forward at the "
                  "speed of light. The camera follows the wave as it passes through empty space, "
                  "through glass (refracting), through a prism (splitting into colors). "
                  "Photorealistic 3D visualization, dark background with glowing fields, "
                  "ultra-detailed. Physics accurate: E and B fields are perpendicular to each "
                  "other and to direction of propagation, c = 1/√(μ₀ε₀), frequency determines "
                  "color in visible spectrum, Snell's law for refraction.",
        "physics_principles": ["electromagnetic waves", "Maxwell's equations", "field interaction",
                               "speed of light", "refraction", "spectrum"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Class 12 EM waves is a high-search topic. Students struggle with the "
                       "abstract concept — visual explanation gets massive watch time.",
            "facebook": "Indian Class 12 students share physics content heavily.",
            "instagram": "The glowing 3D wave visualization is visually stunning.",
            "x": "Science teachers share and discuss EM wave visualizations actively.",
        },
        "viral_score": 80,
        "monetization_niche": "education",
        "series_potential": "Very High — part of NCERT Class 12 Physics series",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["physics", "ncert", "class 12", "em waves", "electromagnetic", "maxwell", "cbse"],
    },
    {
        "id": "ncert_phys_newton_cradle",
        "category": "NCERT Physics",
        "title": "Newton's Cradle — conservation of momentum and energy made visible",
        "description": "NCERT Class 11, Chapter 4: Laws of Motion. When one ball strikes the row, "
                       "the same number of balls swing out the other side. Momentum and kinetic "
                       "energy are conserved in every collision.",
        "prompt": "OPENING FRAME: Close-up of a Newton's cradle on a wooden desk. One steel ball "
                  "is pulled back and released. It swings forward and strikes the row. The impact "
                  "travels through the balls instantly — one ball swings out the other side, rises "
                  "to the same height, and swings back. The cycle repeats perfectly. Slow-motion "
                  "capture of the moment of collision — steel deforms microscopically, a shock "
                  "wave travels through the row. Photorealistic, macro lens, natural lighting, "
                  "shallow depth of field. Physics accurate: momentum conserved (m1v1 = m2v2), "
                  "kinetic energy conserved in elastic collision, balls swing as pendulums "
                  "following T = 2π√(L/g), steel elastic deformation follows Hooke's law.",
        "physics_principles": ["conservation of momentum", "conservation of energy", "elastic collision",
                               "pendulum motion", "Hooke's law", "shock wave propagation"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Newton's laws is the most searched physics topic. Visual demonstrations "
                       "get high watch time from Class 11 students.",
            "facebook": "Satisfying physics content is highly shareable among student communities.",
            "instagram": "The Newton's cradle visual is both educational and satisfying — high save rate.",
            "x": "Physics educators share and discuss demonstration videos actively.",
        },
        "viral_score": 76,
        "monetization_niche": "education",
        "series_potential": "High — 'Laws of Motion Visualized' series",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["physics", "ncert", "class 11", "newton", "momentum", "collision", "cbse"],
    },
    {
        "id": "ncert_phys_doppler",
        "category": "NCERT Physics",
        "title": "Doppler Effect — why an ambulance siren changes pitch as it passes",
        "description": "NCERT Class 11, Chapter 14: Waves. When a sound source moves toward you, "
                       "waves compress (higher pitch). As it moves away, waves stretch (lower pitch). "
                       "The same effect applies to light — redshift and blueshift in astronomy.",
        "prompt": "OPENING FRAME: An ambulance approaches on a city street with siren blaring. "
                  "Sound waves are visualized as expanding concentric circles. As the ambulance "
                  "moves forward, the waves ahead of it compress together (shorter wavelength = "
                  "higher pitch). Behind it, the waves stretch apart (longer wavelength = lower pitch). "
                  "A listener on the sidewalk experiences the pitch shift as the ambulance passes. "
                  "Transition: the same effect with light — a star moving away appears redder "
                  "(redshift), a star approaching appears bluer (blueshift). Photorealistic, "
                  "cinematic, split-screen showing wave compression and listener perspective. "
                  "Physics accurate: f' = f(v±v₀)/(v∓vs), wavelength compresses ahead of source "
                  "and stretches behind, Doppler shift follows exact wave equation.",
        "physics_principles": ["Doppler effect", "wave compression", "wave frequency",
                               "redshift", "blueshift", "relative motion"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Doppler effect is searched heavily by Class 11 students. Visual explanation "
                       "makes abstract concept intuitive. High watch time.",
            "facebook": "Physics concepts with real-world examples (ambulance) get high engagement.",
            "instagram": "The wave compression visual is both educational and aesthetically satisfying.",
            "x": "Science teachers love sharing Doppler effect visualizations.",
        },
        "viral_score": 77,
        "monetization_niche": "education",
        "series_potential": "High — 'Waves Visualized' series: Doppler, interference, resonance",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["physics", "ncert", "class 11", "doppler", "waves", "sound", "cbse"],
    },

    # ─── NCERT Chemistry (Class 11-12, CBSE) ─────────────────────
    {
        "id": "ncert_chem_hydrogen_bond",
        "category": "NCERT Chemistry",
        "title": "Hydrogen Bonding — why water is weird (and life exists)",
        "description": "NCERT Class 11, Chapter 4: Chemical Bonding. Hydrogen bonds between water "
                       "molecules give water its unusual properties: high boiling point, surface "
                       "tension, ice floating on water, and the ability to sustain life.",
        "prompt": "OPENING FRAME: Macro shot of a water droplet on a leaf. The camera zooms into "
                  "the molecular level — water molecules (H₂O) visible with oxygen (red) and "
                  "hydrogen (white) atoms. Dotted lines form between hydrogen of one molecule and "
                  "oxygen of another — hydrogen bonds. The molecules dance and reconnect constantly. "
                  "Camera pulls back to show surface tension holding the droplet together. Then: "
                  "ice forming — the hydrogen bonds create a crystalline lattice that's less dense "
                  "than liquid water, so ice floats. Photorealistic molecular animation, scientific "
                  "visualization style. Chemistry accurate: hydrogen bond forms between H (δ+) and "
                  "O/N/F (δ-) of adjacent molecule, bond energy ~20 kJ/mol, ice lattice is hexagonal "
                  "with lower density than liquid water.",
        "physics_principles": ["hydrogen bonding", "electrostatic interaction", "molecular dipole",
                               "surface tension", "crystal lattice formation", "density"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Chemical bonding is a core NCERT topic. Visual molecular animation is rare "
                       "and highly searched. Very high watch time.",
            "facebook": "Indian chemistry students share bonding visualizations heavily.",
            "instagram": "The molecular dance is visually mesmerizing — high save rate.",
            "x": "Chemistry teachers share molecular visualizations for classroom use.",
        },
        "viral_score": 79,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Chemical Bonding Visualized' series: ionic, covalent, "
                            "hydrogen, metallic, van der Waals",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["chemistry", "ncert", "class 11", "hydrogen bond", "water", "bonding", "cbse"],
    },
    {
        "id": "ncert_chem_redox_battery",
        "category": "NCERT Chemistry",
        "title": "Redox Reactions — how a battery actually works",
        "description": "NCERT Class 11, Chapter 7: Redox Reactions. Every battery is a redox "
                       "reaction: electrons travel from the anode (oxidation, losing electrons) "
                       "to the cathode (reduction, gaining electrons). The flow of electrons IS "
                       "electricity.",
        "prompt": "OPENING FRAME: A simple battery is cut open to reveal its internal structure. "
                  "At the anode, zinc atoms lose electrons (oxidation) — the electrons glow and "
                  "detach, traveling through the external wire toward the cathode. At the cathode, "
                  "copper ions gain electrons (reduction) and deposit as copper metal. The electron "
                  "flow lights up a small bulb. The camera follows individual electrons flowing "
                  "through the wire. Half-reactions are labeled. Photorealistic cutaway + molecular "
                  "animation, scientific visualization style. Chemistry accurate: anode = oxidation "
                  "(Zn → Zn²⁺ + 2e⁻), cathode = reduction (Cu²⁺ + 2e⁻ → Cu), electron flow "
                  "direction from anode to cathode through external circuit, salt bridge maintains "
                  "charge neutrality.",
        "physics_principles": ["redox reactions", "electron transfer", "electrochemistry",
                               "oxidation", "reduction", "electric current"],
        "best_platforms": ["youtube", "facebook", "x"],
        "platform_reasoning": {
            "youtube": "Redox reactions and electrochemistry are high-search NCERT topics. "
                       "Visual battery internals make it intuitive. Very high watch time.",
            "facebook": "Chemistry students share electrochemistry visualizations widely.",
            "x": "Chemistry teachers share battery/redox visualizations for classroom use.",
            "instagram": "The glowing electron flow is visually striking.",
        },
        "viral_score": 76,
        "monetization_niche": "education",
        "series_potential": "High — 'Electrochemistry Visualized' series: battery, electrolysis, "
                            "corrosion, galvanic cell",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["chemistry", "ncert", "class 11", "redox", "battery", "electrochemistry", "cbse"],
    },
    {
        "id": "ncert_chem_equilibrium",
        "category": "NCERT Chemistry",
        "title": "Chemical Equilibrium — the constant tug of war nobody sees",
        "description": "NCERT Class 11, Chapter 6: Equilibrium. In a reversible reaction, forward "
                       "and reverse reactions happen simultaneously. When their rates become equal, "
                       "the system is at equilibrium — concentrations stop changing even though "
                       "molecules are still reacting.",
        "prompt": "OPENING FRAME: Two chambers connected by a membrane. Blue molecules (reactants) "
                  "on the left, red molecules (products) on the right. Arrows show forward reaction "
                  "(blue → red) and reverse reaction (red → blue) happening simultaneously. Initially "
                  "forward is faster — more red forms. Then reverse speeds up. Eventually both rates "
                  "equalize — molecules still convert in both directions but concentrations stay "
                  "constant. A dynamic graph shows concentrations leveling off. The camera reveals "
                  "that 'still' is actually 'frantically active.' Photorealistic molecular animation, "
                  "scientific visualization. Chemistry accurate: at equilibrium k_forward × [reactants] "
                  "= k_reverse × [products], Kc = [products]/[reactants], Le Chatelier's principle "
                  "shown when stress is applied.",
        "physics_principles": ["chemical equilibrium", "reaction kinetics", "Le Chatelier's principle",
                               "dynamic equilibrium", "rate of reaction"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Equilibrium is one of the most searched chemistry topics. Students struggle "
                       "with the concept — visual explanation has massive watch time.",
            "facebook": "Chemistry students share equilibrium visualizations for exam prep.",
            "instagram": "The molecular tug-of-war visual is both educational and satisfying.",
            "x": "Chemistry teachers share equilibrium visualizations actively.",
        },
        "viral_score": 75,
        "monetization_niche": "education",
        "series_potential": "High — 'Equilibrium Visualized' series: chemical, ionic, Le Chatelier",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["chemistry", "ncert", "class 11", "equilibrium", "reaction", "cbse"],
    },
    {
        "id": "ncert_chem_periodic_trend",
        "category": "NCERT Chemistry",
        "title": "Periodic Table Trends — why atoms behave the way they do",
        "description": "NCERT Class 11, Chapter 3: Classification of Elements. Atomic radius "
                       "shrinks across a period (left to right) as nuclear charge increases, but "
                       "jumps down a group as new shells are added. This single trend explains "
                       "almost all chemical behavior.",
        "prompt": "OPENING FRAME: A glowing 3D periodic table floats in space. The camera zooms "
                  "into a single period (row). Atoms are shown with their electron shells — "
                  "hydrogen (1 shell, large), helium, lithium (2 shells, even larger), then moving "
                  "across period 2: each atom gains a proton (nucleus glows brighter) and the atom "
                  "shrinks as the stronger nuclear charge pulls electrons closer. Then dropping "
                  "down to the next period — a new shell appears and the atom suddenly grows. "
                  "A heat-map overlay shows atomic radius as color across the entire table. "
                  "Photorealistic 3D molecular visualization, dark scientific aesthetic. "
                  "Chemistry accurate: atomic radius decreases left to right across a period "
                  "(increasing Z_eff), increases down a group (new shell added), ionization energy "
                  "and electronegativity follow inverse trends.",
        "physics_principles": ["atomic structure", "effective nuclear charge", "electron shielding",
                               "periodic trends", "Coulomb's law"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Periodic table trends is one of the most searched NCERT chemistry topics. "
                       "3D visualization makes it instantly intuitive.",
            "facebook": "Class 11 students share periodic table content heavily.",
            "instagram": "The glowing 3D periodic table is visually stunning and save-worthy.",
            "x": "Chemistry teachers share periodic trend visualizations for classroom use.",
        },
        "viral_score": 78,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Periodic Table Visualized' series: trends, groups, "
                            "blocks, anomalous behaviors",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["chemistry", "ncert", "class 11", "periodic table", "atomic radius", "trends", "cbse"],
    },

    # ─── NCERT Maths (Class 11-12, CBSE) ─────────────────────────
    {
        "id": "ncert_math_euclid",
        "category": "NCERT Maths",
        "title": "Euclid's Geometry — the 5 rules that built all of mathematics",
        "description": "NCERT Class 9, Chapter 5: Introduction to Euclid's Geometry. Five simple "
                       "postulates that every mathematical truth is built on. The axiomatic method "
                       "that started it all.",
        "prompt": "OPENING FRAME: An ancient Greek scholar drawing in sand with a stick. He draws a "
                  "straight line — it extends infinitely in both directions, the camera follows it "
                  "racing across the landscape. He draws a circle — it spins into a perfect disc. "
                  "Right angles snap into place like building blocks. Parallel lines stretch forever "
                  "without touching. These five simple rules light up one by one, each spawning a "
                  "cascade of mathematical structures: triangles, polygons, pyramids, proofs. "
                  "The camera pulls back to reveal the entire edifice of geometry built from five "
                  "lines in the sand. Photorealistic, cinematic, warm Mediterranean light, "
                  "ultra-detailed. Physics accurate: geometric constructions follow compass-and-straightedge "
                  "rules, lines are perfectly straight, circles are mathematically exact.",
        "physics_principles": ["geometric construction", "axiomatic systems", "infinity",
                               "parallel postulate", "mathematical proof"],
        "best_platforms": ["youtube", "facebook", "x"],
        "platform_reasoning": {
            "youtube": "NCERT geometry content has steady search volume. Visual Euclid is rare "
                       "and engaging. High watch time.",
            "facebook": "Indian student communities share maths content heavily.",
            "x": "Math history + visual storytelling is a proven @ChaosAndContext format.",
            "instagram": "The cascading geometric structures are visually stunning.",
        },
        "viral_score": 76,
        "monetization_niche": "education",
        "series_potential": "High — 'Math Built From Nothing' series: Euclid, Set theory, Peano axioms",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["maths", "ncert", "class 9", "euclid", "geometry", "axioms", "cbse"],
    },
    {
        "id": "ncert_math_calculus",
        "category": "NCERT Maths",
        "title": "Calculus — the mathematics of change, visualized",
        "description": "NCERT Class 11-12: Limits and Derivatives. Calculus answers one question: "
                       "how fast is something changing RIGHT NOW? Derivatives are instantaneous "
                       "rate of change. Integrals accumulate change. This is the engine of physics.",
        "prompt": "OPENING FRAME: A car accelerating on a highway. A speedometer needle climbs. "
                  "The camera splits the screen: left side shows the car moving, right side shows "
                  "a graph of position vs time. A tangent line appears on the curve — its slope IS "
                  "the speed at that instant. The car accelerates, the tangent steepens. Then the "
                  "reverse: area under the velocity curve fills in — that's the distance traveled. "
                  "The Fundamental Theorem of Calculus appears as a glowing equation connecting "
                  "both sides. Photorealistic, cinematic, split-screen with mathematical overlay, "
                  "ultra-detailed. Physics accurate: derivative = instantaneous rate of change "
                  "d/dx(x²) = 2x, integral = accumulation ∫v dt = position, FTC connects them.",
        "physics_principles": ["limits", "derivatives", "integration", "rate of change",
                               "Fundamental Theorem of Calculus", "tangent lines"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Calculus is one of the most searched maths topics by Class 11-12 students. "
                       "Visual explanation is extremely rare — massive watch time.",
            "facebook": "Indian students share calculus visualizations for exam prep.",
            "instagram": "The split-screen visual of car + graph is striking.",
            "x": "Math teachers share calculus visualizations actively.",
        },
        "viral_score": 80,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Calculus Visualized' series: limits, derivatives, "
                            "integrals, applications, differential equations",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["maths", "ncert", "class 11", "calculus", "derivatives", "cbse"],
    },
    {
        "id": "ncert_math_probability",
        "category": "NCERT Maths",
        "title": "Probability — the math that governs luck, chance, and life",
        "description": "NCERT Class 11-12: Probability. From coin flips to Bayes' theorem. "
                       "Probability is how we make sense of an uncertain world. Every decision, "
                       "every insurance premium, every weather forecast — it's all probability.",
        "prompt": "OPENING FRAME: A single coin spinning in the air, frozen in slow motion. "
                  "The camera orbits the coin. Heads and tails are visible. A split probability "
                  "bar appears: 50/50. The coin lands — heads. Flip again. And again. The screen "
                  "fills with hundreds of coin flips, the ratio converging to 50/50. Then: dice, "
                  "cards, a lottery machine. The Law of Large Numbers visualized as outcomes "
                  "converging to expected values. Then a dramatic shift — conditional probability: "
                  "given new evidence, probabilities UPDATE. Bayes' theorem glows as a formula. "
                  "Photorealistic, cinematic, macro photography + mathematical overlay, ultra-detailed. "
                  "Physics accurate: coin flip follows rigid body dynamics, probability distributions "
                  "follow exact mathematical equations, convergence follows Law of Large Numbers.",
        "physics_principles": ["probability theory", "Law of Large Numbers", "Bayes' theorem",
                               "conditional probability", "random variables", "convergence"],
        "best_platforms": ["youtube", "x", "facebook"],
        "platform_reasoning": {
            "youtube": "Probability is widely searched by NCERT students. Visual convergence "
                       "is satisfying and educational.",
            "x": "'Probability governs your entire life' is a great conversation hook.",
            "facebook": "Indian students share probability content for exam prep.",
            "instagram": "The converging coin flips visual is mesmerizing.",
        },
        "viral_score": 77,
        "monetization_niche": "education",
        "series_potential": "High — 'Probability Visualized' series: basics, Bayes, distributions, "
                            "random walks, Monte Carlo",
        "estimated_rpm": 0.08,
        "trending": False,
        "tags": ["maths", "ncert", "class 11", "probability", "bayes", "chance", "cbse"],
    },

    # ─── NCERT Biology (Class 11-12, CBSE) ──────────────────────
    {
        "id": "ncert_bio_mitosis",
        "category": "NCERT Biology",
        "title": "Mitosis — how one cell becomes two (and you were once one cell)",
        "description": "NCERT Class 11, Chapter 10: Cell Cycle and Cell Division. Mitosis is the "
                       "process by which one cell divides into two identical copies. Every cell in "
                       "your body came from this process. You started as a single cell.",
        "prompt": "OPENING FRAME: Inside a cell, viewed as if through a powerful microscope. "
                  "Chromosomes condense — they look like X-shaped structures thickening and becoming "
                  "visible. The nuclear envelope dissolves. Spindle fibers shoot out from opposite "
                  "poles and grab the chromosomes. They align in the center, then snap apart — "
                  "each chromatid pulled to opposite ends. The cell pinches in the middle and splits "
                  "into two. The camera zooms out to show millions of cells dividing simultaneously, "
                  "building tissue. Photorealistic 3D molecular animation, microscope aesthetic, "
                  "dark background with glowing cellular structures, ultra-detailed. Biology accurate: "
                  "prophase → metaphase → anaphase → telophase, spindle fibers follow microtubule "
                  "dynamics, chromosomes follow karyotype structure, cytokinesis follows membrane "
                  "physics.",
        "physics_principles": ["microtubule dynamics", "membrane physics", "molecular motor forces",
                               "surface tension", "viscoelastic deformation"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Cell division is a core NCERT biology topic. 3D molecular animation of "
                       "mitosis is extremely rare — very high watch time.",
            "facebook": "Biology students share cell division visualizations heavily.",
            "instagram": "The glowing cellular structures are visually stunning.",
            "x": "Biology teachers share mitosis animations for classroom use.",
        },
        "viral_score": 79,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Cell Division Visualized' series: mitosis, meiosis, "
                            "binary fission, apoptosis",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["biology", "ncert", "class 11", "mitosis", "cell division", "cbse"],
    },
    {
        "id": "ncert_bio_photosynthesis",
        "category": "NCERT Biology",
        "title": "Photosynthesis — how plants eat sunlight",
        "description": "NCERT Class 11, Chapter 13: Photosynthesis in Higher Plants. Plants capture "
                       "sunlight and turn it into sugar. This single process feeds almost all life "
                       "on Earth and produces the oxygen you breathe.",
        "prompt": "OPENING FRAME: A single leaf in sunlight. The camera zooms into the leaf surface, "
                  "into a stomate, into a chloroplast. Inside, stacked green discs (thylakoids) catch "
                  "light particles — photons streak in and are absorbed. Water molecules split, "
                  "releasing oxygen that bubbles upward. The energy drives a molecular machine "
                  "(ATP synthase) that spins like a turbine, producing ATP. Carbon dioxide enters "
                  "and is assembled into glucose sugar, molecule by molecule. The camera pulls back "
                  "out to the leaf, now producing a tiny bubble of oxygen. Photorealistic 3D "
                  "molecular animation, natural lighting transitioning to molecular glow, ultra-detailed. "
                  "Biology accurate: light reactions in thylakoids (PSII → PSI), Calvin cycle in stroma, "
                  "ATP synthase is a rotary motor, O₂ released from water splitting.",
        "physics_principles": ["photon absorption", "electron transport chain", "molecular machinery",
                               "thermodynamics of biological systems", "diffusion"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Photosynthesis is a top-searched NCERT biology topic. Visual molecular "
                       "animation is extremely rare and engaging. Very high watch time.",
            "facebook": "Biology students share photosynthesis visualizations for exam prep.",
            "instagram": "The spinning ATP synthase and glowing chloroplast are visually stunning.",
            "x": "Biology teachers share photosynthesis animations for classroom use.",
        },
        "viral_score": 81,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Life's Molecular Machines' series: photosynthesis, "
                            "respiration, DNA replication, protein synthesis",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["biology", "ncert", "class 11", "photosynthesis", "chloroplast", "cbse"],
    },
    {
        "id": "ncert_bio_dna_replication",
        "category": "NCERT Biology",
        "title": "DNA Replication — the molecular copy machine inside you",
        "description": "NCERT Class 12, Chapter 6: Molecular Basis of Inheritance. Every time a cell "
                       "divides, it must copy 3 billion letters of DNA perfectly. The machinery that "
                       "does this is faster and more accurate than any human printer.",
        "prompt": "OPENING FRAME: A DNA double helix slowly rotating, its two strands glowing "
                  "in different colors. An enzyme (helicase) appears and unzips the helix — the two "
                  "strands separate like a zipper opening. Another enzyme (DNA polymerase) slides "
                  "along each strand, reading it and assembling a new complementary strand letter by "
                  "letter: A pairs with T, C pairs with G. The letters click into place with satisfying "
                  "precision. Two complete DNA molecules emerge where there was one. The camera "
                  "follows DNA polymerase at molecular speed — it's building 50 letters per second. "
                  "Photorealistic 3D molecular animation, scientific visualization, dark background "
                  "with glowing molecular structures, ultra-detailed. Biology accurate: helicase "
                  "unwinds, DNA polymerase adds nucleotides 5'→3', leading strand continuous, lagging "
                  "strand in Okazaki fragments, semi-conservative replication.",
        "physics_principles": ["molecular machinery", "hydrogen bonding", "enzyme kinetics",
                               "molecular motor forces", "thermodynamics of biological systems"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "DNA replication is one of the most fascinating and searched biology topics. "
                       "Molecular animation is extremely rare — massive watch time.",
            "facebook": "Biology students share DNA content heavily for NEET preparation.",
            "instagram": "The glowing helix and clicking letters are visually mesmerizing.",
            "x": "Biology teachers share DNA animations for classroom use.",
        },
        "viral_score": 83,
        "monetization_niche": "education",
        "series_potential": "Very High — 'Molecular Biology Visualized' series: DNA replication, "
                            "transcription, translation, gene expression",
        "estimated_rpm": 0.08,
        "trending": True,
        "tags": ["biology", "ncert", "class 12", "dna", "replication", "genetics", "cbse"],
    },

    # ─── Anime / Silly / Viral ──────────────────────────────────
    {
        "id": "anime_battle_physics",
        "category": "Anime & Silly",
        "title": "Anime battle but with REAL physics — what if Goku's Kamehameha obeyed thermodynamics?",
        "description": "What happens when anime attacks follow actual physics? A Kamehameha blast "
                       "is basically a directed energy beam — the energy, heat, and recoil would "
                       "have real consequences. This is silly, fun, and secretly educational.",
        "prompt": "OPENING FRAME: An anime-style character in a dramatic battle pose charges up "
                  "a glowing energy blast between cupped hands. But this time, physics labels "
                  "appear: 'Energy output: 10^15 joules'. The blast fires — and the RECOIL launches "
                  "the character backward through a mountain (Newton's Third Law). The air in front "
                  "of the beam turns to plasma (ionization). The ground beneath cracks from the "
                  "pressure wave. The beam hits the ocean — instant vaporization, steam explosion, "
                  "tsunami. The camera follows the chain of real physics consequences from one "
                  "anime attack. Anime art style but with realistic physics simulation overlays. "
                  "Physics accurate: Newton's Third Law (recoil = forward momentum), E=mc² for "
                  "energy-mass conversion, plasma formation at high temperatures, pressure wave "
                  "propagation, water vaporization thermodynamics.",
        "physics_principles": ["Newton's Third Law", "energy conservation", "recoil momentum",
                               "plasma formation", "thermodynamics", "pressure waves"],
        "best_platforms": ["youtube", "x", "instagram"],
        "platform_reasoning": {
            "youtube": "Anime + physics is a proven viral format. 'What if anime obeyed physics' "
                       "gets millions of views. Crosses education and entertainment audiences.",
            "x": "Anime content goes viral on X. Physics analysis adds a unique angle that drives "
                 "replies and debates.",
            "instagram": "Anime visuals + physics labels is a scroll-stopping format.",
            "facebook": "Anime + humor content performs well on Facebook Reels.",
        },
        "viral_score": 88,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Anime But With Real Physics' series: Kamehameha, "
                            "Rasengan, Bankai, Titan transformation, Nen ability",
        "estimated_rpm": 0.05,
        "trending": True,
        "tags": ["anime", "physics", "goku", "kamehameha", "silly", "viral", "fun"],
    },
    {
        "id": "anime_naruto_rasengan",
        "category": "Anime & Silly",
        "title": "Naruto's Rasengan but it's actually a fluid dynamics problem",
        "description": "The Rasengan is a spinning ball of chakra — which is basically a "
                       "high-velocity vortex. What would actually happen if you created a "
                       "contained tornado in your hand? Fluid dynamics has answers.",
        "prompt": "OPENING FRAME: An anime-style ninja holding a glowing blue sphere of spinning "
                  "energy in his palm. The camera zooms in — the sphere is a vortex, fluid spiraling "
                  "at incredible speed. Physics overlay appears: 'Angular velocity: 10,000 RPM'. "
                  "The air around it is being sucked in and flung outward (centripetal force). "
                  "The ninja's hand should be shredded by the shear forces. When he pushes it "
                  "forward into a wall, it doesn't just break the wall — it creates a cavitation "
                  "void, the wall material is pulverized by the pressure differential, and the "
                  "shockwave shatters windows for 100 meters. Anime art style with realistic "
                  "fluid dynamics overlay. Physics accurate: vortex follows Navier-Stokes equations, "
                  "centripetal force F = mv²/r, cavitation follows Bernoulli's principle, "
                  "shockwave follows pressure wave dynamics.",
        "physics_principles": ["fluid dynamics", "vortex mechanics", "centripetal force",
                               "cavitation", "Bernoulli's principle", "shockwave propagation"],
        "best_platforms": ["youtube", "x", "instagram"],
        "platform_reasoning": {
            "youtube": "Naruto + physics is a proven viral crossover. Massive anime audience + "
                       "curiosity-driven educational angle.",
            "x": "Anime physics analysis is extremely shareable. Drives debates between fans.",
            "instagram": "The glowing Rasengan visual is eye-catching.",
            "facebook": "Anime content performs well on Facebook Reels in India.",
        },
        "viral_score": 86,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Anime But With Real Physics' series",
        "estimated_rpm": 0.05,
        "trending": True,
        "tags": ["anime", "naruto", "rasengan", "fluid dynamics", "physics", "viral"],
    },
    {
        "id": "silly_domino_physics",
        "category": "Anime & Silly",
        "title": "1 million dominoes falling in slow motion — the most satisfying chain reaction",
        "description": "Pure satisfaction. Dominoes falling in increasingly elaborate patterns. "
                       "No educational message, no deep meaning — just physics doing its thing "
                       "and your brain loving it. This is what goes viral.",
        "prompt": "OPENING FRAME: A single domino tips over. It hits the next one, which hits "
                  "two, which hit four. The chain reaction accelerates. The camera follows the "
                  "wave of falling dominoes through increasingly elaborate paths: spirals, "
                  "staircases, branching paths that rejoin, dominoes that trigger ramps, balls "
                  "that roll into dominoes, dominoes that fall in 3D structures. The sound is "
                  "a rhythmic clicking that builds to a crescendo. The final domino triggers "
                  "a massive structure that collapses in a satisfying chain. Shot in extreme "
                  "slow motion with shallow depth of field. Photorealistic, cinematic, macro "
                  "photography, natural lighting, ultra-detailed. Physics accurate: domino "
                  "toppling follows rigid body dynamics, gravitational torque, collision "
                  "transfer of momentum, chain reaction follows energy cascade, domino spacing "
                  "affects propagation speed.",
        "physics_principles": ["rigid body dynamics", "gravitational torque", "momentum transfer",
                               "chain reaction", "energy cascade", "collision physics"],
        "best_platforms": ["youtube", "facebook", "instagram"],
        "platform_reasoning": {
            "youtube": "Domino videos are among the most-watched satisfying content on YouTube. "
                       "Millions of views are common. High watch time.",
            "facebook": "Satisfying content is the #1 shared category on Facebook Reels.",
            "instagram": "Satisfying content has the highest save rate on Instagram.",
            "x": "Satisfying videos get shared as mood content — 'watch this to calm down'.",
        },
        "viral_score": 90,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Satisfying Physics' series: dominoes, marbles, "
                            "kinetic sand, slinky, ferrofluid",
        "estimated_rpm": 0.03,
        "trending": True,
        "tags": ["satisfying", "dominoes", "chain reaction", "silly", "viral", "physics"],
    },
    {
        "id": "silly_what_if_rain_up",
        "category": "Anime & Silly",
        "title": "What if rain fell UP instead of down? A physics thought experiment",
        "description": "A completely silly question with a real physics answer. If gravity reversed "
                       "for water droplets, what would happen? Puddles would float. Rivers would "
                       "flow into the sky. Your umbrella would be useless. Fun, visual, viral.",
        "prompt": "OPENING FRAME: A rainy city street. The rain is falling normally. Then — "
                  "something changes. A single raindrop stops mid-air, then starts rising. "
                  "Another. Another. All the rain starts flowing upward. Puddles lift off the "
                  "ground as spheres of water. Car tires throw water UP. People's hair defies "
                  "gravity as water droplets rise from wet hair. Rivers reverse — water cascades "
                  "upward from the surface into the sky. The ocean starts draining upward into "
                  "the clouds. The city is drenched from below. The camera follows a single "
                  "droplet rising from a puddle, past rooftops, into the clouds. Photorealistic, "
                  "cinematic, dramatic, ultra-detailed. Physics accurate: if gravitational "
                  "acceleration reverses to +9.8 m/s² upward, water droplets follow parabolic "
                  "upward trajectories, surface tension causes puddles to form spheres, Bernoulli "
                  "effects on rivers, atmospheric moisture dynamics.",
        "physics_principles": ["gravity reversal", "fluid dynamics", "surface tension",
                               "parabolic trajectories", "atmospheric physics"],
        "best_platforms": ["youtube", "x", "instagram"],
        "platform_reasoning": {
            "youtube": "'What if' physics content is a proven viral format. High curiosity factor, "
                       "high watch time.",
            "x": "'What if rain fell up?' is a perfect conversation starter — drives replies, "
                 "quotes, and shares.",
            "instagram": "The reversed-rain visual is striking and scroll-stopping.",
            "facebook": "What-if content performs well on Facebook Reels.",
        },
        "viral_score": 87,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'What If Physics' series: rain falls up, gravity stops, "
                            "light is slow, friction disappears, time runs backward",
        "estimated_rpm": 0.05,
        "trending": True,
        "tags": ["what if", "physics", "rain", "gravity", "silly", "thought experiment", "viral"],
    },
    {
        "id": "anime_aot_titan_physics",
        "category": "Anime & Silly",
        "title": "Attack on Titan: Could a 15-meter Titan actually exist? (Square-Cube Law says NO)",
        "description": "The Titans in Attack on Titan are 15 meters tall. But the square-cube law "
                       "in biology says that when you scale up an organism, its volume (and weight) "
                       "grows faster than its bone cross-section (and strength). A 15-meter human "
                       "would instantly collapse under its own weight. Unless...",
        "prompt": "OPENING FRAME: A normal human stands next to a 15-meter Titan (anime style). "
                  "Physics overlay: 'Height ×8.5, Volume ×614, Bone strength ×72'. The Titan takes "
                  "one step — and its legs shatter. The bones cannot support the weight. The Titan "
                  "collapses in slow motion. Then the question: 'Unless their bones are made of "
                  "something else?' The analysis continues — what material could support a 15-meter "
                  "humanoid? Carbon nanotubes? Titanium? The Titan gets back up, now with glowing "
                  "reinforced bones visible through semi-transparent skin. Anime art style with "
                  "scientific analysis overlay. Physics accurate: square-cube law (volume ∝ L³, "
                  "cross-section ∝ L²), compressive strength of bone ~170 MPa, scaling of "
                  "metabolic rate, buckling load F = π²EI/L² (Euler's formula).",
        "physics_principles": ["square-cube law", "compressive strength", "bone mechanics",
                               "Euler buckling formula", "metabolic scaling", "material science"],
        "best_platforms": ["youtube", "x", "facebook"],
        "platform_reasoning": {
            "youtube": "Anime + biology/physics analysis is a proven viral format. AoT has a "
                       "massive fan base. 'Could Titans exist?' gets millions of views.",
            "x": "AoT fans love debating Titan biology. Drives massive replies and quote tweets.",
            "facebook": "Anime analysis content performs well on Facebook in India.",
            "instagram": "The side-by-side scale comparison is visually striking.",
        },
        "viral_score": 85,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Could Anime Exist?' series: Titans, Zanpakuto, "
                            "Quirks, Nen, Devil Fruits",
        "estimated_rpm": 0.05,
        "trending": True,
        "tags": ["anime", "attack on titan", "biology", "square cube law", "physics", "viral"],
    },
    {
        "id": "silly_1000_balls",
        "category": "Anime & Silly",
        "title": "1000 balls falling through a giant pegboard — the most satisfying physics demo ever",
        "description": "A Galton board (bean machine) the size of a building. 1000 balls dropped "
                       "simultaneously through a massive pegboard. Each bounce is random, but "
                       "the final distribution is a perfect bell curve. Pure satisfaction + "
                       "stealth statistics lesson.",
        "prompt": "OPENING FRAME: A massive pegboard the size of a building, viewed from below. "
                  "1000 glowing balls are released from the top. They cascade downward, bouncing "
                  "off pegs in a mesmerizing cascade of random paths. Each ball makes a satisfying "
                  "click as it hits a peg. The balls collect at the bottom, and as more arrive, "
                  "a pattern emerges: a perfect bell curve (normal distribution). The camera "
                  "follows individual balls on their chaotic journeys, then pulls back to show "
                  "the beautiful order emerging from chaos. Photorealistic, cinematic, slow motion "
                  "sections, shallow depth of field, ultra-detailed. Physics accurate: each bounce "
                  "follows elastic collision with gravity, ball trajectory follows projectile motion, "
                  "distribution converges to normal (Central Limit Theorem), peg arrangement follows "
                  "Pascal's triangle.",
        "physics_principles": ["elastic collision", "gravity", "probability distributions",
                               "Central Limit Theorem", "Pascal's triangle", "random walk"],
        "best_platforms": ["youtube", "instagram", "facebook"],
        "platform_reasoning": {
            "youtube": "Satisfying physics demonstrations get millions of views. The bell curve "
                       "reveal at the end adds educational value that boosts watch time.",
            "instagram": "Satisfying + glowing balls + bell curve = maximum save rate.",
            "facebook": "Satisfying content is the top shared category on Facebook.",
            "x": "'Chaos creates order' is a great conversation hook.",
        },
        "viral_score": 89,
        "monetization_niche": "entertainment",
        "series_potential": "Very High — 'Satisfying Physics' series",
        "estimated_rpm": 0.03,
        "trending": True,
        "tags": ["satisfying", "physics", "probability", "bell curve", "silly", "viral"],
    },
]

# Category metadata
CATEGORIES = {
    "Physics": {"icon": "⚛️", "description": "Physical phenomena, forces, waves, motion"},
    "Chemistry": {"icon": "🧪", "description": "Chemical reactions, crystals, glow, color changes"},
    "Nature": {"icon": "🌊", "description": "Natural phenomena, bioluminescence, aurora, weather"},
    "Satisfying": {"icon": "✨", "description": "ASMR, oddly satisfying, cutting, crushing, flowing"},
    "Geography": {"icon": "🌍", "description": "Scale, depth, height, places, planets"},
    "Engineering": {"icon": "⚙️", "description": "How things work, mechanisms, machines"},
    "History": {"icon": "📜", "description": "History, science, culture — storytelling for @ChaosAndContext"},
    "NCERT Physics": {"icon": "⚛️", "description": "Class 11-12 CBSE physics concepts visualized"},
    "NCERT Chemistry": {"icon": "🧪", "description": "Class 11-12 CBSE chemistry concepts visualized"},
    "NCERT Maths": {"icon": "📐", "description": "Class 9-12 CBSE maths concepts visualized"},
    "NCERT Biology": {"icon": "🧬", "description": "Class 11-12 CBSE biology concepts visualized"},
    "Anime & Silly": {"icon": "🎨", "description": "Anime physics, what-if scenarios, satisfying content — pure viral"},
}


def get_ideas(
    category: str = "",
    trending_only: bool = False,
    limit: int = 20,
    random_pick: bool = False,
) -> list[dict]:
    """
    Get content ideas, optionally filtered by category or trending status.
    """
    results = IDEAS.copy()

    if category:
        results = [i for i in results if i["category"].lower() == category.lower()]
    if trending_only:
        results = [i for i in results if i.get("trending")]

    if random_pick and results:
        results = [random.choice(results)]

    return results[:limit]


def get_idea(idea_id: str) -> dict:
    """Get a specific idea by ID."""
    for idea in IDEAS:
        if idea["id"] == idea_id:
            return idea
    return None


def get_categories() -> dict:
    """Return all categories with metadata."""
    return CATEGORIES


def get_idea_with_analysis(idea_id: str) -> dict:
    """
    Get an idea with full analysis: enhanced prompt with physics realism,
    viral score, and platform recommendations.
    """
    idea = get_idea(idea_id)
    if not idea:
        return None

    # Enhance prompt with physics realism
    enhanced = enhance_physics_realism(
        idea["prompt"],
        physics_principles=idea.get("physics_principles", []),
        maximize_realism=True,
    )

    # Score viral potential
    score = score_viral_potential(idea["prompt"])

    # Build platform recommendations with full scoring data
    full_recs = recommend_platforms(
        prompt=idea.get("prompt", ""),
        category=idea.get("category", ""),
        tags=idea.get("tags", []),
        top_n=4,
    )
    # Merge: use full_recs for score/monetization_rank/platform_info,
    # but keep original reasoning from idea if available
    platform_recs = []
    for rec in full_recs["rankings"]:
        platform = rec["platform"]
        reasoning = idea.get("platform_reasoning", {}).get(platform, rec.get("reasoning", ""))
        platform_recs.append({
            "platform": platform,
            "reasoning": reasoning,
            "rank": rec["rank"],
            "score": rec["score"],
            "monetization_rank": rec["monetization_rank"],
            "platform_info": rec.get("platform_info", {}),
        })

    return {
        "idea": idea,
        "enhanced_prompt": enhanced["enhanced_prompt"],
        "physics_notes": enhanced["physics_notes"],
        "viral_score": score,
        "platform_recommendations": platform_recs,
        "recommended_provider": _recommend_provider(idea),
    }


def _recommend_provider(idea) -> str:
    """Recommend the best AI video provider for this idea."""
    category = idea.get("category", "")

    # Veo 3.1 for maximum physics realism (science content)
    if category in ("Physics", "Chemistry", "Nature", "Geography"):
        return "veo"

    # Kling 3.0 for realistic human subjects/motion
    if "human" in idea.get("prompt", "").lower() or "person" in idea.get("prompt", "").lower():
        return "kling"

    # MiniMax for satisfying/ASMR (fast, cheap, high volume)
    if category == "Satisfying":
        return "minimax"

    # Runway for engineering/brand content
    if category == "Engineering":
        return "runway"

    # Default
    return "veo"


def get_random_idea() -> dict:
    """Get a random idea with full analysis — for 'surprise me' feature."""
    idea = random.choice(IDEAS)
    return get_idea_with_analysis(idea["id"])


def get_trending_ideas(limit: int = 10) -> list[dict]:
    """Get currently trending ideas."""
    return [i for i in IDEAS if i.get("trending")][:limit]


def get_best_earning_ideas(limit: int = 10) -> list[dict]:
    """Get ideas sorted by earning potential (RPM × viral score)."""
    scored = sorted(IDEAS, key=lambda i: i.get("estimated_rpm", 0) * i.get("viral_score", 0), reverse=True)
    return scored[:limit]
