import pandas as pd
import numpy as np


def table_data_to_frame(data):
  df = pd.DataFrame(data)
  df.replace('', np.nan, inplace=True)
  df.dropna(inplace=True)
  return df
