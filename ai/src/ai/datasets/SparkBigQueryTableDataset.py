from kedro.io.core import AbstractDataset
from typing import Any, NoReturn, List
from xtreamly_data_platform.utils.spark import get_spark
from pyspark.sql import DataFrame
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from pyspark.sql.functions import min, max


class SparkBigQueryTableDataset(AbstractDataset[Any, DataFrame]):
    # More details here: https://github.com/GoogleCloudDataproc/spark-bigquery-connector/blob/master/README.md
    def __init__(
        self,
        project_id: str,
        table: str,
        mode: str = 'overwrite_partitions',
        partition_field: str = None,
        partition_type: str = None,
        clusters: List[str] = None,
    ):
        self.project_id = project_id
        self.table = table
        self.mode = mode
        self.partition_field = partition_field
        self.partition_type = partition_type
        self.clusters = clusters
        self._full_table = f"{project_id}:{table}"

    def _load(self) -> DataFrame:
        return get_spark().read \
            .format("bigquery") \
            .option("table", self._full_table) \
            .load()

    def create_conditions_string(self, df: DataFrame):
        conditions = []

        for col in self.clusters:
            values = df.select(col).distinct().rdd.flatMap(lambda x: x).collect()
            values = [f"'{v}'" for v in values]
            cond = f"CAST({col} as STRING) in ({','.join(values)})"
            conditions.append(cond)

        return " and ".join(conditions)

    def _save(self, data: DataFrame) -> NoReturn:
        if data.isEmpty():
            return

        if self.mode == "overwrite_partitions" is not None and self.exists():
            conditions = []
            if self.clusters:
                conditions.append(self.create_conditions_string(data))

            if self.partition_field in data.columns:
                min_max_timestamps = data.agg(
                    min(self.partition_field).alias("min_ts"),
                    max(self.partition_field).alias("max_ts")
                ).collect()[0]

                min_ts = min_max_timestamps["min_ts"]
                max_ts = min_max_timestamps["max_ts"]

                conditions.append(f"{self.partition_field} BETWEEN '{min_ts}' AND '{max_ts}'")

            if len(conditions) > 0:
                conditions = " AND ".join(conditions)
                delete_query = f"DELETE FROM `{self.project_id}.{self.table}` WHERE " + conditions
                bigquery.Client().query(delete_query).result()

        mode = "append" if self.mode == "overwrite_partitions" else self.mode
        cmd = data.write \
            .format("bigquery") \
            .option("allowFieldRelaxation", "true") \
            .option("table", self._full_table) \
            .mode(mode)

        if self.partition_field in data.columns:
            cmd = cmd.option("partitionField", self.partition_field)
            if self.partition_type is not None:
                cmd = cmd.option("partitionType", self.partition_type)

        if self.clusters is not None:
            cmd = cmd.option("clusteredFields", ",".join(self.clusters))

        cmd.save()

    def _exists(self) -> bool:
        try:
            bigquery.Client().get_table(f"{self.project_id}.{self.table}")
            return True
        except NotFound:
            return False

    def _describe(self):
        return dict(
            project_id=self.project_id,
            table=self.table,
            mode=self.mode,
            partition_field=self.partition_field,
            partition_type=self.partition_type,
            clusters=self.clusters,
        )
