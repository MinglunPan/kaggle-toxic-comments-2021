# from sklearn.pipeline import Pipeline, FeatureUnion
# from sklearn.base import TransformerMixin, BaseEstimator
# from scipy import sparse

# class LengthTransformer(BaseEstimator, TransformerMixin):

#     def fit(self, X, y=None):
#         return self
#     def transform(self, X):
#         return sparse.csr_matrix([[(len(x)-360)/550] for x in X])
#     def get_feature_names(self):
#         return ["lngth"]
    
# features = FeatureUnion([
#     ('vect1', LengthTransformer()),
#     #('vect2', LengthUpperTransformer()),
#     ("vect3", TfidfVectorizer(min_df= 3, max_df=0.5, analyzer = 'char_wb', ngram_range = (3,5))),
#     #("vect4", TfidfVectorizer(min_df= 5, max_df=0.5, analyzer = 'word', token_pattern=r'(?u)\b\w{8,}\b')),

# ])
# pipeline = Pipeline(
#     [
#         ("features", features),
#         #("clf", RandomForestRegressor(n_estimators = 5, min_sample_leaf=3)),
#         ("clf", Ridge()),
#         #("clf",LinearRegression())
#     ]
#     )

# ## Weights of features
# feature_wts = sorted(list(zip(pipeline['features'].get_feature_names(), 
#                                   np.round(pipeline['clf'].coef_,2) )), 
#                          key = lambda x:x[1], 
#                          reverse=True)
