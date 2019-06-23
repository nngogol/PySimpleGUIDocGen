# PySimpleGUIDocGen
PySimpleGUIDocGen - is software for generating *some* documentation.

Brief: this project is created for generating and maintaining `readme.md` for PySimpleGUI library. Simple and easy.

# What is what?

`db` - building parts

`make_real_readme.py` - the builder

`PySimpleGUIlib.py` - some version of PySimpleGUI


# Usage

### CLI:

```bash
python3 make_real_readme.py
```

You will get `readme.md`.

### GUI:

```bash
python3 make_real_readme.py
```


---

---

---


# Everything is a `function` (maybe even you are)

FUNTION is:

- simple `def test1()`
- class method (it's a function INSIDE of class defenition)

---

# `__doc__`

Every function has `__doc__` - it's just a string.

What we know about `__doc__`? Well:

- it can be big or small.
- it can contain lines starting like `:param blabla1: blabla2`


```python

class Person(object):
    """ hello world from class.__doc__ """      # <- this guy is a "doc string"

    def __init__(self, name, age=20, color='white', dicksize=None, width=180):
        """                                    
        :param name: name of person
        :param age: age of person (Default value = 20)
        :param color:  (Default value = 'white')
        :param dicksize:  (Default value = None)
        :param width:  (Default value = 180)

        """                                     # <- and this guy is a "doc string"
        self.name = name
        self.age = age
        self.color = color
        self.width = width

    def sey_hello(self, person=None):
        """
        :param person: person, that will hear your "hello"
        """                                     # <- and this guy is a "doc string"
        if person:
            print(f'Hello from {self.name} to {person.name}')
        else:
            print(f'Hello! I\'m {self.name}')

```

# There is 2 tags:

| Meaning | his looks |
| :-: | - |
| for classes  | `<!-- <+Classname.method+> -->`   |
| for function | `<!-- <+func.function_name+> -->` |


Here is defenitions for `method` in `Classname` tag:

| TagName | Meaning |
| :-:       |  :-: |
| `.testmethod`      | signature + table of params |
| `.1testmethod`     | signature |
| `.2testmethod`     | table of params |
----

"`testmethod`" can be any method, that really exists in class: "`__init__, hello, blabla`" etc.

**Big exception is "`.class_obj_doc`"**

`.class_obj_doc` will render doc string **for your class**.

If you have method `class_obj_doc` in your class - it's bad for your.

----

The function tag  `<!-- <+func.function_name+> -->` is like class tag.
It's just has 1st part `func`. No more no less.


### Examples

**Possible use cases for 1st tag:**

```
<!-- <+Button.doc+> -->
<!-- <+Button.2__init__+> -->
<!-- <+Button.Update+> -->
<!-- <+Button.1GetText+> -->
```

**Possible use cases for 2st tag:**

```
<!-- <+func.Popup+> -->
<!-- <+func.PopupAnimated+> -->
<!-- <+func.2TestoFunction+> -->
```

