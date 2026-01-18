# Branded Presentation Example

This example demonstrates using a template image as a style reference to maintain visual consistency across all slides.

## Workflow

1. **Generate a template** - Create a base design with colors, layout elements, and visual style (no content)
2. **Use template as input** - Pass the template with `-i` flag when generating each slide
3. **Describe slide content** - The prompt focuses on content while the template ensures consistent styling

---

## Template

**File:** `template.png`

**Design elements:**
- Dark navy blue background (#1a1a2e)
- Electric cyan accent bar on left (#00d9ff)
- Geometric triangle logo in top right
- Thin cyan horizontal line at bottom
- Futuristic tech aesthetic

**Command:**
```bash
./nanobanana -aspect 16:9 -size 2K -o template.png \
  "A presentation slide template with dark navy blue background (#1a1a2e). Left side has a vertical accent bar in electric cyan (#00d9ff). Top right corner has a small geometric logo of three stacked triangles in cyan. Bottom has a thin cyan horizontal line. Clean, futuristic tech aesthetic. No text, just the visual framework and design elements."
```

---

## Slide 1: Title

**Content:** Company name "NEXUS AI" with tagline "Intelligence Amplified"

**Command:**
```bash
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01_title.png \
  "Using this template style exactly, create a title slide with 'NEXUS AI' as large bold text in white, centered. Below it in smaller cyan text: 'Intelligence Amplified'. Keep the dark navy background, cyan accent bar on left, geometric logo top right, and bottom line from the template."
```

---

## Slide 2: Three Pillars

**Content:** Three key product pillars with icons

**Command:**
```bash
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02_pillars.png \
  "Using this template style exactly, create a slide showing three vertical columns. Each column has a glowing cyan icon at top and white label below. Column 1: brain icon, 'ANALYZE'. Column 2: lightning bolt icon, 'AUTOMATE'. Column 3: chart trending up icon, 'ACCELERATE'. Keep the dark navy background, cyan accent bar, geometric logo, and bottom line from the template."
```

---

## Slide 3: Contact

**Content:** Closing slide with contact information

**Command:**
```bash
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_03_contact.png \
  "Using this template style exactly, create a closing slide. Large white text says 'LET'S CONNECT' centered. Below it show: email icon with 'hello@nexus.ai', globe icon with 'nexus.ai'. Icons are cyan, text is white. Keep the dark navy background, cyan accent bar, geometric logo, and bottom line from the template."
```

---

## Commands Summary

```bash
# Step 1: Generate template (style reference)
./nanobanana -aspect 16:9 -size 2K -o template.png "template prompt..."

# Step 2: Generate slides using template as reference
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01_title.png "slide 1 prompt..."
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02_pillars.png "slide 2 prompt..."
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_03_contact.png "slide 3 prompt..."
```

## Key Technique

The `-i template.png` flag passes the template as context to the model. The prompt then instructs it to maintain the template's visual style while adding the specific content for each slide. This ensures:

- Consistent color palette
- Matching layout structure
- Unified design elements (logo, accent bars, lines)
- Cohesive brand appearance across all slides
