# main.py
from model import Model
from controller import Controller
from view.gui import Application

def main():
    model = Model()
    app = Application()  # Create Application first, without a controller
    controller = Controller(model, app)  # Now create Controller
    app.set_controller(controller)  # Assign controller after creation
    app.run()

if __name__ == "__main__":
    main()
