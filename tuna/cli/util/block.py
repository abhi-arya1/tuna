# pylint: disable=missing-module-docstring

class JupyterBlock:
    """
    Defines a block in a Jupyter Notebook for Tuna autogenerations.
    """
    def __init__(self, markdown: 'function' | str, code: 'function' | str, _id: int):
        self._md = markdown
        self._code = code
        self._id = _id



    def md(self, *args, **kwargs):
        """
        Returns the markdown content of the block.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: The markdown content of the block.

        Raises:
            ValueError: If the block does not accept markdown arguments.
        """
        if callable(self._md):
            return self._md(*args, **kwargs)

        if args or kwargs:
            raise ValueError(f"Block '{self._id}' does not accept markdown arguments.")
        return self._md



    def code(self, *args, **kwargs):
        """
        Returns the code content of the block.
         
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns: 
            str: The code content of the block.

        Raises: 
            ValueError: If the block does not accept code arguments.
        """
        if callable(self._code):
            return self._code(*args, **kwargs)

        if args or kwargs:
            raise ValueError(f"Block '{self._id}' does not accept code arguments.")
        return self._code



    def __str__(self):
        return f"JupyterBlock({self._id})"
