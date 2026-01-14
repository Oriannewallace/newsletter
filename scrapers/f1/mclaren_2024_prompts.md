# McLaren MCL38 2024 Evolution - AI Prompts

## Project: Option A - Single Year Evolution
**Story**: "How upgrades won the championship"
**Stages**: Pre-Miami → Miami Upgrade → Final Spec

---

## NANO BANANA PROMPTS (Image Generation)

### Stage 1: Pre-Miami Spec (Rounds 1-5)
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange and blue livery, 2024 pre-Miami specification. Traditional sidepod design with full bodywork coverage, standard floor edges visible. The car is centered in a void with dramatic studio lighting. Clean, photorealistic render with sharp details on the front wing, halo device, and rear wing. 3/4 front angle view showing the distinctive papaya orange color and blue accents. Dark background with subtle reflections on the floor.
```

### Stage 2: Miami Mega-Upgrade Spec (Round 6+)
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange and blue livery, 2024 Miami upgrade specification. Revolutionary hollowed-out lower sidepods creating dramatic undercut, redesigned floor edges, new coke bottle section with tighter waist. The car is centered in a void with dramatic studio lighting. Clean, photorealistic render showing the aggressive new sidepod sculpting. 3/4 front angle view highlighting the visual difference in sidepod shape. Dark background with subtle reflections.
```

### Stage 3: Championship-Winning Final Spec (Round 24)
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange and blue livery, 2024 championship-winning final specification. Refined hollowed sidepods, optimized floor edges, championship number 1 visible. The car is centered in a void with dramatic studio lighting, celebratory atmosphere. Clean, photorealistic render with premium finish. 3/4 front angle view showing the evolved aerodynamic package. Dark background with golden accent lighting suggesting victory.
```

### Alternative Angles (for each stage)
**Side Profile:**
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange and blue livery, [SPEC VERSION]. Perfect side profile view showing the full length of the car, sidepod shape clearly visible, floor edge detail, rear wing profile. Centered in a void, studio lighting, dark background, photorealistic render.
```

**Rear 3/4 View:**
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange and blue livery, [SPEC VERSION]. Rear 3/4 angle showing the diffuser, rear wing, coke bottle section, and engine cover. Centered in a void, studio lighting highlighting the aerodynamic surfaces, dark background, photorealistic render.
```

---

## VEO 3 PROMPT (Video Generation - 360° Morphing Spin)

### Main Animation Prompt
```
Subject: A single McLaren MCL38 Formula 1 car centered in a void, executing a very slow, smooth, and continuous 360-degree spin. The car undergoes a fluid metamorphosis while spinning, transforming through three distinct stages:

Stage 1 (0-120°): Pre-Miami specification with traditional full sidepods
Stage 2 (120-240°): Miami upgrade with dramatically hollowed sidepods and new floor
Stage 3 (240-360°): Championship-winning final spec with refined aero

Motion Dynamics (Critical): The spinning motion must be completely continuous with constant angular velocity. Do not pause or freeze during the shape-shift transformation. The rotation speed is slow, cinematic, and linear.

Visual Style: Photorealistic McLaren papaya orange and blue livery. Dark void background with subtle floor reflections. Dramatic studio lighting that follows the car. The morphing between specs should be smooth and fluid, like liquid metal reshaping.

Camera: Fixed position, car rotates in center of frame. Slight low angle to emphasize the aggressive F1 stance.
```

### Shorter Loop Version (Single Transformation)
```
Subject: A McLaren MCL38 Formula 1 car in papaya orange livery, centered in a dark void, executing a slow 180-degree rotation. During the rotation, the car's sidepods smoothly morph from traditional full bodywork to the revolutionary hollowed Miami-spec design.

Motion Dynamics: Continuous rotation, no pauses. Smooth fluid transformation of the sidepod shape as if the bodywork is reshaping itself. Cinematic, slow movement.

Visual Style: Photorealistic, dramatic lighting, dark background with reflections. The transformation should feel magical yet technically grounded.
```

---

## FRAMER COMPONENT SPEC

### Toggle Controls
- **Slider or Buttons**: "Pre-Miami" | "Miami Upgrade" | "Final Spec"
- **Auto-play option**: Cycles through all 3 with morphing animation
- **Play/Pause control** for the spinning video

### Labels/Annotations to Display
| Stage | Label | Stats |
|-------|-------|-------|
| Pre-Miami | "Rounds 1-5" | "19.2 pts/race avg" |
| Miami | "Round 6 Upgrade" | "+0.5s per lap" |
| Final | "Championship Spec" | "31.1 pts/race avg" |

### Visual Callouts (Optional Overlay)
- Arrow pointing to sidepods: "Hollowed undercut - key to Miami pace"
- Arrow pointing to floor: "New floor edge design"
- Arrow pointing to coke bottle: "Tighter waist for better airflow"

---

## WORKFLOW

1. **Generate base images** in Nano Banana (all 3 stages, 3/4 front angle)
2. **Review and refine** - may need multiple generations to get consistent car shape
3. **Feed into Veo 3** for spinning/morphing video
4. **Export video** in web-friendly format
5. **Build Framer component** with toggle and labels
6. **Embed in newsletter** or website

---

## NOTES FOR LATER: Option B (Multi-Year Winners)

For future expansion, same workflow but with:
- 2024: McLaren MCL38 (papaya orange)
- 2023: Red Bull RB19 (dark blue)
- 2022: Red Bull RB18 (dark blue)
- 2021: Mercedes W12 (silver/teal)

Toggle would switch between years instead of upgrade stages.
