from kedro.pipeline import Pipeline, pipeline, node
from .nodes import reporting


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=reporting,
            inputs=["model_trained", "uniswap_v3_trader_raw"],
            outputs=["reporting_done"],
        )
    ])
