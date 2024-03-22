import logging
import pandas as pd
from fondant.component import PandasTransformComponent
from Bio.SeqUtils.CheckSum import crc64

# Set up logging
logger = logging.getLogger(__name__)

class ChecksumComponent(PandasTransformComponent):

	def __init__(self, *_):
		pass

	def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:

		dataframe['sequence_checksum'] = dataframe['sequence'].apply(crc64)
		return dataframe
