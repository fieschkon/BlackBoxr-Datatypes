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
    - [CollectionElement().getPrivateValue](#collectionelement()getprivatevalue)
    - [CollectionElement().getPublicValue](#collectionelement()getpublicvalue)
    - [CollectionElement().setPrivateValue](#collectionelement()setprivatevalue)
    - [CollectionElement().setPublicValue](#collectionelement()setpublicvalue)
    - [CollectionElement().toDict](#collectionelement()todict)
  - [ItemDefinition](#itemdefinition)
    - [ItemDefinition().addField](#itemdefinition()addfield)
    - [ItemDefinition().addFields](#itemdefinition()addfields)
    - [ItemDefinition.fromDict](#itemdefinitionfromdict)
    - [ItemDefinition().toDict](#itemdefinition()todict)
  - [ItemTypeCollection](#itemtypecollection)
    - [ItemTypeCollection().addDesignElement](#itemtypecollection()adddesignelement)
    - [ItemTypeCollection().addDesignElements](#itemtypecollection()adddesignelements)
    - [ItemTypeCollection().addRequirement](#itemtypecollection()addrequirement)
    - [ItemTypeCollection().addRequirements](#itemtypecollection()addrequirements)
    - [ItemTypeCollection().addTestItem](#itemtypecollection()addtestitem)
    - [ItemTypeCollection().addTestItems](#itemtypecollection()addtestitems)
    - [ItemTypeCollection.fromDict](#itemtypecollectionfromdict)
    - [ItemTypeCollection().toDict](#itemtypecollection()todict)
  - [System](#system)

## CollectionElement

[Show source in BBData.py:13](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L13)

#### Signature

```python
class CollectionElement:
    def __init__(self) -> None:
        ...
```

### CollectionElement.copy

[Show source in BBData.py:68](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L68)

Create a copy of an element

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

[Show source in BBData.py:15](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L15)

Diff elements

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

[Show source in BBData.py:29](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L29)

Creates Collection Element from dict

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

[Show source in BBData.py:55](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L55)

Creates Collection Element from str

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

[Show source in BBData.py:113](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L113)

Generate the current time

#### Returns

- `str` - Current Time

#### Signature

```python
def generateCreateTime(self):
    ...
```

### CollectionElement().getPrivateValue

[Show source in BBData.py:106](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L106)

#### Signature

```python
def getPrivateValue(self, key):
    ...
```

### CollectionElement().getPublicValue

[Show source in BBData.py:103](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L103)

#### Signature

```python
def getPublicValue(self, key):
    ...
```

### CollectionElement().setPrivateValue

[Show source in BBData.py:109](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L109)

#### Signature

```python
def setPrivateValue(self, key, value):
    ...
```

### CollectionElement().setPublicValue

[Show source in BBData.py:99](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L99)

#### Signature

```python
def setPublicValue(self, key, value):
    ...
```

### CollectionElement().toDict

[Show source in BBData.py:122](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L122)

Serialize to dict

#### Returns

- `dict` - serialized dict

#### Signature

```python
def toDict(self) -> dict:
    ...
```



## ItemDefinition

[Show source in BBData.py:161](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L161)

Defines an item to be displayed in panels and on the canvas. Contains fields that change how input is taken from the user.

#### Signature

```python
class ItemDefinition(CollectionElement):
    def __init__(self, name: str = "Item Definition", fields: list[Field] = []) -> None:
        ...
```

#### See also

- [CollectionElement](#collectionelement)
- [Field](./Fields.md#field)

### ItemDefinition().addField

[Show source in BBData.py:231](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L231)

Adds a field to the item definition

#### Arguments

- `field` *Field* - Field to add

#### Signature

```python
def addField(self, field: Field):
    ...
```

#### See also

- [Field](./Fields.md#field)

### ItemDefinition().addFields

[Show source in BBData.py:240](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L240)

Adds a list of fields to the item definition.

#### Arguments

- `fields` *list[Field]* - Fields to add

#### Signature

```python
def addFields(self, fields: list[Field]):
    ...
```

#### See also

- [Field](./Fields.md#field)

### ItemDefinition.fromDict

[Show source in BBData.py:165](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L165)

Creates ItemDefinitionCollection from dict

#### Arguments

- `inDict` *dict* - Dictionary to parse

#### Returns

- `ItemDefinitionCollection` - Item Collection

#### Signature

```python
@staticmethod
def fromDict(inDict: dict):
    ...
```

### ItemDefinition().toDict

[Show source in BBData.py:219](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L219)

Serializes Item Definition to dict

#### Returns

- `dict` - output dictionary

#### Signature

```python
def toDict(self) -> dict:
    ...
```



## ItemTypeCollection

[Show source in BBData.py:260](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L260)

Collection of item types to be used inside systems and standards collections.

#### Signature

```python
class ItemTypeCollection(CollectionElement):
    def __init__(self, name: str = "Item Definition Collection") -> None:
        ...
```

#### See also

- [CollectionElement](#collectionelement)

### ItemTypeCollection().addDesignElement

[Show source in BBData.py:347](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L347)

Adds a single design element definition

#### Arguments

- `designelement` *ItemDefinition* - Design element to add

#### Signature

```python
def addDesignElement(self, designelement: ItemDefinition):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection().addDesignElements

[Show source in BBData.py:357](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L357)

Adds multiple design element definitions

#### Arguments

- `designelements` *list[ItemDefinition]* - Design elements to add

#### Signature

```python
def addDesignElements(self, designelements: list[ItemDefinition]):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection().addRequirement

[Show source in BBData.py:327](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L327)

Adds a single requirement

#### Arguments

- `requirement` *ItemDefinition* - Requirement type to add

#### Signature

```python
def addRequirement(self, requirement: ItemDefinition):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection().addRequirements

[Show source in BBData.py:337](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L337)

Adds multiple requirements

#### Arguments

- `requirements` *list[ItemDefinition]* - Requirement types to add

#### Signature

```python
def addRequirements(self, requirements: list[ItemDefinition]):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection().addTestItem

[Show source in BBData.py:367](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L367)

Adds a test item definition

#### Arguments

- `testitem` *ItemDefinition* - Test item

#### Signature

```python
def addTestItem(self, testitem: ItemDefinition):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection().addTestItems

[Show source in BBData.py:377](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L377)

Adds multiple test item definitions

#### Arguments

- `testitems` *list[ItemDefinition]* - Definitions to add

#### Signature

```python
def addTestItems(self, testitems: list[ItemDefinition]):
    ...
```

#### See also

- [ItemDefinition](#itemdefinition)

### ItemTypeCollection.fromDict

[Show source in BBData.py:264](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L264)

Create ItemTypeCollection from dictionary.

#### Arguments

- `inDict` *dict* - input dictionary

#### Returns

- [ItemTypeCollection](#itemtypecollection) - ItemTypeCollection

#### Signature

```python
@staticmethod
def fromDict(inDict: dict):
    ...
```

### ItemTypeCollection().toDict

[Show source in BBData.py:313](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L313)

Serializes ItemTypeCollection to dict

#### Returns

- `dict` - output dict

#### Signature

```python
def toDict(self) -> dict:
    ...
```



## System

[Show source in BBData.py:387](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/BBData.py#L387)

#### Signature

```python
class System(CollectionElement):
    def __init__(self) -> None:
        ...
```

#### See also

- [CollectionElement](#collectionelement)


