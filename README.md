# Data Science Notes

This is a set of lecture notes for CSCI 1010: Applied Data Science at Middlebury College. This repository powers a [website](https://middcs.github.io/data-science-notes/) which serves as the primary text for the course. 

This README describes how the site works and how to add/modify content. Please note that this process was created and implemented by Phil, and has a LOT of room for improvement! I'd love to collaborate on tidying things up. 

## Big Picture

Content is housed in Quarto Markdown `.qmd` files in the `source` directory. These content files are processed into the `chapters` directory, which is then rendered into a website in the `docs` directory. *Simultaneously*, the same files are converted into Jupyter Notebooks in the `docs/live-notebooks` directory. The purpose of these notebooks is to be served via Google Colab. Links to the Colab versions of the notebooks are interpolated in the `html` content files after rendering. Authors can specify blocks of code to be removed from the live versions in order to facilitate live-coding. 

*Room for improvement*: there is some crud (like YAML metadata) that is also converted into the live notebooks that could ideally be removed. 

## Setup

First, install [Quarto](https://quarto.org/docs/get-started/). 

Next, instantiate a new virtual environment (Python 3.10 is fine) with required packages: 

```bash
python -m venv env
source env/bin/activate  
pip install -r requirements.txt
```

*Room for improvement*: Phil is open to running this through Anaconda instead. 

## Workflow

### Create a Chapter 

To create a chapter, create a new `.qmd` file in the `source` directory. You can copy and paste from existing files to get started. The YAML metadata must include `jupyter: python3` for code-chunk execution; other metadata is flexible. Example:

```yaml
---
code-fold: true
code-summary: "Show code"
jupyter: python3
---
```

When naming the file, I like to use a two-digit prefix to handle file ordering, acknowledging that the order may eventually diverge from the filenames.

Next, add the chapter to the files `_quarto-preview.yml` and `_quarto-publish.yml` in your desired location. Note that in the file `_quarto-preview.yml`, the paths to the chapter files should be prefixed with `source/`, while in `_quarto-publish.yml`, they should be prefixed with `chapters/`.

### Preview 

To preview the site locally, first run 

```bash
source env/bin/activate
```

Then, run

```bash
quarto preview --profile preview
```

in the command line. Alternatively, `make preview` will do the same thing.

### Publish

There are several steps to publish updates. The site build involves activating the virtual environment with 

```bash
source env/bin/activate
```

and then has four steps: 

```bash
python3 scripts/prep-qmd.py
quarto render --profile publish
python3 scripts/create-ipynb.py
python3 scripts/insert-colab-link.py
```

Once these commands have been run, the entire directory (except for excluded files) should be committed and pushed to GitHub. The website is hosted via GitHub Pages from the `docs` directory.

Alternatively, if one does not mind poor version control hygiene, `make publish` will automate the above four steps plus a git commit/push with an uninformative commit message. 