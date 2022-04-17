from fnmatch import fnmatch
from functools import lru_cache

import requests
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx


@lru_cache
def load_providers():
    resp = requests.get("https://oembed.com/providers.json")
    return resp.json()


@lru_cache
def get_service_url(url):
    for provider in load_providers():
        for endpoint in provider["endpoints"]:
            if "schemes" not in endpoint:
                continue
            for scheme in endpoint["schemes"]:
                if fnmatch(url, scheme):
                    return endpoint["url"]
    raise Exception("Service is not found")


class oembed(nodes.General, nodes.Element):  # noqa: D101,E501
    pass


class OembedDirective(Directive):  # noqa: D101
    has_content = False
    required_arguments = 1

    def run(self):  # noqa: D102
        node = oembed()
        url = self.arguments[0]
        resp = requests.get(get_service_url(url), params={"url": url})
        node["content"] = resp.json()
        return [
            node,
        ]


def visit_oembed_node(self, node):
    self.body.append(node["content"]["html"])


def depart_oembed_node(self, node):
    pass


def setup(app: Sphinx):
    app.add_node(
        oembed,
        html=(visit_oembed_node, depart_oembed_node),
    )
    app.add_directive("oembed", OembedDirective)
