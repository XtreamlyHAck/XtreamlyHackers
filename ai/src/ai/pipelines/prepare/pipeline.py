from kedro.pipeline import Pipeline, pipeline, node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=lambda node: node.__name__,
            inputs=["uniswap_v3_trader_raw"],
            outputs=["uniswap_v3_prepared"],
        )
    ])
