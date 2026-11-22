# Repository Guidelines

## Project Structure & Module Organization

This repository is a small, dependency-free browser application. Its files are kept at the repository root:

- `index.html` defines the page structure and loads the other files.
- `style.css` contains layout, colors, and component styling.
- `script.js` implements the “My Little Library” interaction.

There are currently no separate source, asset, or test directories. Keep additions simple; introduce folders when assets or modules warrant them.

## Build, Test, and Development Commands

No package manager, build system, or automated test suite is configured. Open `index.html` directly in a browser to run the app. For a local HTTP preview, run `python -m http.server 8000` from this directory and visit `http://localhost:8000`.

After changes, reload the page and verify that it renders without browser-console errors and that **Add Book** appends a numbered item. Check layout at a narrow viewport when changing CSS.

## Coding Style & Naming Conventions

Use two spaces for indentation in HTML, CSS, and JavaScript. Keep browser code in the existing files, use semantic HTML, and prefer descriptive kebab-case IDs and classes (for example, `book-list`). Use `const` by default and `let` only for reassigned values. Keep CSS selectors focused and place related declarations together. No formatter or linter is currently configured.

## Testing Guidelines

There is no automated test framework or coverage requirement. Test behavior manually in a browser: load the page, click **Add Book** more than once, confirm numbering increments, and inspect the console for errors. If automated tests are introduced, document their command and keep them focused on observable UI behavior.

## Commit & Pull Request Guidelines

Recent commits use short, imperative subjects (for example, “Create README.md”); follow that style and keep each commit focused. Pull requests should explain the user-visible change, summarize relevant implementation details, and include manual verification steps. Add screenshots for visual changes and link a related issue when one exists.

## Security & Configuration

The app has no secrets or runtime configuration. Avoid adding credentials to source files; keep any future configuration or third-party dependency needs explicit in the change description.
