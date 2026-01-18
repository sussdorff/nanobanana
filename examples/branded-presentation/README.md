# Branded Presentation Example

Demonstrates using a template image as a style reference to maintain visual consistency across slides.

## Key Technique

Generate a template first, then pass it with `-i` to each slide generation. This ensures consistent:
- Color palette (dark navy + electric cyan)
- Layout structure (accent bar, logo placement)
- Design elements (lines, geometric shapes)
- Overall brand aesthetic

## Files

| File | Description |
|------|-------------|
| `template.png` | Base style template (no content) |
| `presentation.md` | Full documentation with prompts |
| `slide_01_title.png` | "NEXUS AI" title slide |
| `slide_02_pillars.png` | Three pillars: Analyze, Automate, Accelerate |
| `slide_03_contact.png` | Contact/closing slide |

## Generated Slides

### Template (Style Reference)
![Template](template.png)

### Slide 1: Title
![Title](slide_01_title.png)

### Slide 2: Three Pillars
![Pillars](slide_02_pillars.png)

### Slide 3: Contact
![Contact](slide_03_contact.png)

## Commands

```bash
# 1. Generate template
./nanobanana -aspect 16:9 -size 2K -o template.png \
  "A presentation slide template with dark navy blue background..."

# 2. Generate slides using template as reference
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01_title.png \
  "Using this template style exactly, create a title slide..."

./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02_pillars.png \
  "Using this template style exactly, create a slide showing three columns..."

./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_03_contact.png \
  "Using this template style exactly, create a closing slide..."
```

## Workflow for Claude Code

1. Read `presentation.md` for slide descriptions
2. Generate template first (if not exists)
3. For each slide, run nanobanana with `-i template.png` and the slide-specific prompt
