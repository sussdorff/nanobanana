# Nanobanana

A lightweight CLI tool for generating and editing images using Google's Gemini API.

## Features

- **Text-to-image generation** - Create images from text prompts
- **Image editing** - Transform existing images with text instructions
- **Multi-image composition** - Combine multiple input images
- **Flexible output** - 9 aspect ratios and 3 size options

## Requirements

- Go 1.25+ (for building from source)
- Google Gemini API key with access to `gemini-3-pro-image-preview`

## Installation

### From GitHub Releases

Download the latest binary for your platform from the [Releases](../../releases) page.

```bash
# Example for macOS arm64
curl -L -o nanobanana https://github.com/<owner>/nanobanana/releases/latest/download/nanobanana-darwin-arm64
chmod +x nanobanana
./nanobanana -version
```

### From source

```bash
git clone <repository-url>
cd nanobanana
go build -o nanobanana main.go
```

## Setup

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

```bash
nanobanana [options] "prompt"
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable for multiple images) | none |
| `-o <file>` | Output filename | `image_YYYYMMDD_HHMMSS.png` |
| `-aspect <ratio>` | Aspect ratio | `1:1` |
| `-size <size>` | Image size | `1K` |
| `-h` | Show help | - |
| `-version` | Show version | - |

### Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Supported Sizes

| Size | Resolution |
|------|------------|
| `1K` | ~1024px |
| `2K` | ~2048px |
| `4K` | ~4096px |

### Supported Image Formats

PNG, JPEG, WebP, GIF

## Examples

### Text-to-image

```bash
# Simple generation
nanobanana "a cute cat sitting on a windowsill"

# With aspect ratio and size
nanobanana -aspect 16:9 -size 2K "cinematic mountain landscape at sunset"

# Custom output filename
nanobanana -o hero-image.png "abstract geometric pattern"
```

### Image editing

```bash
# Style transfer
nanobanana -i photo.jpg "transform into watercolor painting"

# Modifications
nanobanana -i portrait.png "add sunglasses"
```

### Multi-image composition

```bash
# Combine images
nanobanana -i background.png -i subject.png "place the subject in the scene"

# Style reference
nanobanana -i content.jpg -i style.jpg "apply the style to the content image"
```

## Examples

The `examples/` folder contains working examples with generated images:

### basic/
Simple text-to-image generation.

```bash
./nanobanana -o basic_example.png "a friendly yellow banana character"
```

### presentation/
Generate presentation slides from text prompts.

```bash
./nanobanana -aspect 16:9 -size 2K -o slide_01.png "title slide prompt..."
./nanobanana -aspect 16:9 -size 2K -o slide_02.png "content slide prompt..."
```

### branded-presentation/
Use a template image as a style reference for consistent branding across slides.

```bash
# 1. Generate a style template first
./nanobanana -aspect 16:9 -size 2K -o template.png "slide template with brand colors..."

# 2. Generate slides using template as reference
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01.png "title slide..."
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02.png "content slide..."
```

Each example includes a README and the markdown source used to generate the images. See the `examples/` folder for full prompts and generated outputs.

## Using with Claude Code

Nanobanana works well with Claude Code for automated image generation workflows:

1. Describe slides/images in a markdown file
2. Claude Code reads the markdown and extracts prompts
3. Claude Code runs nanobanana to generate each image

See `examples/branded-presentation/` for a complete workflow demonstration.

## License

MIT
