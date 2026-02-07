# Functional Module

The `functional` module provides utilities for building composable function pipelines.

## Classes

### Pipeline

```markdown
::: iragca.functional.Pipeline
```

### Step

```markdown
::: iragca.functional.Step
```

## Overview

The `functional` module enables functional programming patterns in Python, allowing you to:

- **Build pipelines**: Chain multiple functions together in a sequence
- **Reuse steps**: Encapsulate functions with pre-bound arguments using `Step`
- **Compose transformations**: Create readable, composable data transformation workflows

## Examples

### Basic Pipeline

```python
from iragca.functional import Pipeline

# Create a simple pipeline
pipeline = Pipeline([
    lambda x: x * 2,
    lambda x: x + 10,
    lambda x: x ** 2,
])

result = pipeline(5)
# Result: (5 * 2 + 10)^2 = 400
```

### Using Steps with Arguments

```python
from iragca.functional import Pipeline, Step

def multiply(x, factor):
    return x * factor

def power(x, exponent):
    return x ** exponent

# Create steps with pre-bound arguments
pipeline = Pipeline([
    Step(multiply, 2),           # Multiply by 2
    Step(lambda x: x + 10),      # Add 10
    Step(power, 2),              # Square the result
])

result = pipeline(5)
# Result: ((5 * 2) + 10)^2 = 400
```

### Using Keyword Arguments

```python
from iragca.functional import Step

step = Step(
    lambda x, y, z: x + y + z,
    y=10,
    z=20
)

result = step(5)
# Result: 5 + 10 + 20 = 35
```
