import abc

import gi
import typing

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk

from css.base import BaseCSS


def setup_css(widget: Gtk.Widget, css: BaseCSS) -> None:
    """
    Sets up the CSS for the given widget.

    :param widget: The widget to apply the CSS to.
    :param css: The CSS to apply.
    """
    css.apply(widget)
