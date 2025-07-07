# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website repository for `django-vditor`, a Markdown Editor plugin application for Django based on the vditor editor. The repository contains a simple GitHub Pages site that serves as the project's homepage.

## Repository Structure

This is a minimal static website repository with:
- `index.html` - Main landing page showcasing the django-vditor project
- `CNAME` - Custom domain configuration for GitHub Pages (django-vditor.pi-dal.com)

## Architecture

This is a **GitHub Pages repository** (on the `gh-pages` branch) that hosts a static promotional website. The site is built with:
- Pure HTML with Tailwind CSS for styling
- No build process or dependencies
- Hosted on GitHub Pages with custom domain

## Development Notes

- This repository contains only static web assets for the project homepage
- The actual `django-vditor` Python package is maintained in a separate repository
- Changes to `index.html` are immediately reflected on the live site
- The site uses CDN-hosted Tailwind CSS (v2.0.3) for styling
- All content is in Chinese (zh-cmn-Hans) as indicated by the HTML lang attribute

## Key Files

- `index.html` - The complete website in a single HTML file
- `CNAME` - GitHub Pages custom domain configuration

## Common Tasks

Since this is a static site with no build process:
- **Edit content**: Modify `index.html` directly
- **Preview changes**: Open `index.html` in a browser locally
- **Deploy**: Push changes to the `gh-pages` branch (auto-deploys via GitHub Pages)

## Branch Information

- Main development branch: `gh-pages` (this serves the live site)
- The `main` branch may contain source code for the actual django-vditor package