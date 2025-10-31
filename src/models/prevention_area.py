from dataclasses import dataclass
from typing import Optional


@dataclass
class PreventionArea:
    code: str
    name: str
    population: Optional[int] = None
    river_name: Optional[str] = None
    river_code: Optional[str] = None
    category: Optional[str] = None
    
    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'population': self.population,
            'river_name': self.river_name,
            'river_code': self.river_code,
            'category': self.category
        }
