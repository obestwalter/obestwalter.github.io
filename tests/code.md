title: bla
---
cdate: $blubb
----
content:


```python
2 * 2 * 2 * 2  # single line code with single line output
```
```text
[RESULT]
16```
### Pack and unpack arguments


```python
def foo(*args, **kwargs):
    bar(*args, **kwargs)

def bar(a, b, c=None, d=None):
    print(a, b ,c, d)
    
foo(*[1, 2], **dict(c=3, d=4))
```
```text
[STDOUT]
1 2 3 4
```

```python
for seq in ["egg", [1, 2, 3], (1, 2, 3), {1, 2, 3}, {1: 'a', 2: 'b', 3: 'c'}]:
    print(f"{seq} is {type(seq)}")
    a, b, c = seq
    print(f"a, b, c  -> {a} {b} {c}")
    *a, b = seq
    print(f"*a, b = seq -> {a} {b}")
    a, *b = seq
    print(f"a, *b = seq -> {a} {b}\n")
```
```text
[STDOUT]
egg is <class 'str'>
a, b, c  -> e g g
*a, b = seq -> ['e', 'g'] g
a, *b = seq -> e ['g', 'g']

[1, 2, 3] is <class 'list'>
a, b, c  -> 1 2 3
*a, b = seq -> [1, 2] 3
a, *b = seq -> 1 [2, 3]

(1, 2, 3) is <class 'tuple'>
a, b, c  -> 1 2 3
*a, b = seq -> [1, 2] 3
a, *b = seq -> 1 [2, 3]

{1, 2, 3} is <class 'set'>
a, b, c  -> 1 2 3
*a, b = seq -> [1, 2] 3
a, *b = seq -> 1 [2, 3]

{1: 'a', 2: 'b', 3: 'c'} is <class 'dict'>
a, b, c  -> 1 2 3
*a, b = seq -> [1, 2] 3
a, *b = seq -> 1 [2, 3]

```

```python
%%capture
a = {"a": 1, "foo": { "a": 1}}
b = {"a": 1, "foo": { "b": 2, "c": 3}}
# This will not merge the nested dict foo, but overwrite it
```

```python
raise SyntaxError("NO OTHER OUTPUT!")

```
```text
[ERROR]
SyntaxError: NO OTHER OUTPUT! (<string>)```

```python
print("Other output")
raise ValueError("BOOM WITH OTHER OUTPUTS!")

```
```text
[STDOUT]
Other output
```
```text
[ERROR]
ValueError: BOOM WITH OTHER OUTPUTS!```

```python
{**a, **b}
```
```text
[RESULT]
{'a': 1, 'foo': {'b': 2, 'c': 3}}```
!!! This article is generated from a [Jupyter notebook](https://jupyter.org/).
You can [download it](https://oliver.bestwalter.de/articles/tests/code.ipynb) and play with it.
