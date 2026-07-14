import re
from typing import Generator, Dict, Optional

# Standart Nginx/Apache Combined Log formatı üçün REGEX şablonu
LOG_PATTERN = r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\d+)'

def parse_log_line(line: str) -> Optional[Dict]:
    """Bir sətir loqu oxuyub dictionary-ə çevirir."""
    match = re.match(LOG_PATTERN, line.strip())
    if match:
        data = match.groupdict()
        data['status'] = int(data['status'])
        data['size'] = int(data['size']) if data['size'] != '-' else 0
        return data
    return None

def stream_log_file(file_path: str) -> Generator[Dict, None, None]:
    """Böyük faylları RAM-ı doldurmadan axın (stream) şəklində oxuyur."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                yield parsed
