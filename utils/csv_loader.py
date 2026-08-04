import pandas as pd


def load_csv(csv_path: str):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1",
    ]

    separators = [
        ",",
        ";",
        "\t",
        "|",
    ]

    last_error = None

    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(
                    csv_path,
                    encoding=encoding,
                    sep=sep,
                    low_memory=False
                )

                # Skip if it looks like everything became one column
                if len(df.columns) <= 1:
                    continue

                print(f"Loaded using encoding={encoding}, separator='{sep}'")
                return df

            except Exception as e:
                last_error = e

    raise ValueError(
        f"Unable to read CSV.\n{last_error}"
    )