# Relative World

Relative World is a Python-based simulation framework that allows for the creation and management of entities and events within a simulated environment.

## Features

- **Entity Management**: Create, update, and manage entities within the simulation.
- **Event Propagation**: Propagate events through entities and handle them accordingly.
- **Ollama Integration**: Integrate with Ollama for generating responses and actions based on events.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Creating an Entity

To create a new entity, subclass the `Entity` class and define its attributes and methods:

```python
from relative_world.entity import Entity

class MyEntity(Entity):
    def act(self):
        # Define actions for the entity
        pass
```

### Handling Events

Entities can handle events by overriding the `handle_event` method:

```python
def handle_event(self, entity, event):
    # Handle the event
    pass
```

### Updating Entities

Entities can be updated by calling the `update` method, which yields events:

```python
for entity, event in my_entity.update():
    # Process the event
    pass
```

### Ollama Integration

The `OllamaEntity` class extends `Entity` and integrates with Ollama for generating responses and actions:

```python
from relative_world_ollama.entity import OllamaEntity

class MyOllamaEntity(OllamaEntity):
    def get_system_prompt(self):
        return "You are a helpful assistant."
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
