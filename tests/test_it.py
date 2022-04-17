import pytest
from pytest import MonkeyPatch
from sphinxcontrib import oembed

stub_providers = [
    {
        "endpoints": [
            {
                "schemes": [
                    "https://open.spotify.com/*",
                ],
                "url": "https://open.spotify.com/oembed/",
            }
        ]
    },
]


def test_find_endpoint__found(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    endpoint = oembed.find_endpoint("https://open.spotify.com/hello")
    assert endpoint == "https://open.spotify.com/oembed/"


def test_find_endpoint__not_found(monkeypatch: MonkeyPatch, caplog):
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    with pytest.raises(oembed.EndpointNotFound) as err:
        oembed.find_endpoint("https://example.com")
    assert "Endpoint for URL is not found" in str(err)
