from pyspark.sql import functions as F
from pyspark.sql.functions import from_unixtime
from pyspark.sql import DataFrame


def prepare_training_data(df: DataFrame):
    df_split = df.withColumn(
        "uuid", F.col("datastream_metadata.uuid")
    ).withColumn(
        "source_timestamp_from_metadata", F.col("datastream_metadata.source_timestamp")
    )
    df = df_split.withColumn(
        "source_date", from_unixtime(F.col("source_timestamp_from_metadata").cast("long") / 1000)
    )
    df = df.select("wallet_address", "contract_address", "total_amount_0", "total_amount_usd", "uuid", "source_date")#.show(truncate=False)
    df = df.filter((F.col("source_date") >= "2023-01-01 00:00:00") & (F.col("source_date") <= "2024-11-15 00:00:00"))
    # df = df.limit(10000)
    df = df.orderBy(["source_date", "wallet_address", "contract_address"])
    df = df.withColumnRenamed(f"source_date", f"_time")

    t_window = F.window(F.col("_time"), windowDuration="15 minutes", slideDuration="1 minute").alias("window")
    df_t = (
        df.groupBy(t_window)
        .agg(F.last("wallet_address").alias("xxx"))
        .withColumn("_time", F.col("window.end"))
        .drop("window")
        .orderBy("_time")
        .select("_time")
    )

    # w = 60
    windows = [5, 15,60, 240] #
    for w in windows:
        fwindow = F.window(
            F.col("_time"),
            windowDuration=f"{w} minutes",
            slideDuration=f"1 minute",
        ).alias("window")
        df_x = (
            df.groupBy(fwindow).agg(
                F.countDistinct("wallet_address").alias(f"wallet"+f"_{w}min_"+"nunique"),
                F.countDistinct("contract_address").alias(f"contract"+f"_{w}min_"+"nunique"),
                F.countDistinct("uuid").alias(f"uuid"+f"_{w}min_"+"nunique"),
                F.sum("total_amount_usd").alias(f"usd"+f"_{w}min_"+"sum"),
                F.stddev("total_amount_usd").alias(f"usd"+f"_{w}min_"+"stddev"),
            )
            .withColumn("_time", F.col("window.start"))
            .drop("window")
        )
        df_t = df_t.join(df_x, on=["_time"], how="left")

    return df
