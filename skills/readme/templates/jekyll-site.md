# Jekyll Static Site README Template

Use this template for Jekyll-based static sites (GitHub Pages, blogs, personal sites).

```markdown
# {site-name}

[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]

> One-line description of the site.

## Overview

Brief description of what this site is about.

## Tech Stack

- **Jekyll** - Static site generator
- **Theme** - [Theme Name](link-to-theme)
- **Hosted on** - GitHub Pages / Netlify / Other

## Local Development

### Prerequisites

- Ruby 2.7+
- Bundler
- Jekyll

### Setup

\`\`\`bash
# Install dependencies
bundle install

# Run locally
bundle exec jekyll serve

# With live reload
bundle exec jekyll serve --livereload
\`\`\`

Access at: http://localhost:4000

## Project Structure

\`\`\`
{site-name}/
├── _config.yml       # Site configuration
├── _posts/           # Blog posts
├── _pages/           # Static pages
├── _layouts/         # Page templates
├── _includes/        # Reusable components
├── _sass/            # Stylesheets
├── assets/           # Images, fonts, etc.
└── index.html        # Homepage
\`\`\`

## Configuration

### Site Settings

Edit `_config.yml`:

\`\`\`yaml
title: Your Site Title
description: Site description
author: Your Name
url: "https://yoursite.com"
\`\`\`

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `JEKYLL_ENV` | Set to `production` for builds |

## Content Management

### Creating a Post

\`\`\`bash
# Create new post
_posts/YYYY-MM-DD-title.md
\`\`\`

### Creating a Page

\`\`\`bash
# Create new page
_pages/page-name.md
\`\`\`

### Front Matter

\`\`\`yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
categories: [category1]
tags: [tag1, tag2]
---
\`\`\`

## Deployment

### GitHub Pages

Push to `main` branch. Site automatically deploys.

Settings → Pages → Source: `main` branch

### Manual Build

\`\`\`bash
# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Output in _site/
\`\`\`

### Netlify

Connect repository, set build command:
- Build: `jekyll build`
- Publish: `_site`

## Customization

### Theme

This site uses [Theme Name]. Customize by:

1. Override layouts in `_layouts/`
2. Override includes in `_includes/`
3. Custom styles in `_sass/`

### Plugins

| Plugin | Purpose |
|--------|---------|
| `jekyll-seo-tag` | SEO metadata |
| `jekyll-sitemap` | Generate sitemap |

## Contributing

1. Fork the repository
2. Create a branch
3. Make changes
4. Submit pull request

## License

Content is licensed under [License Type].

Site code is [MIT](LICENSE).

[license]: LICENSE
```

## Badge Reference

For Jekyll sites:

| Badge | Markdown |
|-------|----------|
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |

**Optional badges**:
- GitHub Pages: `https://img.shields.io/github/deployments/{user}/{repo}/github-pages`

## Section Guidelines

- **Tech Stack**: Mention Jekyll version and theme
- **Local Development**: Ruby/Bundler setup instructions
- **Project Structure**: Jekyll-specific directories
- **Content Management**: How to add posts/pages
- **Deployment**: GitHub Pages is most common
- **Customization**: How to override theme defaults