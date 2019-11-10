title: It's the little things
---
ctime: 2019-10-27
---
tags:

python
fundamentals
---
summary:

---
content:

## NEXT then the different meanings of `_` 

## Something I really must underscore ...

### `_` (single underscore)

Doesn't look like much, but has quite a few special meanings

As the (complete) name: "I have to assign a name here, but won't be using it"


```python
left, _, right = (0, 1, 2)
left, right

```
```text
[result]
(0, 2)
```

```python
for _ in range(3):
    print("hi")

```
```text
[stdout]
hi
hi
hi

```
As prefix: "This is private, please don't use it"


```python
_private_name = "Please don't access me from outside"

```
As postfix: "I would shadow something here , but really wan't to name it that way."


```python
dir_ = "somedir"  #  Don't overwrite builtin dir
dir(dir_)[0]

```
```text
[result]
'__add__'
```
## `__` (double underscore (a.k.a. dunder))

* as prefix in a class method: "mangle the name, I might want to still use that, even if it's overwritten"


```python
class A:
    def __mangled(self):
        print("a")


A.__mangled

```
```text
[AttributeError]
type object 'A' has no attribute '__mangled'
```

```python
a = A()
a.__mangled

```
```text
[AttributeError]
'A' object has no attribute '__mangled'
```

```python
A._A__mangled

```
```text
[result]
<function __main__.A.__mangled(self)>
```

```python
class B(A):
    def __mangled(self):
        print("b")

```

```python
B._A__mangled

```
```text
[result]
<function __main__.A.__mangled(self)>
```
## `__...__` (double double underscore)

### (a.k.a. also dunder ... I think)

### ["I am very special, maybe even magic ..."](https://docs.python.org/3/reference/datamodel.html#special-method-names)

> A class can implement certain operations that are invoked by special syntax (such as arithmetic operations or subscripting and slicing) by defining methods with special names. This is Python’s approach to operator overloading, allowing classes to define their own behavior with respect to language operators. 

-- [Python docs](https://docs.python.org/3/reference/datamodel.html#special-method-names)

... They are defining "language operators" very broadly there

# Passing arguments

Independent order if using kwargs even for positional arguments


```python
def func(foo, *args, baz=None, **kwargs):
    print(f"foo: {foo}, args: {args}, baz: {baz}, kwargs: {kwargs}")


func(1, 2, 3, 4)

```
```text
[stdout]
foo: 1, args: (2, 3, 4), baz: None, kwargs: {}

```

```python
func(2, 1, 3, x=5)

```
```text
[stdout]
foo: 2, args: (1, 3), baz: None, kwargs: {'x': 5}

```

```python
func(bar=2, foo=1)

```
```text
[stdout]
foo: 1, args: (), baz: None, kwargs: {'bar': 2}

```

```python
func(2, 4, bar=2)

```
```text
[stdout]
foo: 2, args: (4,), baz: None, kwargs: {'bar': 2}

```

```python
func(bar=2, foo=1, baz=3)

```
```text
[stdout]
foo: 1, args: (), baz: 3, kwargs: {'bar': 2}

```

```python
func(bar=2, foo=1, baz=3, bam=4)

```
```text
[stdout]
foo: 1, args: (), baz: 3, kwargs: {'bar': 2, 'bam': 4}

```
## Arguments are passed by assignment

That is **neither** pass by value nor pass by reference

... but closer to call by reference - except that you can't pass a reference to a reference.

In C++ you would call this [pass by const reference](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3445.html), which means you can't pass a pointer to a pointer (please correct me if I am wrong - C++ is not my string suite).

## Boolean operations return the object

(**not** a boolean)


```python
emtpy_list = []
non_empty_list = [1, 2, "That's handy actually ..."]
emtpy_list or non_empty_list

```
```text
[result]
[1, 2, "That's handy actually ..."]
```
## Handy in assignments of function arguments


```python
def foo(my_list=None):
    my_list = my_list or []

```
(To avoid the mutable objects as default parameters gotcha)


```python
def foo(my_list=[]):
    my_list.append(1)
    print(my_list)


foo(), foo(), foo(), foo()

```
```text
[stdout]
[1]
[1, 1]
[1, 1, 1]
[1, 1, 1, 1]

```
```text
[result]
(None, None, None, None)
```
!!! This article is generated from a [Jupyter notebook](https://jupyter.org/) running in a Python 3.8 kernel. You can [download it](https://oliver.bestwalter.de/articles/its-the-little-things-stash/its-the-little-things.ipynb) and play with it.
