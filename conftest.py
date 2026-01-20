from src.constants import Env


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=Env.DEVELOPMENT, type=str)
