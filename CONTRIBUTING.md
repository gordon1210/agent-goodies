# Contributing

Thanks for helping improve Agent Goodies.

## Before opening a pull request

1. Read [AGENTS.md](AGENTS.md) for the repository's portability and packaging
   rules.
2. Keep shared skills provider-neutral. Put host-specific behavior in the
   corresponding manifest or configuration.
3. Keep multi-skill plugins self-contained under `plugins/<plugin-name>/` and
   standalone skills under `skills/<skill-name>/`.
4. Add a package independently to each marketplace that supports its layout.
5. Run:

   ```bash
   python3 scripts/validate_repo.py
   python3 -m unittest tests/test_handoff.py -v
   ```

6. If Claude Code is installed, also run:

   ```bash
   claude plugin validate ./plugins/<plugin-name>
   claude plugin validate .
   ```

Keep pull requests focused and explain any user-visible behavior change. Do not
include secrets, generated caches, or machine-specific paths.

## Changing a released plugin

Use semantic versioning. Update both host manifests and the plugin's
`CHANGELOG.md` together when preparing a release. Maintainers create the tag and
GitHub Release after the change reaches `main`; contributors should not create
or move release tags.

See [RELEASING.md](RELEASING.md) for the complete release process.
