"""
The BiopythonComponent class is a component that takes in a dataframe, performs the Biopython functions to generate new features and returns the dataframe with the new features added.
"""
import logging
import pandas as pd
from fondant.component import PandasTransformComponent
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Set up logging
logger = logging.getLogger(__name__)


class BiopythonComponent(PandasTransformComponent):
	"""The BiopythonComponent class is a component that takes in a dataframe, performs the Biopython functions to generate new features and returns the dataframe with the new features added."""

	def __init__(self, *_):
		pass

	def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:

		sequence_analysis = dataframe["sequence"].apply(ProteinAnalysis)
		dataframe["molecular_weight"] = sequence_analysis.apply(lambda x: x.molecular_weight())

		return dataframe
