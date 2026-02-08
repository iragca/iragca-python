<h1 align="center">iragca</h1>

<h3 align="center">My library of custom python scripts and configurations</h3>

---

<p align="center">

<a href="https://github.com/iragca/iragca-python">
<img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"/>
</a>
<a href="https://github.com/iragca/iragca-python/releases">
<img alt="Release" src="https://img.shields.io/github/v/release/iragca/iragca-python"/>
</a>
<a href="https://pypi.org/project/iragca/">
<img alt="PyPI" src="https://img.shields.io/badge/pypi-iragca-python?logo=pypi"/>
</a>
<a href="https://www.python.org/downloads/">
<img alt="Python Version" src="https://img.shields.io/badge/python-3.10+-blue.svg?logo=python"/>
</a>

</p>

---

`iragca-python` is a comprehensive Python library providing practical utilities for data science, machine learning, and visualization workflows. It streamlines common tasks in machine learning, data visualization, and functional programming.

## Key Features

- **Accessible Visualization**: Professional matplotlib styles and WCAG-compliant color palettes designed for clarity and accessibility.
- **Lightweight Experiment Tracking**: `RunLogger` for logging metrics with dynamic property access and optional progress bars.
- **Functional Programming Utilities**: Composable data transformation pipelines using `Pipeline` and `Step`.
- **Deprecation Management**: Tools to manage deprecations and guide users to alternatives.

## Use Cases

- **ML/DL Training**: Track metrics with `RunLogger` during training loops
- **Data Pipelines**: Build readable transformation chains with `Pipeline`
- **Publication Plots**: Create accessible visualizations with pre-configured styles
- **Library Maintenance**: Manage deprecations gracefully with proper warnings

## Installation

Install using [pip](https://pypi.org/project/pip/):

```bash
pip install iragca
```

Install a specific module (see the [docs](https://iragca.github.io/iragca-python/api-reference/) for options):

```bash
pip install iragca[functional]
```

## Quick Start

### RunLogger

```python
from iragca.ml import RunLogger

logger = RunLogger(max_steps=100, display_progress=True)
for epoch in range(100):
	loss = 1.0 / (epoch + 1)
	logger.log_metrics({'loss': loss}, step=epoch)

print(f"Final loss: {logger.loss[-1]}")
```

### Matplotlib Colors and Styles

```python
import matplotlib.pyplot as plt

from iragca.matplotlib import Color, Styles

plt.style.use(Styles.CMR10.value)

sample_data = [1, 3, 2, 4, 3, 5]

plt.plot(sample_data, color=Color.BLUE.value)
plt.title("Sample Plot with Custom Style and Color")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```

<img src="docs/docs/images/sample_plot.png" width=300>

### Functional Pipelines

```python
from iragca.functional import Pipeline, Step

pipeline = Pipeline([
	lambda x: x * 2,
	Step(lambda x, n: x + n, n=10),
	lambda x: x ** 2,
])

result = pipeline(5)  # (5 * 2 + 10)^2 = 400
```

## Documentation

Read the full documentation in the [docs](https://iragca.github.io/iragca-python/) or visit the [API reference](https://iragca.github.io/iragca-python/api-reference/).
