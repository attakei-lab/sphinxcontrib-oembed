====================
sphinxcontrib-oembed
====================

Embed HTML content by URL from eEmbed consumer

Overview
========

.. note:: Writing later

Installation
============

Install package from GitHub Releases.

.. code-block:: console

   pip install --find-links=https://github.com/attakei-lab/sphinxcontrib-oembed/releases sphinxcontrib-oembed

Usage
=====

Add this extension into your ``conf.py`` of Sphinx.

.. code-block:: python

   extensions = [
       "sphinxcontrib.oembed",
   ]

   # You can change User-agent
   # Default is sphinxcontrib-oembed/{ext-version}
   obmed_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"

Canges
======

v0.2.0
------

* Enable to confiugre User-agent when request oEmbed providers

License
=======

Apache-2.0
