import pandas as pd

from memory.memory_store import MemoryStore
from models.task import Task
from utils.csv_loader import load_csv
from agents.base_agent import BaseAgent


DOMAIN_KEYWORDS = {
    "Cybersecurity": ["ip", "src", "dst", "protocol", "port", "risk", "severity", "bytes", "attacks", "action", "alert"],
    "Sales": ["sales", "customer", "product", "order", "quantity", "price", "profit", "revenue"],
    "Healthcare": ["patient", "disease", "diagnosis", "treatment", "medicine", "hospital", "doctor"],
    "Finance": ["expense", "income", "balance", "transaction", "payment", "amount", "budget", "investment"],
    "E-commerce": ["product", "category", "price", "rating", "review", "order", "customer"],
    "Education": ["student", "course", "grade", "teacher", "school", "university", "exam", "assignment"],
    "Social Media": ["post", "like", "comment", "share", "follower", "hashtag", "engagement"],
    "Manufacturing": ["production", "machine", "quality", "defect", "process", "efficiency", "inventory"],
}


class ProfilerAgent(BaseAgent):

    def __init__(self, memory: MemoryStore):
        super().__init__(memory)

    def detect_domains(self, columns):
        detected = []
        lower_columns = [c.lower() for c in columns]

        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = 0

            for keyword in keywords:
                if any(keyword in col for col in lower_columns):
                    score += 1

            if score >= 2:
                detected.append(domain)

        return detected if detected else ["Generic"]

    def calculate_outliers(self, df):
        outliers = {}

        for col in df.select_dtypes(include="number").columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers[col] = int(((df[col] < lower) | (df[col] > upper)).sum())

        return outliers

    def get_top_categories(self, df):
        summary = {}

        for col in df.select_dtypes(include="object").columns:
            summary[col] = (
                df[col]
                .value_counts(dropna=False)
                .head(5)
                .to_dict()
            )

        return summary

    def execute(self, task: Task):

        csv_path = self.memory.get_dataset("path")
        if csv_path is None:
            raise ValueError("Dataset path not found in shared memory.")
        df = load_csv(csv_path)

        for column in df.select_dtypes(include=["object"]).columns:
            try:
                converted = pd.to_datetime(df[column], errors="coerce")

                if converted.notna().sum() >= len(df) * 0.8:
                    df[column] = converted

            except Exception:
                pass

        column_groups = {
            "numerical": df.select_dtypes(include="number").columns.tolist(),
            "categorical": df.select_dtypes(include="object").columns.tolist(),
            "datetime": df.select_dtypes(include="datetime").columns.tolist(),
            "boolean": df.select_dtypes(include="bool").columns.tolist(),
        }

        numeric_df = df.select_dtypes(include="number")

        profile = {
            "dataset_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "duplicate_rows": int(df.duplicated().sum()),
            },
            "schema": {
                "column_names": list(df.columns),
                "data_types": df.dtypes.astype(str).to_dict(),
            },
            "column_groups": column_groups,
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (
                (df.isnull().sum() / len(df)) * 100
            ).round(2).to_dict(),
            "possible_domains": self.detect_domains(df.columns),
            "outliers": self.calculate_outliers(df),
            "top_categories": self.get_top_categories(df),
        }

        self.memory.store_dataset("dataframe", df)

        # Store profile in both dataset and analysis memory
        self.memory.store_dataset("profile", profile)
        self.memory.store_analysis("profile", profile)

        return profile