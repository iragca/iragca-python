from pydantic import Field, validate_call
from tqdm import tqdm
from tqdm.notebook import tqdm as nbtqdm


class RunLogger:
    """
    A lightweight logger for tracking scalar metrics across sequential steps.

    This class provides:
    - Metric logging for arbitrary named metrics.
    - Dynamic attribute access, e.g., `logger.loss` → list of all logged loss values.
    - Optional tqdm progress bar display, with support for both console and Jupyter Notebook environments.

    Example usage
    -------------
    ```python
    from iragca.ml import RunLogger

    logger = RunLogger(max_steps=100, display_progress=True)
    for epoch in range(100):
        # Simulate logging metrics
        logger.log_metrics({'loss': 1.035, 'accuracy': 0.7728}, step=epoch)

    print(logger.loss)                #  Access logged loss values
    # [10.0, 9.9, 9.8, ..., 0.1]
    print(logger.accuracy)            #  Access logged accuracy values
    # [0.0, 0.01, 0.02, ..., 0.99]
    ```
    """

    @validate_call
    def __init__(
        self,
        max_steps: int = Field(..., ge=1),
        display_progress: bool = Field(False),
        update_interval: int = Field(1, ge=1),
        notebook: bool = Field(False),
        tqdm_kwargs: dict = Field({}),
    ):
        """
        Parameters
        ----------
        max_steps : int
            Total number of expected steps. Used for progress bar display.
        display_progress : bool, optional
            If True, a tqdm progress bar is shown during logging.
        update_interval : int, optional
            Frequency (in steps) to update the progress bar. Default is 1 (update every step).
        notebook : bool, optional
            Whether to use `tqdm.notebook.tqdm` or `tqdm.tqdm`.
        tqdm_kwargs : dict
            Key word arguments for `tqdm.tqdm`
        """
        self.history = {}
        self._display_progress = display_progress
        self._max_steps = max_steps
        self.tqdm_kwargs = tqdm_kwargs
        self._notebook = notebook

        if self._display_progress:
            self._update_interval = update_interval
            self.pbar = (
                nbtqdm(total=max_steps, **self.tqdm_kwargs)
                if notebook
                else tqdm(total=max_steps, **self.tqdm_kwargs)
            )

    def log_metrics(self, log_data: dict, step: int):
        """
        Log one or more metrics for a given step.

        Parameters
        ----------
        log_data : dict
            Dictionary mapping metric names to numeric values.
        step : int
            Index of the current step (e.g., epoch or iteration).

        Notes
        -----
        - If metrics already exist for a step, new values will update or
          extend the existing dictionary.
        - New metric names automatically become accessible as properties,
          e.g., ``logger.accuracy`` returns a list of accuracy values.
        """
        if step not in self.history:
            self.history[step] = {}

        # update metrics for this step
        for key, value in log_data.items():
            self.history[step][key] = value

            # Create metric property lazily if not present
            if not hasattr(self, key):
                self.add_metric_property(key)

        if not self._display_progress:
            return

        # update progress bar
        self.pbar.update(1)
        if step % self._update_interval == 0:
            self.pbar.set_postfix(log_data, refresh=True)

        if self.pbar.n == self._max_steps:
            self.pbar.close()
            self._display_progress = False

    def add_metric_property(self, metric_name: str):
        """
        Dynamically create a read-only property for accessing metric history.

        Parameters
        ----------
        metric_name : str
            Name of the metric to expose as a property.

        Notes
        -----
        After logging ``loss``, you can access it via ``logger.loss``.
        """
        if hasattr(self, metric_name):
            raise AttributeError(f"Attribute {metric_name!r} already exists.")

        def getter(self):
            if not self.history:
                return []
            return [self.history[step].get(metric_name) for step in sorted(self.history.keys())]

        setattr(self.__class__, metric_name, property(getter))

    def get_logs(self) -> dict:
        """
        Return all logged metrics organized by step.

        Returns
        -------
        dict
            Dictionary of the form::

                {
                    "step": [...],
                    "metric_name_1": [...],
                    "metric_name_2": [...],
                    ...
                }

            If no logs are recorded, returns::

                {
                    "step": [],
                    "metrics": {}
                }
        """
        if not self.history:
            return {"step": [], "metrics": {}}

        steps = sorted(self.history.keys())
        first_step = steps[0]

        return {
            "step": steps,
            **{
                key: [self.history[step].get(key) for step in steps]
                for key in self.history[first_step].keys()
            },
        }

    @property
    def steps(self) -> list[int]:
        """
        List[int]
            Sorted list of recorded step indices.
        """
        return sorted(self.history.keys())

    def __getattr__(self, name):
        """
        Fallback attribute access for dynamic metric lookup.

        Parameters
        ----------
        name : str
            Metric name being accessed.

        Returns
        -------
        list
            List of values for the metric across all steps.

        Raises
        ------
        AttributeError
            If the metric does not exist.
        """
        if self.history:
            steps = sorted(self.history.keys())
            if name in self.history[steps[0]]:
                return [self.history[s].get(name) for s in steps]

        raise AttributeError(f"{name!r} not found in RunLogger.")

    def __repr__(self) -> str:
        if not self.history:
            return "<RunLogger: empty>"

        steps = sorted(self.history.keys())
        first_step = steps[0]
        metrics = list(self.history[first_step].keys())
        return f"<RunLogger: steps={len(steps)}, metrics={metrics}>"

    @classmethod
    def from_dict(cls, logs: dict) -> "RunLogger":
        """
        Create a RunLogger instance from existing logs or dictionary.

        Parameters
        ----------
        logs : dict
            Dictionary of the form::

                {
                    "step": [...],
                    "metric_name_1": [...],
                    "metric_name_2": [...],
                    ...
                }

        Returns
        -------
        RunLogger
            Instance populated with the provided logs.

        Notes
        -----
        This is the inverse of the `get_logs` method.
        'step' key is required in the input dictionary.
        """
        max_steps = len(logs.get("step", []))
        logger = cls(max_steps=max_steps)

        for i, step in enumerate(logs.get("step", [])):
            log_data = {key: logs[key][i] for key in logs.keys() if key != "step"}
            logger.log_metrics(log_data, step)

        return logger

    @property
    def metrics(self) -> list[str]:
        """
        List[str]
            List of all logged metric names.
        """
        if not self.history:
            return []
        first_step = sorted(self.history.keys())[0]
        return list(self.history[first_step].keys())
