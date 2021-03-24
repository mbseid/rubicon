from sklearn.pipeline import Pipeline

from rubicon.sklearn import get_logger


class RubiconPipeline(Pipeline):
    def __init__(self, steps, project, memory=None, verbose=False):
        self.project = project
        self.experiment = project.log_experiment("Logged from a RubiconPipeline")

        super().__init__(steps, memory=memory, verbose=verbose)

    def fit(self, X, y=None, tags=None, **fit_params):
        pipeline = super().fit(X, y, **fit_params)

        # empty experiments are being logged during
        # the grid search run so using tags to track
        # the relevant data
        if tags is not None:
            self.experiment.add_tags(tags)

        for step_name, estimator in self.steps:
            logger_cls = get_logger(estimator.__class__.__name__)
            logger = logger_cls(self.experiment, step_name)

            logger.log(parameters=estimator.get_params())

        return pipeline

    def score(self, X, y=None, sample_weight=None):
        score = super().score(X, y, sample_weight)

        self.experiment.log_metric("accuracy", value=score)

        return score
