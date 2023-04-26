---
tags:
    - DIY
    - docs
    - mkdocs
    - website
    - python

---

# How to build these docs

Suppose you've already got a python package going, using for example [a package manager like `poetry`](https://python-poetry.org/).

What you're going to do next is this:

```bash
poetry add --group dev mkdocs mkdocs-material mkdocs-material pillow cairosvg mike mkdocs-glightbox flake8 pytest
```

## The config.yaml file

Now you should do `mkdocs init .` which will create a `docs/` folder and a config file.

This is what your config file should look like:

```yaml

site_name: Typer-TinyDB # package & website name
site_url: https://arnos-stuff.github.io/typer-tinydb/  # to avoid collisions with other repos
repo_url: https://github.com/arnos-stuff/typer-tinydb/
repo_name: typer-tinydb # repo name

plugins:
  - social
  - tags

site_dir: site/typer-tinydb/ # nesting this allows you to ensure you don't use the root of the github.io site.


extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/twitter #socials
      link: https://twitter.com/arno_shae
    - icon: fontawesome/brands/python #socials
      link: https://pypi.org/user/arnos-stuff/
    - icon: fontawesome/brands/docker #socials
      link: https://hub.docker.com/u/arnoveldock
    - icon: fontawesome/brands/discord #socials
      link: https://discord.com/users/724287271364198520

markdown_extensions:
  - markdown.extensions.abbr
  - markdown.extensions.admonition
  - markdown.extensions.attr_list
  - markdown.extensions.md_in_html
  - pymdownx.highlight:
      anchor_linenums: true
      linenums: true
      use_pygments: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - toc:
      permalink: true
  - tables

nav:
    - Home: index.md
    - Commands: commands.md
    - Other Library Utils: other-utils.md
    - Contributing: future-work.md
    - Tags: tags.md
    - About: about.md
theme:
  name: material
  font:
    text: Fira Sans
    code: Fira Code
  logo: assets/Wide-Logo-SM.svg
  favicon: assets/blob48.png
  features:
    - navigation.footer

  palette:
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: deep purple
      accent: pink
      toggle:
        icon: material/palette-swatch-outline
        name: Default Theme
    # Palette toggle for dark mode
    - scheme: slate
      primary: indigo
      accent: teal
      toggle:
        icon: material/format-color-fill
        name: Switch to light mode
    - media: "(prefers-color-scheme: dark)"
      toggle:
        icon: material/brightness-auto
        name: Switch to light mode
    # Palette toggle for light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default 
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
```

# Versioning your docs

When you only have a simple app and care little about versioning, you can just go ahead and manually do

```bash
mkdocs build
mkdocs gh-deploy
```

But if you want to have versioning on your blog info, you **have to know** these two:

```bash
mike deploy --push --update-aliases 0.1.5 latest
mike set-default 0.1.5
```

Which makes you increment & publish at the same time from 0.1.4 to 0.1.5, obviously the next shot is going to be

```bash
mike deploy --push --update-aliases 0.1.6 latest
mike set-default 0.1.6
```

Unless 0.1.6 isn't stable.

# Autodoc from docstrings

An advice is to also add the helpful little package here:

```bash
poetry add --group dev mkgendocs
```

You set up your `mkgendocs.yml` file similarly to what's shown on the [author's github repo](https://github.com/davidenunes/mkgendocs), and you should run in order:

1) the gendocs command `gendocs --config mkgendocs.yml` to get the YAML docs
2) adjust the `mkdocs.yml` if needed in terms of paths
3) Run `mkdocs build` (and possibly `mkdocs serve`)
4) Publish using [mike](https://github.com/jimporter/mike)


## Addendum

Here's my YAML config file for gendocs:

```YAML
sources_dir: docs/sources
templates_dir: docs/reference
repo: https://github.com/arnos-stuff/typer-tinydb #link to sources on github
version: master #link to sources on github

pages:
- page: "getters.md"
  source: "typer_tinydb/utils.py"
  functions:
  - getUserTable
  - ugetKey
  - getKey
  - ugetValue
  - getValue
- page: "setters.md"
  source: 'typer_tinydb/utils.py'
  functions:
  - upsert_param
  - upsert_param_udb
  - create_table
- page: "renderers.md"
  source: 'typer_tinydb/utils.py'
  functions:
  - 'renderQuery'
  - 'tabCallback'
  - 'renderAllTables'

# creates an index page based on everything from target source
- page: "refs.md"
  source: "typer_tinydb/utils.py"
  index: True
```