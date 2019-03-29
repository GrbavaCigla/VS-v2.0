import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListTile(Gtk.Box):
    def __init__(self,name,description):
        Gtk.Box.__init__(self)
        self.name = name
        self.set_border_width(20)
        self.description = description

        name_label = Gtk.Label()
        name_label.set_label(self.name)
        name_label.set_xalign(0)
        desc_label = Gtk.Label()
        desc_label.set_label(self.description)

        grid = Gtk.Grid()

        grid.add(name_label)
        grid.attach(desc_label,0,1,1,1)
        self.add(grid)


class MainWindow(Gtk.Window):
    def selectRow(self,widget,tile):
        self.viru_name = tile.get_child().name
        if not self.output_folder == None:
                self.start_button.set_sensitive(True)

    def openFolder(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a folder", action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK)
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_folder = dialog.get_filename()
            self.dir_entry.set_text(self.output_folder)
            if not self.viru_name == None:
                self.start_button.set_sensitive(True)

        dialog.destroy()
    def __init__(self):
        Gtk.Window.__init__(self, title="ViruStick v2.0")
        self.output_folder = None
        self.viru_name = None
        self.set_default_size(700, 500)
        self.set_resizable(False)
        self.set_border_width(20)

        # Grid
        grid = Gtk.Grid()
        self.add(grid)
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)

        # First and Second Row Buttons
        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked",self.openFolder)
        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_property("can-focus",False)
        self.dir_entry.set_placeholder_text("Device")
        self.dir_entry.set_hexpand(True)

        grid.attach(self.dir_entry, 0, 0, 5, 1)
        grid.attach(browse_button,6,0,1,1)

        # Scroller
        widgets = [ListTile("Generic Name","Generic Discrption.")]
        listbox = Gtk.ListBox()
        listbox.connect("row-selected",self.selectRow)
        for wid,i in enumerate(widgets):
            listbox.insert(i,wid)
        swin = Gtk.ScrolledWindow()
        swin.add(listbox)
        swin.set_vexpand(True)
        grid.attach(swin,0,1,7,6)

        # Deploy Buttons
        self.start_button = Gtk.Button(label="Deploy")
        self.start_button.set_sensitive(False)
        grid.attach(self.start_button,6,7,1,1)
        


window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
