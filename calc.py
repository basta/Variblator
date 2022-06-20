import sys
import traceback
import os

import gi

import parser
from parser import calc

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Adw, Gdk, GObject
from gi.repository.Gdk import Display
import css
import css.widgets as widgets


class CalcTextInput(Gtk.TextView):
    def __init__(self, output: "CalcTextOutput", *args, **kwargs):
        super(CalcTextInput, self).__init__(*args, **kwargs)
        self.output = output
        self.text_buffer = self.get_buffer()

        self.tag_table = self.text_buffer.get_tag_table()
        self.red_tag: Gtk.TextTag = Gtk.TextTag.new("red")
        self.red_tag.set_property("foreground", "#ff0000")
        self.text_tag: Gtk.TextTag = Gtk.TextTag.new("text")
        self.text_tag.set_property("foreground", "#327a12")
        self.tag_table.add(self.red_tag)
        self.tag_table.add(self.text_tag)

        self.set_vexpand(True)
        self.set_hexpand(True)
        css.setup_css(self, widgets.TextInputCSS())

        self.text_buffer.connect("changed", self.update_output)

    def update_output(self, *args, **kwargs):
        self.text_buffer.remove_all_tags(
            self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter()
        )
        parsed_input = self.parse_input()
        try:
            self.output.set_text("\n".join(parsed_input))
        except Exception:
            traceback.print_exc()

        for i, line in enumerate(parsed_input):

            if line == "":
                self.text_buffer.apply_tag(
                    self.text_tag,
                    self.text_buffer.get_iter_at_line(i)[1],
                    self.text_buffer.get_iter_at_line(i + 1)[1],
                )

        # Text buffer tag example
        # self.text_buffer.apply_tag(
        #     self.red_tag,
        #     self.text_buffer.get_start_iter(),
        #     self.text_buffer.get_end_iter(),
        # )

    def parse_input(self) -> list[str]:
        return parser.parse_text(
            self.text_buffer.get_text(
                self.text_buffer.get_start_iter(),
                self.text_buffer.get_end_iter(),
                False,
            ).split("\n")
        )


class CalcTextOutput(Gtk.Label):
    def __init__(self, *args, **kwargs):
        super(CalcTextOutput, self).__init__(*args, **kwargs)
        self.set_vexpand(True)
        self.set_size_request(100, -1)
        css.setup_css(self, widgets.TextOutputCSS())
        self.set_selectable(True)
        self.set_justify(Gtk.Justification.RIGHT)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.END)


class MainTextView(Gtk.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        super(MainTextView, self).__init__(*args, **kwargs)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_child(self.main_box)
        self.main_box.set_vexpand(True)
        self.main_box.set_hexpand(True)
        self.output = CalcTextOutput()
        self.input = CalcTextInput(self.output)

        self.main_box.append(self.input)
        self.main_box.append(self.output)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.set_child(self.main_container)  # Horizontal box to window

        self.main_text = MainTextView()
        self.main_container.append(self.main_text)
        self.main_container.set_spacing(10)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.set_default_size(400, 600)
        self.win.set_title("Calc")
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
