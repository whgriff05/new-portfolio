# Agent Directives (`AGENTS.md`)

This document provides instructions, context, and operational rules for AI agents working in this repository.

---

## 1. Project Overview & Context
- **Purpose**: Personal portfolio website displaying personal projects, writing/blog posts, resume, and contact details.
- **Architecture**: Static site generation / SSG pattern. Content is driven by structured data files (Markdown + TOML frontmatter) and rendered via templates.
- **Design Philosophy**: Minimalist, fast-loading, clean typography, responsive across mobile/desktop, and privacy-conscious.

---

## 2. Tech Stack & Tools
- **Core Languages**: Python / HTML5 / CSS / JavaScript
- **Templates / Markup**: Jinja2 / Markdown
- **Style / Layout**: CSS (Flexbox, CSS Custom Properties for themes)

---

## 3. Directory Structure
```text
.
├── public/             # The built HTML/CSS/image files
├── site/               # The TOML files for page content
├── static/             # The CSS and image files (static files) for page content
└── templates/          # The HTML jinja templates for page construction
```

### Other useful files/things
- `build.py`            # The build script (run `./build.py`)
- `structure.md`        # How a TOML page is structured

## 4. Coding and Development Guidelines

### HTML and Templates
- Keep HTML semantic (`<main>`, `<article>`, ...)
- Ensure all HTML templates extend `base.html`
- Keep structural logic inside Jinja templates clean; avoid heavy computational logic in markup

### CSS Styling
- Use the color scheme defined in `:root`
- Avoid adding third party CSS frameworks 
- Avoid one-off solutions: for certain things that need to be reused (bold/underline/italic/colored spans, heading sizes, etc) create classes that can be added at will to HTML tags in TOML page files

## 5. Agent Rules of Engagement
1. Span of jurisdiction: You are only to work with CSS and HTML template files, as your job is to style my site, not generate or create content.
2. Incremental Edits: When editing, introduce minimal targeted changes, and do not re-architect anything without explicit instruction.
3. No Unused Dependencies: Keep external libraries and packages to absolute minimums, and standard library content is preferred.
