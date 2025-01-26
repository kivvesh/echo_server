import pytest
import os

from settings import ROOT_DIR
from dotenv import dotenv_values

@pytest.fixture(scope='session')
def config():
    return dotenv_values(os.path.join(ROOT_DIR,'.env'))
