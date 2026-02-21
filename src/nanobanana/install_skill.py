"""Install the nanobanana Claude Code skill to ~/.claude/skills/."""

import shutil
from importlib.resources import files
from pathlib import Path


def install_skill(claude_dir: str | None = None) -> None:
    """Copy bundled skill files to the Claude Code skills directory."""
    claude_path = Path(claude_dir) if claude_dir else Path.home() / ".claude"
    target = claude_path / "skills" / "nanobanana"

    if not claude_path.exists():
        print(f"Claude Code directory not found: {claude_path}")
        print("Install Claude Code first, then re-run this command.")
        print(f"Or specify a custom path: nanobanana install-skill --claude-dir <path>")
        return

    # Locate skill files: bundled in package, or repo source directory
    skill_pkg = files("nanobanana") / "skill"
    skill_dir = Path(str(skill_pkg))

    if not skill_dir.exists():
        # Fallback: check if we're in the repo (editable install)
        repo_skill = Path(__file__).parent.parent.parent / "skill" / "nanobanana"
        if repo_skill.exists():
            skill_dir = repo_skill
        else:
            raise RuntimeError(
                "Bundled skill files not found. "
                "Re-install with: uv tool install nanobanana-cli"
            )

    # Copy skill files
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_dir, target)
    print(f"Skill installed to {target}")
