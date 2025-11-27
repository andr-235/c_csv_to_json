import json
import os
from pathlib import Path
from typing import Optional
from csvjsonapp.interfaces import IPhotoFinder, ITemplateProcessor, ILogger
from csvjsonapp.csv_reader import CSVReader
from csvjsonapp.json_writer import JSONFileWriter


class JSONGenerator:
    def __init__(
        self,
        template_processor: ITemplateProcessor,
        photo_finder: IPhotoFinder,
        logger: ILogger
    ):
        self.template_processor = template_processor
        self.photo_finder = photo_finder
        self.logger = logger
    
    def generate(
        self,
        csv_path: str,
        photos_folder: Optional[str],
        template_str: str
    ) -> tuple[int, int]:
        try:
            csv_reader = CSVReader(csv_path)
            rows = csv_reader.read()
        except Exception as e:
            self.logger.log(f"Ошибка при чтении CSV: {e}")
            return 0, 1
        
        photos_path = Path(photos_folder) if photos_folder and os.path.exists(photos_folder) else None
        writer = JSONFileWriter()
        
        created_count = 0
        error_count = 0
        
        for row in rows:
            try:
                if "id" not in row:
                    self.logger.log("Ошибка: В CSV отсутствует колонка 'id'")
                    error_count += 1
                    continue
                
                photo_name = row.get("photo", "")
                found_photo = ""
                if photo_name and photos_path:
                    found_photo = self.photo_finder.find(photo_name, photos_path)
                
                processed_template = self.template_processor.process(
                    template_str,
                    row,
                    found_photo if found_photo else None
                )
                
                try:
                    result = json.loads(processed_template)
                except json.JSONDecodeError as e:
                    self.logger.log(f"Ошибка JSON для строки {row.get('id', 'unknown')}: {e}")
                    error_count += 1
                    continue
                
                writer.write(f"{row['id']}.json", result)
                created_count += 1
                
            except Exception as e:
                error_count += 1
                self.logger.log(f"Ошибка при обработке строки: {e}")
        
        return created_count, error_count

