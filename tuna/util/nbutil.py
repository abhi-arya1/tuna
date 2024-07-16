"""

Jupyter Notebook Management Utilities for Tuna CLI

"""

from pathlib import Path
from enum import Enum
import nbformat as nbf


class NbType(Enum):
    """
    Enum class to represent the type of a Jupyter Notebook block.
    """
    MARKDOWN = 1
    CODE = 2



class JupyterBlock:
    """
    JupyterBlock class to represent a block in a Jupyter Notebook.
    """
    def __init__(self, _content: str, _type: NbType):
        self._content = _content
        self._type = _type

    def blocktype(self):
        """Return the type of the block"""
        return self._type

    def blockcontent(self):
        """Return the content of the block"""
        return self._content




def _get_notebook(notebook_path: Path) -> nbf.notebooknode.NotebookNode:
    """
    Reads a Jupyter Notebook File and returns the NotebookNode object.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.

    Returns:
        nbf.notebooknode.NotebookNode: The NotebookNode object for the Jupyter Notebook file.
    """
    if notebook_path.exists():
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbf.read(f, as_version=4)
    else:
        return nbf.v4.new_notebook()




def validate_nb(notebook_path: Path) -> bool:
    """
    Validates if a Jupyter Notebook File exists.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.

    Returns:
        bool: True if the Jupyter Notebook file exists, else False.
    """
    return notebook_path.exists()




def add_md_cell(notebook_path: Path, content: str) -> None:
    """
    Adds a Markdown Cell to a Jupyter Notebook File.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.
        content (str): The content to be added to the Markdown Cell.
    """
    nb = _get_notebook(notebook_path)
    new_cell = nbf.v4.new_markdown_cell(content)
    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)




def add_code_cell(notebook_path: Path, content: str) -> None:
    """
    Adds a Code Cell to a Jupyter Notebook File.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.
        content (str): The content to be added to the Code Cell.
    """
    nb = _get_notebook(notebook_path)
    new_cell = nbf.v4.new_code_cell(content)
    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
