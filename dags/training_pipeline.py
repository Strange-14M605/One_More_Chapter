# TRAINING PIPELINE
# frequency: manual/weekly

# 1. load features from DuckDB
# 2. fit the model 
# 3. evaluate model perf.
# 4. save recommendations
# 5. save metrics

# Output: 
# a. artifacts/models/{model_type}/{version}/recommendations.json    -> acts as a backup of the recommendations
# b. artifacts/models/{model_type}/{version}/metrics.json            -> to compare across versions

# possible future work:
# multiple recommender algorithms
# automated retraining with MLflow model registry
# hyperparameter tuning