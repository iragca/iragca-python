import warnings

from iragca.warnings import deprecated


def test_deprecated_decorator_warns(monkeypatch):
    @deprecated("Use `new_func` instead.")
    def old_func(x, y):
        return x + y

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = old_func(1, 2)
        assert result == 3
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "old_func is deprecated. Use `new_func` instead." in str(w[0].message)


def test_deprecated_decorator_warns_without_reason():
    @deprecated()
    def old_func(x):
        return x * 2

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = old_func(5)
        assert result == 10
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "old_func is deprecated." in str(w[0].message)


def test_deprecated_decorator_preserves_function_metadata():
    @deprecated("test")
    def func(a, b):
        """Docstring"""
        return a - b

    assert func.__name__ == "func"
    assert func.__doc__ == "Docstring"
