# Relative World

A Python-based time-stepped simulation providing an environment for Large Language Model (\LLM\) interactions. This project focuses on representing time and events in a more human-like and relative manner, reducing the need for explicit time calculations within an \LLM\.

## Features

- **Relative Time Representation**  
  Uses custom helper functions to convert timestamps into human-readable, relative phrases (e.g., "in 5 minutes", "yesterday", "a year ago").

- **Actors and Scripts**  
  Allows defining and scheduling actions as `Actor` instances with scripts that execute once their scheduled timestamps occur.

- **Flexible Time Step**  
  Main simulation updates advance time consistently or even backwards based on a configurable time step.

- **Unit Testing**  
  Thorough test coverage of major features to ensure stability and correctness.

## Project Structure

- `relative_world/`  
  Contains the core simulation logic, including the `Actor` classes and time utility functions.
- `tests/world/`  
  Provides unit tests for the main simulation components.

## Getting Started

1. **Clone or Download** the project.
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
   
## Run Tests

```
python -m unittest discover tests
```
