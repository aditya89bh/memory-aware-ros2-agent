# Release Checklist

Use this checklist before publishing a release.

## Validation

- [ ] `pytest`
- [ ] `ruff check .`
- [ ] `mypy src`
- [ ] `python -m build`
- [ ] `git status`

## Documentation

- [ ] README is current.
- [ ] Architecture docs reflect the released scope.
- [ ] Changelog includes the release version and date.

## Repository

- [ ] CI is passing on supported Python versions.
- [ ] Release tag matches the package version.
- [ ] GitHub release notes summarize user-facing changes.
