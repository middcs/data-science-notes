#!/usr/bin/env python3
import argparse
import contextlib
import json
import os
import nbformat as nb
import re
import shutil
import subprocess
from dotenv import load_dotenv
from pathlib import Path

@contextlib.contextmanager
def temporary_softlink(target_path, link_path):
    """
    A context manager to create a temporary softlink.

    Args:
        target_path (str or Path): The destination the softlink should point to.
        link_path (str or Path): The location where the softlink should be created.
    """
    try:
        os.symlink(target_path, link_path)
        yield link_path # Yield control to the 'with' block
    finally:
        # Removed link on exit
        if os.path.islink(link_path):
            os.remove(link_path)

def create_notebook(src_path: Path, out_path: Path, site_url: str):
    """Create notebook from .qmd or .ipynb file, rendering qmd to remove quarto-specific content.

    Args:
        src_path (Path): Path to the source file (.qmd or .ipynb)
        out_path (Path): Path where the output notebook should be saved
        site_url (str): URL of the site for metadata

    Raises:
        ValueError: If the file type is unsupported
    """
    if src_path.suffix == ".qmd":
        # Use absolute paths to avoid issues when changing working directories
        with temporary_softlink(src_path.absolute(), src_path.with_name(f"_{src_path.name}").absolute()) as link_path:
            # Render to create notebook (instead of convert) to ensure any quarto-specific content is handled (stripped). The lua filter
            # removes solution blocks with '.hide .solution' classes.
            subprocess.run(
                ["quarto", "render", str(link_path), "--profile", "notebook", "--output", out_path.name, "--no-execute", "--to", "ipynb", "--metadata", f"site-url:{site_url}", "--lua-filter", f"{Path.cwd()}/scripts/remove-solution.lua"], 
                cwd=out_path.parent,
                check=True,
            )
    elif src_path.suffix == ".ipynb":
        shutil.copyfile(src_path, out_path)
    else:
        raise ValueError(f"Unsupported file type: {src_path.suffix}")

def clean_notebook(notebook_path):
    """Remove hidden content and outputs from a notebook_path ipynb file"""
    notebook = nb.read(notebook_path, as_version = 4)
    
    for cell in notebook["cells"]:
         # Remove code content designed to be hidden (markdown solution blocks are handled in lua filter during rendering)
        message = "# TODO" if cell["cell_type"] == "code" else "*[TODO]*"
        cell["source"] = re.sub(r"#---[\S\s]*?#---", message, cell["source"])

        # Delete quarto metadata on individual cells
        cell["source"] = re.sub(r"#\|.*\n", "", cell["source"])

        # Clear outputs
        cell["outputs"] = []

        # Reset execution count
        cell["execution_count"] = None

    nb.write(notebook, notebook_path)

def main():
    load_dotenv("_environment")  # Load quarto environment variables

    parser = argparse.ArgumentParser(
        description="Create cleaned Jupyter notebooks from source .qmd and .ipynb files"
    )
    parser.add_argument(
        "--output_dir", default= Path("docs/live-notebooks"), type=Path, help="Output directory for notebooks"
    )
    parser.add_argument(
        "--site_url", default=os.environ.get("SITE_URL"), help="Site URL for notebook URLs"
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    for src_path in Path("source").glob("*"):
        if not src_path.name.startswith("_") and src_path.suffix in {".qmd", ".ipynb"}:
            out_path = args.output_dir / src_path.with_suffix(".ipynb").name
            if not out_path.exists() or out_path.stat().st_mtime < src_path.stat().st_mtime:
                create_notebook(src_path, out_path, args.site_url)
                clean_notebook(out_path)

if __name__ == "__main__":
    main()





