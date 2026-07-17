# Contributing

Thanks for helping improve Agent Goodies.

## Before opening a pull request

1. Read [AGENTS.md](AGENTS.md) for the repository's portability and packaging
   rules.
2. Keep shared skills provider-neutral. Put host-specific behavior in the
   corresponding manifest or configuration.
3. Keep each plugin self-contained under `plugins/<plugin-name>/`.
4. Add a plugin independently to each marketplace that should expose it.
5. Run:

   ```bash
   python3 scripts/validate_repo.py
   ```

6. If Claude Code is installed, also run:

   ```bash
   claude plugin validate ./plugins/<plugin-name>
   ```

Keep pull requests focused and explain any user-visible behavior change. Do not
include secrets, generated caches, or machine-specific paths.

## Changing a released plugin

Use semantic versioning. Update both host manifests and the plugin's
`CHANGELOG.md` together when preparing a release. Maintainers create the tag and
GitHub Release after the change reaches `main`; contributors should not create
or move release tags.

See [RELEASING.md](RELEASING.md) for the complete release process.
