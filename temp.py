import pandas as pd

# load parquet file
df = pd.read_parquet(".fondant/test_pipeline/test_pipeline-20240415111110/checksum_component")

print(df.head())