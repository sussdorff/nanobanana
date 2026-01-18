# Presentation Slide Generation

This example demonstrates using Claude Code to read a markdown presentation and generate slide images with nanobanana.

## Files

| File | Description |
|------|-------------|
| `presentation.md` | Source markdown with slide descriptions and prompts |
| `slide_01_title.png` | Generated title slide |
| `slide_02_features.png` | Generated features slide |
| `slide_03_cta.png` | Generated call-to-action slide |

## Generated Slides

### Slide 1: Title
![Title Slide](slide_01_title.png)

### Slide 2: Features
![Features Slide](slide_02_features.png)

### Slide 3: Call to Action
![CTA Slide](slide_03_cta.png)

## Workflow

1. Write slide descriptions in `presentation.md`
2. Claude Code reads the markdown and extracts prompts
3. Each slide is generated with nanobanana:

```bash
./nanobanana -aspect 16:9 -size 2K -o slide_01_title.png "prompt..."
./nanobanana -aspect 16:9 -size 2K -o slide_02_features.png "prompt..."
./nanobanana -aspect 16:9 -size 2K -o slide_03_cta.png "prompt..."
```

## Parameters

- **Aspect ratio:** 16:9 (widescreen presentation format)
- **Size:** 2K (high resolution for presentations)
