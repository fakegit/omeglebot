#!/usr/bin/env python3
# -*- coding: utf-8 -*-

version_info = (0, 0, 2)
__version__ = "{}.{}.{}".format(*version_info)


authors = (("Michael Mooney", "mikeyy@mikeyy.com"),)

authors_email = ", ".join("{}".format(email) for _, email in authors)

__license__ = "MPL-2.0"
__author__ = ", ".join(
    "{} <{}>".format(name, email) for name, email in authors
)

package_info = (
    "An Omegle bot in Python with typo generation, content spinning,",
    "asynchronicity, and Proxy management."
)
__maintainer__ = __author__

__all__ = (
    "__author__",
    "__author__",
    "__license__",
    "__maintainer__",
    "__version__",
    "version_info",
)
