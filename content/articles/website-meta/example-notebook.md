This is a raw cell, it will stay unchanged.

## This is a header in a markdown cell

This is a paragraph in a markdown cell. It will be rendered and provides all kinds of fancy things.

```python
# this is a code cell containing Python code - it can be executed
# and the output will be shown in the notebook
print("I the output of a code cell.")
2 + 5  # The evaluated result on the last line, will also be shown
```

    I the output of a code cell.

    7

```python
from pathlib import Path

# this will throw an exception
Path("idontexist").read_text()
```

    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    <ipython-input-2-1980b319f594> in <module>
          2 
          3 # this will throw an exception
    ----> 4 Path("idontexist").read_text()
    

    /usr/local/lib/python3.8/pathlib.py in read_text(self, encoding, errors)
       1206         Open the file in text mode, read it, and close the file.
       1207         """
    -> 1208         with self.open(mode='r', encoding=encoding, errors=errors) as f:
       1209             return f.read()
       1210 


    /usr/local/lib/python3.8/pathlib.py in open(self, mode, buffering, encoding, errors, newline)
       1192         if self._closed:
       1193             self._raise_closed()
    -> 1194         return io.open(self, mode, buffering, encoding, errors, newline,
       1195                        opener=self._opener)
       1196 


    /usr/local/lib/python3.8/pathlib.py in _opener(self, name, flags, mode)
       1046     def _opener(self, name, flags, mode=0o666):
       1047         # A stub for the opener argument to built-in open()
    -> 1048         return self._accessor.open(self, flags, mode)
       1049 
       1050     def _raw_open(self, flags, mode=0o777):


    FileNotFoundError: [Errno 2] No such file or directory: 'idontexist'

