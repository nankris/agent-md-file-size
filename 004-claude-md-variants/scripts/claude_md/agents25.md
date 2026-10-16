# Project notes
This folder is a small JavaScript package (Node 18+, no dependencies, CommonJS).

## Layout
- `broken.js` — the module under test. All fixes go here.
- `test.js` — plain `assert` tests. Never edit it.
- Other `.js`/`.csv` files are fixtures or helpers.

## Commands
- Test: `node test.js` (exit 0 and prints OK on success).
- No build step, no linter, no package.json.

## Conventions
- 2-space indent, double quotes, semicolons.
- Keep exports unchanged (`module.exports = { … }`).
- Prefer the minimal fix; don't rename functions.

## Workflow
1. Run `node test.js` to see the failure.
2. Read `broken.js`.
3. Fix it with a small edit.
4. Run `node test.js` again.
5. Reply with one sentence describing the fix.
