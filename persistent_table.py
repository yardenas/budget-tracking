import os

import pandas as pd


class PersistentTable:

  def __init__(self, name):
    self.name = name + '.json'
    if os.path.isfile(name):
      self.data = pd.read_json(self.name, lines=True)
    else:
      self.data = pd.DataFrame()

  def save(self):
    self.data.to_json(self.name, orient='records', lines=True)
