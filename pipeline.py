import pyarrow as pa
from fondant.pipeline import Pipeline
from fondant.component import PandasTransformComponent
from fondant.pipeline import lightweight_component
import pandas as pd

# create a new pipeline
pipeline = Pipeline(
	name="feature_extraction_pipeline",
	base_path=".fondant",
	description="A pipeline to extract features from protein sequences."
)

# generate mock data
pd.DataFrame({
	"sequence": [
		"MKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKED",
		"MHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKED",
		"MTRDADDVAVVNYANLQGKLSKEDKKPEVKQVYRITELRLTRDADDVAVVNYANL"
	]
}).to_parquet("./data/mock_data.parquet")

# read the dataset
dataset = pipeline.read(
	"load_from_parquet",
	arguments={
		"dataset_uri": "/data/mock_data.parquet",
	},
	produces={
		"sequence": pa.string()
	}
)

_ = dataset.apply(
	"./components/checksum_component",
).apply(
	"./components/biopython_component",
).apply(
	"./components/other_component",
)
