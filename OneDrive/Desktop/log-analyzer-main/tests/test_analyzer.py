import pytest
from src.parser import parse_log_line
from src.analyzer import analyze_logs

def test_parse_log_line():
    log_line = '192.168.1.1 - - [10/Jul/2026:12:00:01 +0400] "GET /index.html HTTP/1.1" 200 1024'
    parsed = parse_log_line(log_line)
    assert parsed is not None
    assert parsed['ip'] == '192.168.1.1'
    assert parsed['status'] == 200
    assert parsed['size'] == 1024

def test_analyze_logs():
    mock_logs = [
        {'ip': '1.1.1.1', 'status': 200, 'url': '/home', 'size': 500},
        {'ip': '1.1.1.1', 'status': 401, 'url': '/admin', 'size': 0}
    ]
    report = analyze_logs(mock_logs)
    assert report['metrics']['total_requests'] == 2
    assert report['metrics']['status_codes'][401] == 1
