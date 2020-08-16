import tkinter as tk
from threading import Thread

from plyer import notification


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = "200x200+0+0"
        master.geometry(
            "{0}x{1}+0+0".format(
                master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad
            )
        )
        master.bind("<Escape>", self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


class PlatformAdapter:
    def blockScreenHelper(self, seconds):
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.configure(background="black")
        root.after(
            int(seconds * 1000), root.destroy
        )  # Destroy the widget after 30 seconds
        app = FullScreenApp(root)
        root.wm_attributes("-topmost", 1)
        root.mainloop()

    def blockScreen(self, seconds):
        t = Thread(target=self.blockScreenHelper, args=(seconds,))
        t.start()

    @staticmethod
    def sendNotification(message):
        notification.notify(
            title="Take A Break",
            message=message,
            app_icon="assets/logo.ico",
            timeout=10,
        )

    def getLastUserActivityTime(self):
        raise NotImplementedError
