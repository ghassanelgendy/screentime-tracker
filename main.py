# main.py
from model import Model
from controller import Controller
from view.gui import Application

def main():
    model = Model()
    controller = Controller(model)
    app = Application(controller)
    app.run()

if __name__ == "__main__":
    main()