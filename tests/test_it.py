import textwrap

import pytest
from docutils import frontend, parsers, utils
from docutils.parsers.rst import directives
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
    {
        "provider_name": "Reddit",
        "provider_url": "https://reddit.com/",
        "endpoints": [
            {
                "schemes": [
                    "https://reddit.com/r/*/comments/*/*",
                    "https://www.reddit.com/r/*/comments/*/*",
                ],
                "url": "https://www.reddit.com/oembed",
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


def test_directive__useragent(monkeypatch: MonkeyPatch, caplog):

    source = textwrap.dedent(
        """
    .. oembed:: https://www.reddit.com/r/Python/comments/vdopqj/sphinxrevealjs_html_presentation_builder_for/
    """
    )
    monkeypatch.setattr(oembed, "load_providers", lambda: stub_providers)
    directives.register_directive("oembed", oembed.OembedDirective)
    parser = parsers.get_parser_class("rst")()
    document = utils.new_document(
        "test", frontend.OptionParser(components=(parser,)).get_default_values()
    )
    parser.parse(source, document)
    assert not caplog.records
