# Nanobanana Presentation

A sample presentation to demonstrate using Claude Code with nanobanana to generate slide images.

---

## Slide 1: Title Slide

**Visual Description:**
A bold, modern title slide with "Nanobanana" as the main text. Background features a gradient from yellow to orange with subtle banana illustrations. Clean, tech-startup aesthetic. Minimalist design with plenty of whitespace.

**Prompt for nanobanana:**
```
nanobanana -aspect 16:9 -size 2K -o examples/slide_01_title.png "A modern presentation title slide with the word 'Nanobanana' in bold white sans-serif font, centered. Background is a smooth gradient from golden yellow to warm orange. Subtle decorative banana shapes in the corners. Clean, professional tech startup aesthetic. Minimalist design."
```

---

## Slide 2: Features

**Visual Description:**
An infographic-style slide showing three key features: Generate, Edit, Compose. Each feature represented by a simple icon. Clean grid layout with icons on the left and space for text on the right. Light background with accent colors.

**Prompt for nanobanana:**
```
nanobanana -aspect 16:9 -size 2K -o examples/slide_02_features.png "A clean infographic presentation slide with three rows showing features. Row 1: sparkle icon with 'Generate' text. Row 2: magic wand icon with 'Edit' text. Row 3: layers icon with 'Compose' text. Light gray background, modern flat design icons in yellow and orange. Professional business presentation style."
```

---

## Slide 3: Call to Action

**Visual Description:**
A closing slide with "Get Started" as the main message. Features a terminal/command line aesthetic showing the basic usage command. Dark background (terminal-like) with green or yellow text. Includes a friendly banana mascot character in the corner.

**Prompt for nanobanana:**
```
nanobanana -aspect 16:9 -size 2K -o examples/slide_03_cta.png "A presentation closing slide with dark charcoal background resembling a terminal. Large text says 'Get Started' in bright green monospace font. Below it shows a command: ./nanobanana 'your prompt'. A small cute cartoon banana mascot character waves from the bottom right corner. Retro tech aesthetic."
```

---

## How to Generate These Slides

Run these commands to generate the slide images:

```bash
cd /path/to/nanobanana

# Slide 1: Title
./nanobanana -aspect 16:9 -size 2K -o examples/slide_01_title.png "A modern presentation title slide with the word 'Nanobanana' in bold white sans-serif font, centered. Background is a smooth gradient from golden yellow to warm orange. Subtle decorative banana shapes in the corners. Clean, professional tech startup aesthetic. Minimalist design."

# Slide 2: Features
./nanobanana -aspect 16:9 -size 2K -o examples/slide_02_features.png "A clean infographic presentation slide with three rows showing features. Row 1: sparkle icon with 'Generate' text. Row 2: magic wand icon with 'Edit' text. Row 3: layers icon with 'Compose' text. Light gray background, modern flat design icons in yellow and orange. Professional business presentation style."

# Slide 3: Call to Action
./nanobanana -aspect 16:9 -size 2K -o examples/slide_03_cta.png "A presentation closing slide with dark charcoal background resembling a terminal. Large text says 'Get Started' in bright green monospace font. Below it shows a command: ./nanobanana 'your prompt'. A small cute cartoon banana mascot character waves from the bottom right corner. Retro tech aesthetic."
```
