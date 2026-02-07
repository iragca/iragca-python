---
hide:
  - navigation
  - toc
---


# Basic Examples

**Log training metrics with RunLogger:**

```python
from iragca.ml import RunLogger

logger = RunLogger(max_steps=100, display_progress=True)
for epoch in range(100):
    loss = 1.0 / (epoch + 1)
    logger.log_metrics({'loss': loss}, step=epoch)

print(f"Final loss: {logger.loss[-1]}")
```

**Create accessible visualizations:**

```python
from iragca.matplotlib import Color
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3], color=Color.BLUE.value)
plt.scatter([1, 2, 3, 4], [1, 4, 2, 3], color=Color.ORANGE.value)
plt.show()
```

**Build data pipelines:**

```python
from iragca.functional import Pipeline, Step

pipeline = Pipeline([
    lambda x: x * 2,
    Step(lambda x, n: x + n, n=10),
    lambda x: x ** 2,
])

result = pipeline(5)  # (5 * 2 + 10)^2 = 400
```
