---
name: nanobanana
description: >
  Generate and edit images using nanobanana CLI with Gemini or OpenRouter API.
  Use for creating images, slides, dashboards, wireframes, moodboards, icons,
  architecture diagrams, and visual content from text prompts.
  Triggers on "generate image", "nanobanana", "design mockup", "UI variations",
  "dashboard mockup", "moodboard", "wireframe", "slide generation",
  "social media image", "app icon", "architecture diagram".
dependencies: nanobanana (uv tool install nanobanana)
---

# Nanobanana Image Generation Skill

Generate images using Google's Gemini API via the nanobanana CLI tool.
Supports free-form prompts and structured subcommands with optimized prompt templates.

## Prerequisites

1. Install nanobanana:
   ```bash
   uv tool install nanobanana
   ```
   To upgrade: `uv tool upgrade nanobanana`

2. Set your API key (one of):
   ```bash
   # Option A: Gemini API (direct)
   export GEMINI_API_KEY="your-api-key"
   # Get a key at: https://aistudio.google.com/apikey

   # Option B: OpenRouter
   export OPENROUTER_API_KEY="your-api-key"
   # Get a key at: https://openrouter.ai/keys
   ```

3. Optional config file at `~/.config/nanobanana/config.json`:
   ```json
   {
     "api": "openrouter",
     "model": "google/gemini-3-pro-image-preview",
     "aspect": "16:9",
     "size": "2K",
     "key_command": "op read 'op://API Keys/OpenRouter - nanobanana/credential'"
   }
   ```
   The `key_command` field runs a shell command to retrieve the API key dynamically (e.g., from 1Password). Env vars take priority over key_command.

## When to Use This Skill

Use this skill when the user asks to:
- Generate images from text descriptions
- Create presentation slides, dashboards, or wireframes
- Design moodboards, icons, or architecture diagrams
- Explore design variations for a concept
- Create social media images
- Edit or transform existing images
- Combine multiple images
- Create consistent branded visuals using templates

## Subcommands

Each subcommand wraps the user's prompt in an optimized template with sensible defaults.

### Design Exploration

| Command | Description | Default Aspect | Default Size |
|---------|-------------|----------------|--------------|
| `dashboard` | KPI/analytics dashboard mockup | 16:9 | 2K |
| `moodboard` | Website/app moodboard collage | 1:1 | 2K |
| `explore` | Same concept in 4 style variations (2x2 grid) | 1:1 | 2K |
| `wireframe` | UI wireframe or screen layout | 16:9 | 2K |

### Content Creation

| Command | Description | Default Aspect | Default Size |
|---------|-------------|----------------|--------------|
| `slide` | Presentation slide | 16:9 | 2K |
| `social` | Social media post image | 1:1 | 2K |
| `icon` | App icon | 1:1 | 1K |
| `architecture` | System/cloud architecture diagram | 16:9 | 2K |

### Base

| Command | Description |
|---------|-------------|
| `generate` | Free-form prompt (explicit version of default) |

If the first argument is not a known command, it is treated as a free-form prompt (backwards compatible).

## Prompt Template Structure

Each subcommand wraps the user's prompt in a structured block format:

```
TASK
What to create (command-specific)

SOURCE MATERIAL
{user's prompt injected here}

STYLE
Visual treatment guidelines (command-specific)

LAYOUT
Composition and arrangement rules (command-specific)

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution
```

The `generate` command passes the user's prompt through without wrapping.

## Usage Examples

### Subcommands
```bash
# Dashboard mockup (16:9, 2K by default)
nanobanana dashboard "SaaS metrics with MRR, churn rate, and user growth"

# Presentation slide
nanobanana slide "Q4 revenue highlights: 40% YoY growth, 3 new enterprise clients"

# App icon
nanobanana icon "podcast app with microphone and sound waves"

# Architecture diagram
nanobanana architecture "microservices with API gateway, 3 services, Redis cache, PostgreSQL"

# Design exploration (4 style variations)
nanobanana explore "landing page hero for a meditation app"

# Moodboard
nanobanana moodboard "fintech app targeting young professionals"

# Wireframe
nanobanana wireframe "settings page with account, notifications, and billing"

# Social media post
nanobanana social "product launch announcement for an AI writing tool"

# Override command defaults
nanobanana dashboard -size 4K "quarterly revenue breakdown"
nanobanana social -aspect 9:16 "instagram story for product launch"
```

### Free-form Generation
```bash
nanobanana "a cute cat sitting on a windowsill"
nanobanana -o output.jpg "a sunset over mountains"
nanobanana -aspect 16:9 -size 2K -o slide.jpg "cinematic landscape"
```

### Image Editing (with input image)
```bash
nanobanana -i input.jpg "transform into watercolor style"
nanobanana -i photo.jpg "add sunglasses to the person"
```

### Multi-Image Composition
```bash
nanobanana -i background.jpg -i subject.jpg "place the subject in the scene"
nanobanana -i template.jpg -i content.jpg "apply the template style"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable) | none |
| `-o <file>` | Output filename | auto-generated |
| `-aspect <ratio>` | Aspect ratio (overrides command default) | `1:1` |
| `-size <size>` | Image size (1K, 2K, 4K) | `1K` |
| `-model <model>` | OpenRouter model (enables OpenRouter) | `google/gemini-3-pro-image-preview` |
| `-h` | Show help | - |
| `-version` | Show version | - |

### Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Workflow Patterns

### Presentation Slides (Consistent Style)
```bash
# 1. Generate a template first
nanobanana slide -o template.jpg \
  "presentation slide template with dark blue gradient, modern minimal style"

# 2. Generate each slide using template as style reference
nanobanana -i template.jpg slide -o slide_01.jpg "title slide for Project Alpha"
nanobanana -i template.jpg slide -o slide_02.jpg "slide showing three key features"
```

### Design Exploration to Final
```bash
# 1. Explore styles
nanobanana explore "landing page hero for SaaS analytics product"

# 2. Pick a direction, refine with specific command
nanobanana dashboard "SaaS analytics with conversion funnel, MRR trend, top segments"
```

## API Details

- **Model**: `gemini-3-pro-image-preview`
- **Backends**: Gemini API (direct) or OpenRouter
- **Timeout**: 120 seconds

## Pricing

- 1K-2K images: ~$0.13 per image
- 4K images: ~$0.24 per image

## Troubleshooting

- **No API key**: Set `GEMINI_API_KEY` or `OPENROUTER_API_KEY` environment variable
- **Wrong file extension**: nanobanana auto-corrects to match actual format (usually .jpg)
- **Image too large**: Use smaller `-size` option (1K instead of 4K)
- **Command not recognized**: Check `nanobanana help` for available commands

## More Information

- Repository: https://github.com/skorfmann/nanobanana
- Examples: https://github.com/skorfmann/nanobanana/tree/main/examples
- Command help: `nanobanana help <command>`
