# PySimpleGUIDocGen
PySimpleGUIDocGen - is software for generating *some* documentation.

This project is created for generating and maintaining `readme.md` for PySimpleGUI library.

Simple and easy.

# What is what?

|Folder or File|Meaning|
|-|-|
|`doc_string__to__doc_string/` | making `class` doc string from one version of PSG to another|
|`db/` | building parts|
|`make_real_readme.py` | the builder|
|`PySimpleGUIlib.py` | some version of PySimpleGUI|


# Usage

### CLI:

Basic usage:

```bash
python3 make_real_readme.py
```

You will get your markdown file `FINALreadme.md`.

For help:

```bash
>>> python3 make_real_readme.py --help

Usage: make_real_readme.py [OPTIONS]

Options:
  -nol, --no_log                Disable log
  -rml, --delete_log            Delete log file after generating
  -rmh, --delete_html_comments  Delete html comment in the generated .md file
  -o, --output_name PATH        Name for generated .md file
  -lo, --log_file PATH          Name for log file
  --help                        Show this message and exit.
```

---

Make output file `test.md` and log file 'mylog.log'

```bash
python3 make_real_readme.py -o test.md -lo mylog.log
```


Make log, but don't output anything in it

```bash
python3 make_real_readme.py -o test.md -lo mylog.log --no_log
```


Remove log after generating

```bash
python3 make_real_readme.py -o test.md -rml
```


Remove log after generating + remove html triple '\n' in output file (**I use this a lot**)

```bash
python3 make_real_readme.py -o test.md -rml -rmh -nol
```


### GUI:

I removed it. *LEARN SHELL.*

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

    def __init__(self, name, age=20, color='white', headsize=None, width=180):
        """                                    
        :param name: name of person
        :param age: age of person (Default value = 20)
        :param color:  (Default value = 'white')
        :param headsize:  (Default value = None)
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

|Tag|Looks like|Example|
| :-: | --- | --- |
| for classes  | `<!-- <+Classname.method+> -->`   | `<!-- <+Button.Update+> -->` |
| for function | `<!-- <+func.function_name+> -->` | `<!-- <+func.Popup+> -->` |



You can add `1` or `2` before function or method.

|Function or Method|Meaning|                      Looks|
| :-:              |  :-:                        |            ---                   |
| `.testmethod`    | signature + table of params |  `<!-- <+Button.Update+> -->`    |
| `.1testmethod`   | signature                   |  `<!-- <+func.1Popup+> -->`      |
| `.2testmethod`   | table of params             |  `<!-- <+Listbox.2Update+> -->`  |


Here is mapping between tags and doc_strings:

![mdfile](https://github.com/nngogol/PySimpleGUIDocGen/blob/master/img/tags.png)


---
---

#### Comprehensive Example

Let's take this `Person` class:

```python

class Person(object):
    """
        Person class for tracking data about people
        and predict the future.

        This class is used in scientific tasks.
        """

    def __init__(self, name, age=20, color='white', headsize=None, width=180):
        """                                    

        :param name: full name of person
        :param age: age of the person (Default value = 20)
        :param color: skin color (Default value = 'white')
        :param headsize: size of the persons head (Default value = None)
        :param width: width from left hand to the right (Default value = 180)

        """
        self.name = name
        self.age = age
        self.color = color
        self.headsize = headsize
        self.width = width

    def sey_hello(self, person=None):
        """

        :param person: person, that will hear your "hello"

        """
        if person:
            print(f'Hello from {self.name} to {person.name}')
        else:
            print(f'Hello! I\'m {self.name}')


class Animal(object):
    """
        Animal class. Animal - is a person's home pet.
        It's just for fun

        This class is used in scientific tasks.
        """

    def __init__(self, name, person, age=20, color='white', tailsize=None, width=180):
        """                                    

        :param name: full name of animal
        :param person: person, who in responsible for this animal
        :param age: age of the animal (Default value = 20)
        :param color: skin color (Default value = 'white')
        :param tailsize: lenght of tail (Default value = None)
        :param width: width from left head to tail (Default value = 180)

        """
        self.name = name
        self.person = person
        self.age = age
        self.color = color
        self.tailsize = tailsize
        self.width = width

    def sey_hello(self, somebody=None):
        """

        :param somebody: animal or person, that will hear your "hello"

        """
        if somebody:
            print(f'wu-wu-wuf!')
        else:
            print(f'wuf!')


```

Let's make simple block:

![mdfile](https://github.com/nngogol/PySimpleGUIDocGen/blob/master/img/mdfile1.png)

Now, look on this diagram:

![fulldiag](https://github.com/nngogol/PySimpleGUIDocGen/blob/master/img/full-diag.png)

----

"`testmethod`" can be any method, that really exists in class: "`__init__, hello, blabla`" etc.

**Big exception is "`.doc`"** - it will render doc string **for your class**.

If you have method `doc` in your class - it's bad for your (it wouldn't show in generated docs - it will insted show doc string of class).

----

The function tag  `<!-- <+func.function_name+> -->` is like class tag.
Just say `func.`  + your func name. No more no less.



### Examples

#### **class tag:**

```
<!-- <+Button.doc+> -->
<!-- <+Button.2__init__+> -->
<!-- <+Button.Update+> -->
<!-- <+Button.1GetText+> -->
```

#### **func tag:**

```
<!-- <+func.Popup+> -->
<!-- <+func.PopupAnimated+> -->
<!-- <+func.2TestoFunction+> -->
```

