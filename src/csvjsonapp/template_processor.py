import re
from typing import Dict, Optional
from .interfaces import ITemplateProcessor


class TemplateProcessor(ITemplateProcessor):
    def process(self, template: str, data: Dict[str, str], photo_path: Optional[str] = None) -> str:
        filled_template = template
        
        for key, value in data.items():
            filled_template = filled_template.replace(f"{{{key}}}", str(value))
        
        if photo_path:
            filled_template = filled_template.replace("{photo_path}", photo_path)
        else:
            filled_template = self._remove_photo_path(filled_template)
        
        return filled_template
    
    def _remove_photo_path(self, template: str) -> str:
        template = re.sub(r',?\s*"photo_path"\s*:\s*"[^"]*"', '', template)
        template = re.sub(r',?\s*"photo_path"\s*:\s*null', '', template)
        template = re.sub(r',\s*}', '}', template)
        template = re.sub(r'{\s*,', '{', template)
        return template

