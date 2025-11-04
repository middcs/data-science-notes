import os
import nbformat as nb
import re
import shutil


os.makedirs("docs/live-notebooks", exist_ok=True)
for f in os.listdir("source"):
    if f.endswith(".qmd"):
        out_path = f"docs/live-notebooks/{f.replace('qmd', 'ipynb')}"
        os.system(f"quarto convert source/{f} -o {out_path}")
        
    elif f.endswith(".ipynb"):
        
        out_path = f"docs/live-notebooks/{f}"
        shutil.copyfile(f"source/{f}", out_path)
        
    notebook = nb.read(out_path, as_version = 4)
    
    for cell in notebook["cells"]:
        # remove code content designed to be hidden
        cell["source"] = re.sub(r"#---[\S\s]*?#---", "", cell["source"])
        
        # delete quarto metadata on individual cells
        cell["source"] = re.sub(r"#\|.*\n", "", cell["source"])
        
        # delete YAML metadata in notebook header 
        cell["source"] = re.sub(r"---[\S\s]*?---", "", cell["source"])
        
        # clear outputs
        cell["outputs"] = []
        
        # reset execution count
        cell["execution_count"] = None
        
    nb.write(notebook, out_path)
    




