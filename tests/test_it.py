import pytest
from pytest import MonkeyPatch
from sphinxcontrib import oembed

stub_providers = [
    {
        "provider_url": "https://spotify.com/",
        "endpoints": [
            {
                "schemes": [
                    "https://open.spotify.com/*",
                ],
                "url": "https://open.spotify.com/oembed/",
            }
        ],
    },
    {
        "provider_url": "https://www.beautiful.ai/",
        "endpoints": [
            {
                "url": "https://www.beautiful.ai/api/oembed",
            }
        ],
    },
]


def test_loadable():
    result = oembed.load_providers()
    assert isinstance(result, list)


def test_find_endpoint__found(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    endpoint = oembed.find_endpoint("https://open.spotify.com/hello")
    assert endpoint == "https://open.spotify.com/oembed/"


def test_find_endpoint__not_found(monkeypatch: MonkeyPatch, caplog):
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    with pytest.raises(oembed.EndpointNotFound) as err:
        oembed.find_endpoint("https://example.com")
    assert "Endpoint for URL is not found" in str(err)


def test_find_endpoint__no_schemes(monkeypatch: MonkeyPatch, caplog):
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    endpoint = oembed.find_endpoint("https://www.beautiful.ai/deck/dummy")
    assert endpoint == "https://www.beautiful.ai/api/oembed"
