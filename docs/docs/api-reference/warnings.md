# Warnings Module

The `warnings` module provides utilities for managing and marking deprecations in your codebase.

## Functions

### deprecated

```markdown
::: iragca.warnings.deprecated
```

## Overview

The `warnings` module helps maintain clean APIs by:

- **Marking deprecations**: Clearly indicate which functions or methods are obsolete
- **Guiding users**: Provide helpful migration paths and alternatives
- **Tracking removals**: Document when and why features were deprecated

## Examples

### Basic Deprecation

```python
from iragca.warnings import deprecated

@deprecated("Use `new_function` instead.")
def old_function(x, y):
    return x + y

# Calling the function issues a DeprecationWarning
result = old_function(1, 2)  # Returns 3 with warning
```

### Output

When you call a deprecated function:

```
__main__:1: DeprecationWarning: old_function is deprecated. Use `new_function` instead.
```

### Deprecating Methods

```python
from iragca.warnings import deprecated

class MyClass:
    @deprecated("Use `compute_new` instead.")
    def compute_old(self, x):
        return x * 2

obj = MyClass()
result = obj.compute_old(5)  # Issues DeprecationWarning
```

### No Guidance (Optional)

You can deprecate without providing migration guidance:

```python
from iragca.warnings import deprecated

@deprecated()
def obsolete_function():
    return "This is gone soon"
```

## Warning Behavior

- **Category**: `DeprecationWarning`
- **Stack Level**: 2 (points to caller's code, not the decorator)
- **Persistence**: Warnings are shown every time the function is called

## Filtering Deprecation Warnings

Users can control how deprecation warnings are displayed:

```python
import warnings

# Show all warnings (default)
warnings.simplefilter("always")

# Show each warning only once per location
warnings.simplefilter("once")

# Suppress all deprecation warnings
warnings.simplefilter("ignore", DeprecationWarning)
```

## Best Practices

1. **Be descriptive**: Provide clear guidance on alternatives
2. **Version early**: Mark functions as deprecated before removal
3. **Include migration path**: Tell users what to use instead
4. **Set removal timeline**: Indicate when the deprecated function will be removed

```python
@deprecated("Deprecated in v1.5. Use `improved_function` instead. Will be removed in v2.0.")
def legacy_function():
    pass
```
