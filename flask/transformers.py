from sklearn.base import BaseEstimator, TransformerMixin  
from sklearn.preprocessing import  MultiLabelBinarizer, StandardScaler, MinMaxScaler

class MultiLabelBinarizerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mlb = MultiLabelBinarizer()

    def fit(self, X, y=None):
        self.mlb.fit(X)
        return self

    def transform(self, X):
        return self.mlb.transform(X)