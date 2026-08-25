# Public Codex packaging follow-up

zforge currently optimizes for its documented local installation paths: Claude Code loads the repository root with `--plugin-dir`, and Codex installs the repository from its local marketplace. To keep those two hosts from discovering duplicate workflow surfaces, the local Codex manifest loads the shared `skills/` root together with the Codex-only `codex/skills/` root.

That layout is intentionally not a public-directory packaging contract. OpenAI's public plugin validation currently requires `skills` to be a single string that resolves to the plugin's top-level `skills/` directory, requires every skill to be an immediate real child of that directory, and ignores skill-directory symlinks. See the official [plugin packaging guide](https://developers.openai.com/plugins/build/plugins) and [submission errors](https://developers.openai.com/plugins/deploy/submission-errors).

If zforge is prepared for public Codex distribution later, add a build step that assembles a disposable package rather than changing the source layout:

1. Create a clean distribution root with `.codex-plugin/plugin.json` and one top-level `skills/` directory.
2. Copy the four shared skills and the nine Codex-only skills into that directory as real child directories.
3. Include every template and reference used by those skills, rewriting package-relative links only in the generated output when necessary.
4. Validate the assembled package against the current public ingestion contract and smoke-test it as an installed plugin.
5. Keep the generated package out of the source-of-truth workflow so Claude and Codex authoring surfaces cannot drift from generated copies.

Until that build exists, the repository should describe Codex support as local-marketplace compatibility tested with Codex CLI 0.149.1, not as public-directory compatibility.
