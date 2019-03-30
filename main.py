import gi
import json
import requests
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tqdm import tqdm

class Controller:
    def __init__(self,url):
        content = requests.get(url).text
        parsed = json.loads(content)
        self.items = {}
        for i in parsed["Items"]:
            self.items[i["name"]]=[i["desc"],i["link"],i["author"]]
    def toListTile(self):
        res = []
        for k,v in self.items.items():
            res.append(ListTile(k,v[0],v[1],v[2]))
        return res


class ListTile(Gtk.Box):
    def install(self,widget):
        self.content = requests.get(self.link).text
        local_filename = "./scripts/"+self.link.split('/')[-1]
        with requests.get(self.link, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)):
                    if chunk:
                        f.write(chunk)
        return local_filename
    def __init__(self,name,description,link,author):
        Gtk.Box.__init__(self)
        self.link = link
        self.author = author
        self.name = name
        self.set_border_width(20)
        self.description = description

        name_label = Gtk.Label()
        name_label.set_label(self.name)
        name_label.set_xalign(0)
        desc_label = Gtk.Label()
        desc_label.set_label(self.description)
        desc_label.set_xalign(0)
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        inst_button = Gtk.Button(label="Install")
        inst_button.connect("clicked",self.install)

        grid = Gtk.Grid()
        grid.add(name_label)
        grid.attach(desc_label,0,1,1,1)
        grid.attach(spacer,1,0,1,1)
        grid.attach(inst_button,2,0,1,2)
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

        grid.attach(self.dir_entry, 0, 0, 6, 1)
        grid.attach(browse_button,6,0,1,1)

        # Scroller
        widgets = Controller("./source.json").toListTile()
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
window.connect("destroy",Gtk.main_quit)
window.show_all()
Gtk.main()
