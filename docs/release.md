# Release Process

Nanobanana uses [CalVer](https://calver.org/) versioning (`YYYY.0M.MICRO`) and releases are triggered by pushing a git tag.

## Versioning Scheme

- Format: `YYYY.0M.MICRO` (e.g., `2026.02.0`, `2026.02.1`)
- Same month: increment MICRO (`2026.02.0` -> `2026.02.1` -> `2026.02.2`)
- New month: reset MICRO to 0 (`2026.02.3` -> `2026.03.0`)
- Tags are prefixed with `v`: `v2026.02.0`

## Release via /session-close

The primary way to release is through the global `/session-close` skill in Claude Code:

1. Work on features/fixes with conventional commit messages
2. Run `/session-close` when done
3. The skill will:
   - Close relevant beads
   - Commit pending changes
   - Generate/update CHANGELOG.md via `git cliff`
   - Determine the next CalVer version
   - Create and push the tag
4. GitHub Actions handles the rest (test, build, publish to PyPI, create GitHub Release)

## Manual Release (Fallback)

If you need to release manually:

```bash
# 1. Ensure all changes are committed
git status

# 2. Determine next version
# Same month as last tag: increment MICRO
# New month: reset MICRO to 0
git tag --list "v*" --sort=-v:refname | head -1

# 3. Update CHANGELOG.md
git cliff --tag v2026.02.0 --output CHANGELOG.md
git add CHANGELOG.md
git commit -m "chore: update changelog for v2026.02.0"

# 4. Create and push tag
git tag v2026.02.0
git push origin main --tags
```

## What the CI Does

When a tag matching `v[0-9]*` is pushed, the GitHub Actions workflow:

1. **Test job**: Runs `uv run pytest -v`
2. **Publish job** (after tests pass):
   - Extracts version from the tag name (strips `v` prefix)
   - Stamps version into `pyproject.toml`
   - Builds the package with `uv build`
   - Publishes to PyPI via trusted publishing
   - Generates release notes from changelog
   - Creates a GitHub Release

## Changelog Generation

The changelog is managed by [git-cliff](https://git-cliff.org/) using `cliff.toml`:

- Only conventional commits are included (`feat:`, `fix:`, `refactor:`, etc.)
- Commits are grouped by type: Added, Fixed, Changed, Documentation, Maintenance
- Scoped commits show their scope in bold (e.g., `**cli**: Add new flag`)

To preview unreleased changes:

```bash
git cliff --unreleased
```

## Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new image format support
fix: handle missing config gracefully
refactor: simplify API client initialization
docs: update CLI usage examples
chore: update dependencies
```

Optional scope:

```
feat(cli): add --quality flag
fix(gemini): retry on rate limit
```
