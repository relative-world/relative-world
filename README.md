# Project Title

A simulation framework built in Python that manages entities, events, and locations within a dynamic world. This project leverages a structured approach to event propagation and simulation updates via time steps.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Testing](#testing)
- [Usage Examples](#usage-examples)
- [Core Classes](#core-classes)
  - [Entity and Event](#entity-and-event)
  - [Location](#location)
  - [RelativeWorld](#relativeworld)
- [Time Steps](#time-steps)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project simulates a dynamic world where entities and events interact throughout different locations. The core design revolves around the propagation of events and handling privacy through locations. It also allows for complete simulation cycles via time-stepped updates.

## Installation

The project uses [Poetry](https://python-poetry.org/) for dependency management. To install the project, simply run:

```bash
poetry install
```

## Testing

Tests are implemented using [pytest](https://docs.pytest.org/). Run the following command to execute the test suite:

```bash
poetry run pytest
```

## Usage Examples

Refer to the `examples` folder for detailed demonstrations of how to create and simulate common scenarios. Each example provides a step-by-step explanation from creating entities and locations to running a full simulation with time progression.

## Core Classes

### Entity and Event

- **Entity** represents a unit in the simulation capable of producing and handling events.
- **Event** (and the associated `BoundEvent` type) forms the core mechanism enabling interaction and notification between different components of the simulation.

### Location

- **Location** extends the functionality of an Entity by providing locality. Locations maintain privacy settings, allowing them to control whether events bubble up to parent entities. They also facilitate the containment of sub-entities (like actors).

### RelativeWorld

- **RelativeWorld** serves as the full simulation environment that encapsulates locations and actors. It manages the progression of time by updating the simulation through defined time steps.
- A call to the `update` method in `RelativeWorld` applies a time step, handles events from all contained locations, and ensures that the state of the simulation advances in an orderly fashion.

## Time Steps

RelativeWorld uses fixed time intervals to progress the simulation state:
- The simulation start time is recorded at initialization.
- Each update applies a time step interval to compute the current time.
- The framework uses Freezegun to mock all time functions during an update, ensuring that the simulation progresses in a controlled manner.

## Contributing

Contributions are welcome. Please file issues or submit pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.
