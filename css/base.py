import abc
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class BaseCSS(abc.ABC):
    @abc.abstractmethod
    def get_data(self) -> bytes:
        ...

    def apply(self, widget: Gtk.Widget) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(self.get_data())
        context = widget.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
