# Agent Instructions

Work lives in hosted issues. Use `ccore tracker` with `owner/repo#N` references.

## Quick Reference

```bash
ccore tracker resolve --repo sussdorff/nanobanana
ccore tracker show sussdorff/nanobanana#<number>
```

## Session Completion

The assigned delivery owner completes verification, review, publication and the
merge decision. Report the pull request, merge state, verification result and
any project-specific postconditions. Preserve existing authorization for the
same concrete scope. Publication awaiting review is not terminal completion.
