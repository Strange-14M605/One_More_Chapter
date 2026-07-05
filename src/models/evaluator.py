import json
import pandas as pd
from pathlib import Path

class Evaluator:

    def evaluate(self, recommendations: pd.DataFrame, books: pd.DataFrame) -> dict:
        metrics = {}

        metrics.update(self.evaluate_summary(recommendations))
        metrics.update(self.evaluate_coverage(recommendations, books))
        # just add more values to the metrics json as needed for the model
        # todo: pass model type and add conditionals for different model types to evaluate different metrics

        return metrics

    def evaluate_summary(self, recommendations: pd.DataFrame) -> dict:
        return {
            "average_rating": recommendations["Average_Rating"].mean(),
            "median_rating": recommendations["Average_Rating"].median(),
            "average_rating_count": recommendations["Number_of_Ratings"].mean(),
            "highest_rating": recommendations["Average_Rating"].max(),
            "lowest_rating": recommendations["Average_Rating"].min(),
        }

    def evaluate_coverage(
        self,
        recommendations: pd.DataFrame,
        books: pd.DataFrame,
    ) -> dict:

        total_books = len(books)
        recommended_books = len(recommendations)

        return {
            "total_books": total_books,
            "recommended_books": recommended_books,
            "coverage": recommended_books / total_books,
        }

    def save(self, metrics: dict, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(metrics, f, indent=4)

    def display(self, metrics: dict):
        print("\n========== EVALUATION ==========\n")

        for key, value in metrics.items():
            if isinstance(value, float):
                if "coverage" in key:
                    print(f"{key:25}: {value:.2%}")
                else:
                    print(f"{key:25}: {value:.2f}")
            else:
                print(f"{key:25}: {value}")