import pytest
from webguard.checker import normalize_url

def test_https_url():
    assert normalize_url('https://example.com') == 'https://example.com'

def test_adds_https():
    assert normalize_url('example.com') == 'https://example.com'

@pytest.mark.parametrize('value', ['', 'ftp://example.com', 'https://user:pass@example.com'])
def test_rejects_bad_urls(value):
    with pytest.raises(ValueError):
        normalize_url(value)
