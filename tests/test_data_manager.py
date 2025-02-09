# # tests/model/test_data_manager.py
# import pytest
# from model.data_manager import DataManager

# @pytest.fixture
# def data_manager():
#     return DataManager()

# def test_get_or_create_app(data_manager):
#     app_id = data_manager.get_or_create_app("TestApp", "test_path")
#     assert isinstance(app_id, int)

# def test_log_app_switch(data_manager):
#     from_app_id = 1
#     to_app_id = 2
#     result = data_manager.log_app_switch(from_app_id, to_app_id)
#     assert result == True

# def test_get_merged_sessions(data_manager):
#     sessions = data_manager.get_merged_sessions()
#     assert isinstance(sessions, list)