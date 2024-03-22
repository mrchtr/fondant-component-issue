import logging
import pandas as pd
from fondant.component import PandasTransformComponent

# Set up logging
logger = logging.getLogger(__name__)


class OtherComponent(PandasTransformComponent):

	def __init__(self, *_):
		pass

	def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
		dataframe['sequence_length'] = dataframe['sequence'].apply(len)
		return dataframe