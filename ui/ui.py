import pygtk
pygtk.require('2.0')
import gtk
import webkit
import gobject

class MyWindowWebKit:

    default_site = "http://localhost:3000/"

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_default_size(460, 670) 
        self.web_view = webkit.WebView()
        self.web_view.open(self.default_site)

        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)

        self.window.add(scroll_window)
        self.window.show_all()

    def main(self):
        gobject.threads_init()
        gtk.main()

# if __name__ == "__main__":
mn = MyWindowWebKit()
mn.main()