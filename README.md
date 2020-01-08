The word **spiegel** is German for **mirror**. This library enables you to quickly expose/mirror a python class instance via a http server.

## Installation

- install from pypi via `pip install spiegel`

## What it is

In order to function, **spiegel** needs both a server and a client. 
The server uses your an instance of your class and exposes an API via http which 1:1 mirrors the methods and properties on the object. If any of those endpoints is called, the server simply calls the respective method on the object it keeps locally. 
The client is started with your class and an address to the server. It replaces all methods and properties on the class with http requests to the respective endpoint on the remote mirror object that is running as an http server.

The client looks and behaves just like if you had a local instance of the object in memory, but instead it generates all behavior by communicating with the mirrored object.

## Example

- define a simple `Calculator` class in a file `calculator.py`
```python
class Calculator:
    def __init__(self):
        self._last_result = None

    @property
    def last_result(self) -> float:
        return self._last_result

    def sum(self, a: float, b: float) -> float:
        self._last_result = a + b
        return self.last_result
```


### Server

- now create a server as follows in a file `calculator_server.py`
```python
from spiegel.server import create_server
from calculator import Calculator

def create_app():
    return create_server(Calculator())
```

- the server uses `flask` under the hood, so you can start it in the following way from your cli
```bash
$ export FLASK_APP=calculator_server.py
$ flask run --port=5000
```


### Client

- now create a client as follows in a file `calculator_client.py`
```python
from spiegel.client import create_client
from calculator import Calculator

if __name__ == "__main__":
    calculator = create_client(Calculator, "http://localhost:5000")()
    print(calculator.sum(1, 2))
    print(calculator.last_result)
    print(calculator.sum(2, 3))
    print(calculator.last_result)
```

- execute in a separate cli window/tab and the script should print the following as expected
```bash
$ python calculator_client.py
3
3
5
5
```

- you should also see the appropriate endpoints on the server being called

And that's it. Obviously it only gets really interesting once you put the server somewhere other than your local machine.
