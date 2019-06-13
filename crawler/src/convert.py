import sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


input_file = sys.argv[1]
output_dir = sys.argv[2]


data_type = {
    'id': int,
    'retweet_count': int,
    'full_text': str,
    'created_at': str
}

data_frame = pd.read_json(
        path_or_buf=input_file,
        dtype=data_type,
        lines=True
    )

table = pa.Table.from_pandas(df=data_frame)

pq.write_to_dataset(
        table,
        output_dir,
        compression='snappy'
    )
