import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load reporting data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)

        if data.empty:
            raise ValueError("The CSV file contains no data.")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")

    except pd.errors.ParserError:
        raise ValueError("Unable to parse the CSV file.")