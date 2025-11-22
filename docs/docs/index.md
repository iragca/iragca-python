# Home

My library of custom python scripts and configurations.

---

## Features

- Custom matplotlib plotting styles and colors

## Installation

To install using [pip](https://pypi.org/project/pip/), run:

```bash
pip install iragca
```

Only install the matplotlib scripts

```bash
pip install iragca[matplotlib]
```

## Example Usage

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

<img src="/images/sample_plot.png" width=300>
