from unittest.mock import MagicMock

import pytest

from iragca.ml import RunLogger


def test_initial_state():
    logger = RunLogger(max_steps=10)
    assert logger.history == {}
    assert logger.steps == []
    assert "empty" in repr(logger)


def test_log_single_step_metrics():
    logger = RunLogger(max_steps=10)

    logger.log_metrics({"loss": 0.5, "acc": 0.9}, step=0)

    assert logger.history[0]["loss"] == 0.5
    assert logger.history[0]["acc"] == 0.9
    assert logger.steps == [0]

    # dynamic properties
    assert logger.loss == [0.5]
    assert logger.acc == [0.9]


def test_log_multiple_steps():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 0.5}, 0)
    logger.log_metrics({"loss": 0.4}, 1)
    logger.log_metrics({"loss": 0.3}, 2)

    assert logger.loss == [0.5, 0.4, 0.3]
    assert logger.steps == [0, 1, 2]


def test_updating_metrics_for_same_step():
    logger = RunLogger(max_steps=10)

    logger.log_metrics({"loss": 0.5}, step=0)
    logger.log_metrics({"acc": 0.8}, step=0)

    assert logger.history[0]["loss"] == 0.5
    assert logger.history[0]["acc"] == 0.8

    assert logger.loss == [0.5]
    assert logger.acc == [0.8]


def test_dynamic_metric_property_created_once():
    logger = RunLogger(max_steps=10)

    logger.add_metric_property("x")

    with pytest.raises(AttributeError):
        logger.add_metric_property("x")


def test_get_logs_empty():
    logger = RunLogger(max_steps=10)
    logs = logger.get_logs()

    assert logs == {"step": [], "metrics": {}}


def test_get_logs_full():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 1.0, "acc": 0.5}, step=0)
    logger.log_metrics({"loss": 0.8, "acc": 0.6}, step=1)

    logs = logger.get_logs()

    assert logs["step"] == [0, 1]
    assert logs["loss"] == [1.0, 0.8]
    assert logs["acc"] == [0.5, 0.6]


def test_getattr_dynamic_fallback():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 1.0}, 0)
    logger.log_metrics({"loss": 0.8}, 1)

    assert logger.loss == [1.0, 0.8]


def test_getattr_unknown_metric_raises():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 1.0}, 0)

    with pytest.raises(AttributeError):
        _ = logger.not_a_metric


def test_steps_sorted():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 0.5}, 2)
    logger.log_metrics({"loss": 0.4}, 0)
    logger.log_metrics({"loss": 0.3}, 1)
    assert logger.steps == [0, 1, 2]


def test_repr_nonempty():
    logger = RunLogger(max_steps=10)
    logger.log_metrics({"loss": 0.5, "acc": 0.7}, 0)

    output = repr(logger)
    assert "steps=1" in output
    assert "metrics=['loss', 'acc']" in output or "metrics=['acc', 'loss']" in output


def test_progress_bar_updates(monkeypatch):
    mock_pbar = MagicMock()
    mock_pbar.n = 0

    # Patch tqdm inside RunLogger for this test
    monkeypatch.setattr("iragca.ml.runlogger.tqdm", lambda total: mock_pbar)

    logger = RunLogger(max_steps=10, display_progress=True)
    logger.log_metrics({"loss": 0.3}, 0)

    mock_pbar.update.assert_called_once_with(1)
    mock_pbar.set_postfix.assert_called_once()


def test_progress_bar_closes_at_max_steps():
    logger = RunLogger(max_steps=3, display_progress=True)

    logger.pbar = MagicMock()
    logger.pbar.n = 0

    for step in range(3):
        logger.pbar.n += 1
        logger.log_metrics({"loss": 0.3}, step)

    logger.pbar.close.assert_called_once()
    assert not logger._display_progress


def test_update_interval():
    logger = RunLogger(max_steps=10, display_progress=True, update_interval=2)

    logger.pbar = MagicMock()
    logger.pbar.n = 0

    for step in range(5):
        logger.pbar.n += 1
        logger.log_metrics({"loss": 0.3}, step)

    assert logger.pbar.set_postfix.call_count == 3  # Called at steps 0, 2, 4


def test_create_from_dict():
    data = {
        "step": [0, 1],
        "loss": [1.0, 0.8],
        "acc": [0.5, 0.6],
    }
    logger = RunLogger.from_dict(data)

    assert logger.loss == [1.0, 0.8]
    assert logger.acc == [0.5, 0.6]
    assert logger.steps == [0, 1]


def test_metrics_property():
    logger = RunLogger(max_steps=10)

    logger.log_metrics({"loss": 1.0, "acc": 0.5}, step=0)
    logger.log_metrics({"loss": 0.8, "acc": 0.6}, step=1)
    
    assert "loss" in logger.metrics
    assert "acc" in logger.metrics
    assert len(logger.metrics) == 2
