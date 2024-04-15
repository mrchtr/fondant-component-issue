import pyarrow as pa
from fondant.pipeline import Pipeline
import dask.dataframe as dd
import pandas as pd
from fondant.pipeline import lightweight_component
from fondant.component import DaskLoadComponent, PandasTransformComponent

# create a new pipeline
pipeline = Pipeline(
	name="test_pipeline",
	base_path=".fondant",
	description="A pipeline to extract features from protein sequences."
)

@lightweight_component(
    base_image="fndnt/fondant:0.11.dev5-py3.10"
)
class InitDataset(DaskLoadComponent):
    def __init__(self):
        pass
    def load(self) -> dd.DataFrame:
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "sequence": [
                "MKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKED",
                "MHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKED",
                "MTRDADDVAVVNYANLQGKLSKEDKKPEVKQVYRITELRLTRDADDVAVVNYANLMHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKEDMHVKLDRGKTLVQRTDQIYKKPEVHVKLDRGKTLVQRTDQIYKQVYRITELRLTRDADDVAVVNYANLQGKLSKED"
            ]
        })

        ddf = dd.from_pandas(df, npartitions=1)
        ddf["id"] = ddf["id"].astype(str)
        ddf = ddf.set_index("id")
        return ddf


@lightweight_component(
    base_image="fndnt/fondant:0.11.dev5-py3.10",
    extra_requires=["biopython==1.83"]
)
class BioPythonComponent(PandasTransformComponent):
    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        sequence_analysis = dataframe["sequence"].apply(ProteinAnalysis)
        dataframe["molecular_weight"] = sequence_analysis.apply(lambda x: x.molecular_weight())
        print(dataframe.head())
        return dataframe

@lightweight_component(
    base_image="fndnt/fondant:0.11.dev5-py3.10",
    extra_requires=["biopython==1.83"]
)
class ChecksumComponent(PandasTransformComponent):
    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        from Bio.SeqUtils.CheckSum import crc64
        dataframe["sequence_checksum"] = dataframe["sequence"].apply(crc64).astype(str)
        print(dataframe.head())
        return dataframe


# read the dataset
dataset = pipeline.read(
	InitDataset,
	produces={
		"sequence": pa.string()
	}
)

dataset.apply(
    BioPythonComponent,
    produces={
        "molecular_weight": pa.float64()
    }
).apply(
	ChecksumComponent,
    produces={
        "sequence_checksum": pa.string()
    }
).write(
	"write_to_file",
	arguments={
		"path":"/data/export"
	},
)
