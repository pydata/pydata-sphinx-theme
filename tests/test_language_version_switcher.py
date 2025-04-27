import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def sample_html():
    return '''
    <div class="navbar-switcher">
      <select id="language-switcher">
        <option value="en" selected>English</option>
        <option value="ja">日本語</option>
      </select>
      <select id="version-switcher">
        <option value="https://example.com/en/latest/" selected>Latest</option>
        <option value="https://example.com/en/stable/">Stable</option>
      </select>
    </div>
    '''

def test_language_switcher(sample_html):
    soup = BeautifulSoup(sample_html, 'html.parser')
    language_switcher = soup.find(id="language-switcher")
    assert language_switcher is not None
    options = language_switcher.find_all('option')
    assert len(options) == 2
    assert options[0]['value'] == 'en'
    assert options[1]['value'] == 'ja'

def test_version_switcher(sample_html):
    soup = BeautifulSoup(sample_html, 'html.parser')
    version_switcher = soup.find(id="version-switcher")
    assert version_switcher is not None
    options = version_switcher.find_all('option')
    assert len(options) == 2
    assert options[0]['value'] == 'https://example.com/en/latest/'
    assert options[1]['value'] == 'https://example.com/en/stable/'