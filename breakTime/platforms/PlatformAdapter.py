import tkinter as tk
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
    @staticmethod
    def blockScreen(seconds):
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.configure(background="black")
        root.after(
            int(seconds * 1000), lambda: root.destroy()
        )  # Destroy the widget after 30 seconds
        app = FullScreenApp(root)
        root.wm_attributes("-topmost", 1)
        root.mainloop()

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
