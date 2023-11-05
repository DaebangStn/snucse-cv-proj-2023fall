from gui.gui import GUI
from util.loader import load_yaml

if __name__ == "__main__":
    load_yaml()
    gui = GUI()
    gui.run()
