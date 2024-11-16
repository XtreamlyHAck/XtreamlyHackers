from kedro.pipeline import Pipeline, pipeline, node
from .nodes import prepare_training_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=prepare_training_data,
            inputs=["uniswap_v3_trader_raw"],
            outputs=["uniswap_v3_prepared"],
        )
    ])
