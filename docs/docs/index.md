---
hide:
  - navigation
---

# iragca-python Documentation

Welcome to the iragca-python documentation!

`iragca-python` is a comprehensive Python library providing practical utilities for data science, machine learning, and visualization workflows. Designed to streamline common tasks in machine learning, data visualization, and functional programming.

## Key Features

<div class="grid cards" markdown>

-   :lucide-chart-network:{ .lg .middle } __Accessible Visualization__

    ---

    Professional matplotlib styles and WCAG-compliant color palettes designed for clarity and accessibility. Create beautiful, inclusive data visualizations without the hassle of manual styling.

    [:octicons-arrow-right-24: matplotlib module](./api-reference/matplotlib.md)

-   :lucide-clipboard-clock:{ .lg .middle } __Lightweight Experiment Tracking__

    ---

    `RunLogger` provides a minimalist approach to tracking metrics during training. Log metrics with dynamic property access, optional progress bars, and easy export/import functionality.

    [:octicons-arrow-right-24: logger module](./api-reference/run-logger.md)

-   :lucide-square-function:{ .lg .middle } __Functional Programming Utilities__

    ---

    Build composable, readable data transformation pipelines using `Pipeline` and `Step` classes. Perfect for ETL workflows and data processing chains.

    [:octicons-arrow-right-24: functional module](./api-reference/functional.md)

-   :lucide-message-square-warning:{ .lg .middle } __Deprecation Management__

    ---

    Professional deprecation handling tools to maintain clean APIs and guide users toward better alternatives.

    [:octicons-arrow-right-24: warnings module](./api-reference/warnings.md)

</div>

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

Install a specific module. See the [relevant documentation](./api-reference/index.md#modules) for all available modules.

```bash
pip install iragca[functional]
```

