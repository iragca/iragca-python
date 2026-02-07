# ML Module

The `ml` module provides utilities for machine learning workflows, including lightweight metric logging and tracking.

## Classes

### RunLogger

```markdown
::: iragca.ml.RunLogger
```

## Overview

The `ml` module simplifies experiment tracking and metric logging during machine learning training loops. The `RunLogger` class provides:

- **Lightweight metric tracking**: Log arbitrary scalar metrics with minimal overhead
- **Dynamic property access**: Access metrics as properties (e.g., `logger.loss`)
- **Progress bar integration**: Optional tqdm progress bar for console and Jupyter environments
- **Flexible data export**: Export and import logs as dictionaries

## Key Features

### Automatic Property Creation

Once you log a metric, it becomes accessible as a property:

```python
logger = RunLogger(max_steps=100)
logger.log_metrics({'loss': 0.5, 'accuracy': 0.9}, step=0)

# Access metrics directly
loss_values = logger.loss          # [0.5]
accuracy_values = logger.accuracy  # [0.9]
```

### Progress Bar Support

Display training progress with optional tqdm integration:

```python
# Console environments
logger = RunLogger(max_steps=100, display_progress=True)

# Jupyter Notebook environments
logger = RunLogger(max_steps=100, display_progress=True, notebook=True)
```

### Flexible Data Export/Import

Export your logs and reload them later:

```python
logger = RunLogger(max_steps=3)
logger.log_metrics({'loss': 1.0, 'accuracy': 0.7}, step=0)
logger.log_metrics({'loss': 0.5, 'accuracy': 0.8}, step=1)
logger.log_metrics({'loss': 0.2, 'accuracy': 0.9}, step=2)

# Export to dictionary
logs = logger.get_logs()
# {'step': [0, 1, 2], 'loss': [1.0, 0.5, 0.2], 'accuracy': [0.7, 0.8, 0.9]}

# Load from dictionary
new_logger = RunLogger.from_dict(logs)
```

## Examples

### Basic Training Loop

```python
from iragca.ml import RunLogger

logger = RunLogger(max_steps=10, display_progress=True)

for epoch in range(10):
    # Simulate training
    loss = 1.0 / (epoch + 1)
    accuracy = epoch / 10.0

    # Log metrics
    logger.log_metrics({
        'loss': loss,
        'accuracy': accuracy
    }, step=epoch)

# Access metrics
print(f"Final loss: {logger.loss[-1]}")
print(f"Final accuracy: {logger.accuracy[-1]}")
```

### Multiple Metrics

```python
from iragca.ml import RunLogger

logger = RunLogger(max_steps=5)

for step in range(5):
    logger.log_metrics({
        'train_loss': 0.5 - step * 0.1,
        'val_loss': 0.6 - step * 0.09,
        'train_accuracy': 0.7 + step * 0.04,
        'val_accuracy': 0.65 + step * 0.035,
    }, step=step)

# Access individual metric histories
print(logger.train_loss)
print(logger.val_accuracy)
```

### Jupyter Notebook Integration

```python
from iragca.ml import RunLogger

# Enable notebook-specific progress bar
logger = RunLogger(
    max_steps=100,
    display_progress=True,
    notebook=True,
    update_interval=10  # Update every 10 steps
)

for epoch in range(100):
    loss = 1.0 / (epoch + 1)
    logger.log_metrics({'loss': loss}, step=epoch)
```

### Inspecting Logs

```python
from iragca.ml import RunLogger

logger = RunLogger(max_steps=3)
logger.log_metrics({'loss': 1.0, 'accuracy': 0.7}, step=0)
logger.log_metrics({'loss': 0.5, 'accuracy': 0.8}, step=1)
logger.log_metrics({'loss': 0.2, 'accuracy': 0.9}, step=2)

# Get all recorded steps
print(logger.steps)              # [0, 1, 2]

# Get all metric names
print(logger.metrics)            # ['loss', 'accuracy']

# Get full logs dictionary
full_logs = logger.get_logs()
# {'step': [0, 1, 2], 'loss': [1.0, 0.5, 0.2], 'accuracy': [0.7, 0.8, 0.9]}

# String representation
print(logger)
# <RunLogger: steps=3, metrics=['loss', 'accuracy']>
```

### Saving and Loading Experiments

```python
import json
from iragca.ml import RunLogger

# After training
logger = RunLogger(max_steps=3)
logger.log_metrics({'loss': 1.0}, step=0)
logger.log_metrics({'loss': 0.5}, step=1)
logger.log_metrics({'loss': 0.2}, step=2)

# Save logs
logs = logger.get_logs()
with open('experiment.json', 'w') as f:
    json.dump(logs, f)

# Later: Load logs
with open('experiment.json', 'r') as f:
    saved_logs = json.load(f)

restored_logger = RunLogger.from_dict(saved_logs)
print(restored_logger.loss)  # [1.0, 0.5, 0.2]
```

## Advanced Usage

### Custom Progress Bar Configuration

```python
from iragca.ml import RunLogger

logger = RunLogger(
    max_steps=100,
    display_progress=True,
    update_interval=5,  # Update progress bar every 5 steps
    tqdm_kwargs={
        'desc': 'Training',
        'unit': 'epoch',
        'ncols': 80,
    }
)

for step in range(100):
    logger.log_metrics({'loss': 1.0 / (step + 1)}, step=step)
```

## Best Practices

1. **Set accurate max_steps**: Helps the progress bar estimate time remaining
2. **Use consistent step numbering**: Steps should be in sequential order for proper sorting
3. **Export regularly**: Save logs periodically to avoid data loss
4. **Group related metrics**: Log related metrics together for easier analysis
5. **Use descriptive metric names**: Clear names make data analysis simpler

## Integration with ML Frameworks

RunLogger works seamlessly with any ML framework:

- **PyTorch**: Log metrics in training loops
- **TensorFlow/Keras**: Custom callbacks can use RunLogger
- **Scikit-learn**: Track cross-validation scores
- **Custom training loops**: Direct metric logging
