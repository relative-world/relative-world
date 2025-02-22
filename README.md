# Relative World Ollama

Relative World Ollama is a Python simulation extension for interacting with the Ollama API. It leverages structured prompt generation, response validation using Pydantic, and JSON repair functionality for a dynamic simulation framework built upon Relative World.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
  - [Basic Usage of `OllamaEntity`](#basic-usage-of-ollamaentity)
  - [Custom Response Model](#custom-response-model)
  - [Handling JSON Fixing](#handling-json-fixing)
- [Configuration](#configuration)
- [Testing](#testing)
- [License](#license)

## Overview

Relative World Ollama extends the Relative World simulation framework by integrating API-driven entity behavior using the Ollama model. It provides a base `OllamaEntity` class that wraps prompt generation, response validation with Pydantic models, and error handling (including fixing malformed JSON responses).

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the project, run:

```bash
poetry install
```

## Usage Examples

### Basic Usage of `OllamaEntity`

The following example shows how to subclass `OllamaEntity` and implement the `get_prompt` method for generating a query.

```python
import asyncio
from relative_world_ollama.entity import OllamaEntity

class MyOllamaEntity(OllamaEntity):
    def get_prompt(self):
        return "What is the capital of France?"

    async def handle_response(self, response):
        print(response.text)

# Create and update the entity
entity = MyOllamaEntity(name="CapitalQuery")
asyncio.run(entity.update())
```

### Custom Response Model

This example demonstrates how to use a custom Pydantic response model.

```python
import asyncio
from pydantic import BaseModel
from relative_world_ollama.entity import OllamaEntity

class CustomResponse(BaseModel):
    answer: str

class CustomOllamaEntity(OllamaEntity):
    response_model = CustomResponse

    def get_prompt(self):
        return "What is the capital of Germany?"

    async def handle_response(self, response: CustomResponse):
        print(f"The answer is: {response.answer}")

entity = CustomOllamaEntity(name="CapitalQuery")
asyncio.run(entity.update())
```

### Handling JSON Fixing

When the API returns malformed JSON, the `fix_json_response` function can repair it:

```python
import asyncio
from ollama import AsyncClient

from relative_world_ollama.client import fix_json_response
from pydantic import BaseModel
from relative_world_ollama.exceptions import UnparsableResponseError
from relative_world_ollama.settings import settings


class ExampleResponse(BaseModel):
    data: str

client = AsyncClient(host=settings.base_url)
bad_json = '{"data": "Hello, world"'

async def main():
    try:
        fixed_json = await fix_json_response(client, bad_json, ExampleResponse)
        print(fixed_json)
    except UnparsableResponseError as e:
        print(f"Failed to parse JSON: {e}")

asyncio.run(main())
```

## Configuration

The module is configured in the `relative_world_ollama/settings.py` file. Key settings include:
- `base_url` – Base URL for the Ollama API.
- `default_model` – Default model for generation.
- `json_fix_model` – Model used to fix malformed JSON responses.
- `model_keep_alive` – Duration (in seconds) to keep the model alive during execution.

You can override these settings via environment variables prefixed with `relative_world_ollama_`.

## Testing

Tests are executed using [pytest](https://docs.pytest.org/). Run the tests with:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License.
