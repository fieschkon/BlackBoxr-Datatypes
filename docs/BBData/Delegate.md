# Delegate

[Blackboxr-datatypes Index](../README.md#blackboxr-datatypes-index) /
[Bbdata](./index.md#bbdata) /
Delegate

> Auto-generated documentation for [BBData.Delegate](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Delegate.py) module.

- [Delegate](#delegate)
  - [Delegate](#delegate-1)
    - [Delegate().connect](#delegate()connect)
    - [Delegate().disconnect](#delegate()disconnect)
    - [Delegate().emit](#delegate()emit)

## Delegate

[Show source in Delegate.py:4](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Delegate.py#L4)

#### Signature

```python
class Delegate:
    def __init__(self) -> None:
        ...
```

### Delegate().connect

[Show source in Delegate.py:9](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Delegate.py#L9)

Connect function handle to delegate.

#### Arguments

- `function` *Callable* - The handle for the method to be executed. Must handle *args.

#### Signature

```python
def connect(self, function: Callable):
    ...
```

### Delegate().disconnect

[Show source in Delegate.py:18](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Delegate.py#L18)

Disconnects function handle from delegate.

#### Arguments

- `function` *Callable* - The handle to be disconnected from the delegate.

#### Signature

```python
def disconnect(self, function: Callable):
    ...
```

### Delegate().emit

[Show source in Delegate.py:27](https://github.com/fieschkon/BlackBoxr-Datatypes/blob/main/BBData/Delegate.py#L27)

#### Signature

```python
def emit(self, *args):
    ...
```


