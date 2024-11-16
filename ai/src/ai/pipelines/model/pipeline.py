from kedro.pipeline import Pipeline, pipeline, node
from .nodes import generate_features, train


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=generate_features,
            inputs=["uniswap_v3_prepared"],
            outputs=["X", "Y"],
        ),
        node(
            func=train,
            inputs=["X", "Y"],
            outputs=["model_trained"],
        )
    ])
