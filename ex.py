import sys
import traceback

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
        self.output = output
        super(CalcTextInput, self).__init__(*args, **kwargs)
        self.text_buffer = self.get_buffer()
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.text_buffer.connect("changed", self.update_output)
        css.setup_css(self, widgets.TextInputCSS())

    def update_output(self, *args):
        try:
            self.output.get_buffer().set_text(
                "\n".join(
                    parser.parse_text(
                        self.text_buffer.get_text(
                            self.text_buffer.get_start_iter(),
                            self.text_buffer.get_end_iter(),
                            False,
                        ).split("\n")
                    )
                )
            )
        except:
            traceback.print_exc()


class CalcTextOutput(Gtk.TextView):
    def __init__(self, *args, **kwargs):
        super(CalcTextOutput, self).__init__(*args, **kwargs)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_editable(False)


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
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.button = Gtk.Button(label="Hello")
        self.button.connect("clicked", self.hello)

        self.set_child(self.box2)  # Horizontal box to window

        self.main_text = MainTextView()
        self.box2.append(self.main_text)
        self.box2.set_spacing(10)

    def hello(self, button):
        print("Hello world")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.setup_css()
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
