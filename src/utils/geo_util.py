import random
import string


class GeoUtil:
    @staticmethod
    def generate_random_code(length: int = 5) -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    
    @staticmethod
    def clean_code(code: str) -> str:
        if not code:
            return ''
        return code.replace('-', '').replace(' ', '')
    
    @staticmethod
    def validate_coordinates(lgtd: float, lttd: float) -> bool:
        if lgtd < -180 or lgtd > 180:
            return False
        if lttd < -90 or lttd > 90:
            return False
        return True
