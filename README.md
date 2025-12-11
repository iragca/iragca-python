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

Features
- Custom matplotlib plotting styles and colors
- A run logger for logging training runs in Machine/Deep learning pipelines

## Installation

To install using [pip](https://pypi.org/project/pip/), run:

```bash
pip install iragca

# Only install the matplotlib scripts
pip install iragca[matplotlib]
```

## Quick example

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