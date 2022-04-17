import re
import requests
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx


SERVICES = {
    r"^https://speakerdeck.com": "https://speakerdeck.com/oembed.json",
    r"^https://twitter.com": "https://publish.twitter.com/oembed",
}


def get_service_url(url):
    for pattern, endpoint in SERVICES.items():
        if re.search(pattern, url):
            return endpoint
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
