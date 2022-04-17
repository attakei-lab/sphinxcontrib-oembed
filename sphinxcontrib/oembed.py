from fnmatch import fnmatch
from functools import lru_cache
from typing import Optional

import requests
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective


logger = logging.getLogger(__name__)


class EndpointNotFound(Exception):
    pass


@lru_cache
def load_providers():
    resp = requests.get("https://oembed.com/providers.json")
    return resp.json()


@lru_cache
def find_endpoint(url) -> Optional[str]:
    for provider in load_providers():
        for endpoint in provider["endpoints"]:
            if "schemes" not in endpoint:
                if url.startswith(provider["provider_url"]):
                    return endpoint["url"]
                continue
            for scheme in endpoint["schemes"]:
                if fnmatch(url, scheme):
                    return endpoint["url"]
    raise EndpointNotFound("Endpoint for URL is not found")


class oembed(nodes.General, nodes.Element):  # noqa: D101,E501
    pass


class OembedDirective(SphinxDirective):  # noqa: D101
    has_content = False
    required_arguments = 1

    def run(self):  # noqa: D102
        node = oembed()
        url = self.arguments[0]
        try:
            endpoint = find_endpoint(url)
            resp = requests.get(endpoint, params={"url": url})
            node["content"] = resp.json()
        except EndpointNotFound as err:
            logger.warning(f"{err} at {self.get_location()} - {url}")
        return [
            node,
        ]


def visit_oembed_node(self, node):
    if "content" in node and "html" in node["content"]:
        self.body.append(node["content"]["html"])


def depart_oembed_node(self, node):
    pass


def setup(app: Sphinx):
    app.add_node(
        oembed,
        html=(visit_oembed_node, depart_oembed_node),
    )
    app.add_directive("oembed", OembedDirective)
