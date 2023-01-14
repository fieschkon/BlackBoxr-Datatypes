# Bbdata

[Blackboxr-datatypes Index](../README.md#blackboxr-datatypes-index) /
[Bbdata](./index.md#bbdata) /
Bbdata

> Auto-generated documentation for [BBData.BBData](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py) module.

- [Bbdata](#bbdata)
  - [CollectionElement](#collectionelement)
    - [CollectionElement.copy](#collectionelementcopy)
    - [CollectionElement.diff](#collectionelementdiff)
    - [CollectionElement.fromDict](#collectionelementfromdict)
    - [CollectionElement.fromStr](#collectionelementfromstr)
    - [CollectionElement().generateCreateTime](#collectionelement()generatecreatetime)
    - [CollectionElement().toDict](#collectionelement()todict)
  - [Delegate](#delegate)
    - [Delegate().connect](#delegate()connect)
    - [Delegate().disconnect](#delegate()disconnect)
    - [Delegate().emit](#delegate()emit)

## CollectionElement

[Show source in BBData.py:37](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L37)

#### Signature

```python
class CollectionElement:
    def __init__(self) -> None:
        ...
```

### CollectionElement.copy

[Show source in BBData.py:92](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L92)

copy Create a copy of an element

#### Arguments

- `element` *CollectionElement* - Element to copy

#### Returns

- [CollectionElement](#collectionelement) - Copied Element

#### Signature

```python
@staticmethod
def copy(element):
    ...
```

### CollectionElement.diff

[Show source in BBData.py:39](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L39)

diff Diff elements

#### Arguments

- `elementA` *CollectionElement* - Original Element
- `elementB` *CollectionElement* - New Element

#### Returns

- `list` - List of changes

#### Signature

```python
@staticmethod
def diff(elementA, elementB):
    ...
```

### CollectionElement.fromDict

[Show source in BBData.py:53](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L53)

fromDict Creates Collection Element from dict

#### Arguments

- `inDict` *dict* - Dictionary to parse

#### Returns

- [CollectionElement](#collectionelement) - Element

#### Signature

```python
@staticmethod
def fromDict(inDict: dict):
    ...
```

### CollectionElement.fromStr

[Show source in BBData.py:79](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L79)

fromStr Creates Collection Element from str

#### Arguments

- `inStr` *str* - Input String

#### Returns

- [CollectionElement](#collectionelement) - Element

#### Signature

```python
@staticmethod
def fromStr(inStr: str):
    ...
```

### CollectionElement().generateCreateTime

[Show source in BBData.py:121](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L121)

generateCreateTime Generate the current time

#### Returns

- `str` - Current Time

#### Signature

```python
def generateCreateTime(self):
    ...
```

### CollectionElement().toDict

[Show source in BBData.py:130](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L130)

toDict Serialize to dict

#### Returns

- `dict` - serialized dict

#### Signature

```python
def toDict(self) -> dict:
    ...
```



## Delegate

[Show source in BBData.py:10](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L10)

#### Signature

```python
class Delegate:
    def __init__(self) -> None:
        ...
```

### Delegate().connect

[Show source in BBData.py:15](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L15)

connect Connect function handle to delegate.

#### Arguments

- `function` *Callable* - The handle for the method to be executed. Must handle *args.

#### Signature

```python
def connect(self, function: Callable):
    ...
```

### Delegate().disconnect

[Show source in BBData.py:24](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L24)

disconnect Disconnects function handle from delegate.

#### Arguments

- `function` *Callable* - The handle to be disconnected from the delegate.

#### Signature

```python
def disconnect(self, function: Callable):
    ...
```

### Delegate().emit

[Show source in BBData.py:33](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L33)

#### Signature

```python
def emit(self, *args):
    ...
```


