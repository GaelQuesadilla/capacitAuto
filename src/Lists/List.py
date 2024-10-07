from src.FileManager.AskFile import askPath
import pandas as pd
from src.Log import Log


class List:
    def __init__(self, fileName: str, df: pd.DataFrame = None):
        self._fileName: str = fileName
        self._df: pd.DataFrame = df

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, fileName: str):
        if not fileName.endswith(".xlsx"):
            fileName += ".xlsx"
        self._fileName = fileName

    @property
    def df(self):
        return self._df

    def load(self):
        self._df = pd.read_excel(self.fileName)

    def save(self):
        self._df.to_excel(self._fileName, index=False)
