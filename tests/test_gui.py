# # tests/view/test_gui.py
# import pytest
# from view.gui import Application
# from controller import Controller

# @pytest.fixture
# def gui():
#     controller = Controller()
#     return Application(controller)

# def test_setup_canvas(gui):
#     gui.setup_canvas()
#     assert gui.canvas is not None

# def test_create_buttons(gui):
#     gui.create_buttons()
#     assert len(gui.window.children) > 0