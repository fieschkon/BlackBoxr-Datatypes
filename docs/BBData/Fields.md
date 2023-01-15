# Fields

[Blackboxr-datatypes Index](../README.md#blackboxr-datatypes-index) /
[Bbdata](./index.md#bbdata) /
Fields

> Auto-generated documentation for [BBData.Fields](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py) module.

- [Fields](#fields)
  - [Checks](#checks)
    - [Checks().fromDict](#checks()fromdict)
    - [Checks().getOption](#checks()getoption)
    - [Checks().setOption](#checks()setoption)
    - [Checks().toDict](#checks()todict)
  - [Field](#field)
    - [Field().fromDict](#field()fromdict)
    - [Field().toDict](#field()todict)
  - [FieldType](#fieldtype)
  - [LongText](#longtext)
    - [LongText().fromDict](#longtext()fromdict)
    - [LongText().toDict](#longtext()todict)
  - [Radio](#radio)
    - [Radio().disableOtherOptions](#radio()disableotheroptions)
    - [Radio().fromDict](#radio()fromdict)
    - [Radio().toDict](#radio()todict)
  - [ShortText](#shorttext)
    - [ShortText().fromDict](#shorttext()fromdict)
    - [ShortText().toDict](#shorttext()todict)

## Checks

[Show source in Fields.py:36](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L36)

#### Signature

```python
class Checks(Field):
    def __init__(
        self,
        options: list[tuple[int, str, bool]],
        fieldname: str = "Default Checkbox Field",
    ) -> None:
        ...
```

#### See also

- [Field](#field)

### Checks().fromDict

[Show source in Fields.py:38](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L38)

#### Signature

```python
def fromDict(indict: dict):
    ...
```

### Checks().getOption

[Show source in Fields.py:55](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L55)

#### Signature

```python
def getOption(self, index: int):
    ...
```

### Checks().setOption

[Show source in Fields.py:51](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L51)

#### Signature

```python
def setOption(self, index: int, state: bool):
    ...
```

### Checks().toDict

[Show source in Fields.py:58](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L58)

#### Signature

```python
def toDict(self):
    ...
```



## Field

[Show source in Fields.py:17](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L17)

#### Signature

```python
class Field:
    def __init__(self, fieldname: str = "Default Field Name") -> None:
        ...
```

### Field().fromDict

[Show source in Fields.py:19](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L19)

#### Signature

```python
def fromDict(indict: dict):
    ...
```

### Field().toDict

[Show source in Fields.py:25](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L25)

#### Signature

```python
def toDict(self):
    ...
```



## FieldType

[Show source in Fields.py:7](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L7)

FieldType for interpreting serialization

#### Signature

```python
class FieldType(Enum):
    ...
```



## LongText

[Show source in Fields.py:109](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L109)

#### Signature

```python
class LongText(ShortText):
    def __init__(self, fieldname: str = "Default LongText Name", defaultText="") -> None:
        ...
```

#### See also

- [ShortText](#shorttext)

### LongText().fromDict

[Show source in Fields.py:111](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L111)

#### Signature

```python
def fromDict(indict: dict):
    ...
```

### LongText().toDict

[Show source in Fields.py:117](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L117)

#### Signature

```python
def toDict(self):
    ...
```



## Radio

[Show source in Fields.py:64](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L64)

#### Signature

```python
class Radio(Checks):
    def __init__(
        self,
        options: list[tuple[int, str, bool]],
        maximumAllowedChecks=1,
        fieldname: str = "Default Checkbox Field",
    ) -> None:
        ...
```

#### See also

- [Checks](#checks)

### Radio().disableOtherOptions

[Show source in Fields.py:81](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L81)

#### Signature

```python
def disableOtherOptions(self, args):
    ...
```

### Radio().fromDict

[Show source in Fields.py:66](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L66)

#### Signature

```python
def fromDict(indict: dict):
    ...
```

### Radio().toDict

[Show source in Fields.py:87](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L87)

#### Signature

```python
def toDict(self):
    ...
```



## ShortText

[Show source in Fields.py:94](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L94)

#### Signature

```python
class ShortText(Field):
    def __init__(
        self, fieldname: str = "Default ShortText Name", defaultText=""
    ) -> None:
        ...
```

#### See also

- [Field](#field)

### ShortText().fromDict

[Show source in Fields.py:96](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L96)

#### Signature

```python
def fromDict(indict: dict):
    ...
```

### ShortText().toDict

[Show source in Fields.py:103](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Fields.py#L103)

#### Signature

```python
def toDict(self):
    ...
```


