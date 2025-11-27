import csv
import os
from typing import Dict, List


class CSVReader:
    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV-файл не найден: {csv_path}")
        self.csv_path = csv_path
    
    def read(self) -> List[Dict[str, str]]:
        rows = []
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

