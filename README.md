# Relative World

A Python-based time-stepped simulation providing an environment for Large Language Model (LLM) interactions. This project focuses on representing time and events in a more human-like and relative manner, reducing the need for explicit time calculations within an LLM.

## Features

- **Relative Time Representation**: Uses custom helper functions to convert timestamps into human-readable, relative phrases (e.g., "in 5 minutes", "yesterday", "a year ago").
- **Actors and Scripts**: Allows defining and scheduling actions as `Actor` instances with scripts that execute once their scheduled timestamps occur.
- **Flexible Time Step**: Main simulation updates advance time consistently or even backwards based on a configurable time step.
- **Unit Testing**: Thorough test coverage of major features to ensure stability and correctness.

## Project Structure

- `relative_world/`
  - Contains the core simulation logic, including the `Actor` classes and time utility functions.
- `tests/entity/`
  - Provides unit tests for the entity-related components.
- `tests/actor/`
  - Contains unit tests for the actor-related components.

## Getting Started

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)

### Installation

1. **Clone or Download** the project:
    ```bash
    git clone https://github.com/yourusername/relative_world.git
    cd relative_world
    ```

2. **Install Dependencies**:
    ```bash
    poetry install
    ```

### Running the Simulation

To run the simulation, you can create instances of `RelativeWorld`, `Actor`, and other entities, and then call their `update` methods to progress the simulation.

### Running Tests

To run the tests, use the following command:
```bash
poetry run pytest
```

## Usage

### Defining an Actor

You can define an actor by subclassing the `Actor` class and implementing the `get_action` method:

```python
from relative_world.actor import Actor

class MyActor(Actor):
    def get_action(self, action: str):
        if action == "my_action":
            return self.my_action_method

    def my_action_method(self):
        print("Action executed!")
```

### Creating a Scripted Actor

A `ScriptedActor` can be created by defining a script with `ScriptKeyPoint` instances:

```python
from datetime import datetime, timedelta
from relative_world.actor import ScriptedActor, ScriptKeyPoint

class MyScriptedActor(ScriptedActor):
    script: list[ScriptKeyPoint] = [
        ScriptKeyPoint(
            timestamp=datetime.now() + timedelta(seconds=10),
            action="my_action",
            args=[],
            kwargs={}
        )
    ]

    def get_action(self, action: str):
        if action == "my_action":
            return self.my_action_method

    def my_action_method(self):
        print("Scripted action executed!")
```

### Handling Events

Entities can handle events by implementing the `handle_event` method:

```python
from relative_world.entity import Entity

class MyEntity(Entity):
    def propagate_event(self, event: Event) -> bool:
        print(f"Handling event: {event}")
        return True
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Freezegun](https://github.com/spulec/freezegun)
