# Nanobanana Skill for Claude

This folder contains a [Claude Skill](https://support.anthropic.com/en/articles/11175166-what-are-skills-and-how-do-i-use-them) for using nanobanana with Claude Code and Claude.ai.

## Installation

### Claude Code

Copy the `nanobanana` folder to your Claude Code skills directory, or reference it directly.

### Claude.ai (Pro/Max/Team/Enterprise)

1. Zip the `nanobanana` folder:
   ```bash
   cd skill
   zip -r nanobanana.zip nanobanana
   ```

2. Upload to Claude.ai:
   - Go to **Settings** → **Skills**
   - Click **Upload Skill**
   - Select `nanobanana.zip`

3. Enable the skill in your conversation settings.

## What This Skill Does

When enabled, Claude will automatically use nanobanana to:

- Generate images from text descriptions
- Create presentation slides with consistent styling
- Edit and transform existing images
- Design banners, thumbnails, and social media graphics

## Example Usage

Just ask Claude naturally:

- "Create a hero image for my landing page about AI productivity tools"
- "Generate a 3-slide presentation about our Q4 results"
- "Make a social media banner for our product launch"
- "Edit this image to add a sunset in the background"

Claude will use nanobanana with appropriate settings and prompts.

## Prerequisites

Before using this skill, ensure:

1. nanobanana is installed:
   ```bash
   brew tap skorfmann/nanobanana
   brew install nanobanana
   ```

2. `GEMINI_API_KEY` environment variable is set:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

Get an API key at: https://aistudio.google.com/apikey
