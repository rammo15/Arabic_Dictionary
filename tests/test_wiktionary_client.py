from unittest.mock import Mock, patch

from arabic_dictionary.providers.wiktionary.client import MediaWikiClient


@patch("arabic_dictionary.providers.wiktionary.client.requests.get")
def test_get_page(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "parse": {
            "title": "كتاب",
        }
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    client = MediaWikiClient()

    result = client.get_page("كتاب")

    assert result["parse"]["title"] == "كتاب"