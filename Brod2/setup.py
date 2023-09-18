
from setuptools import setup

APP_NAME = 'Brod'
APP = ['New_Workers.py']
DATA_FILES = [('db', ['Works.db'])]
OPTIONS = {
    'packages': ['darkdetect', 'macholib', 'modulegraph', 'PIL', 'PyQt5'],
    'iconfile': 'old_photo.jpg',
    'argv_emulation': True
}
# darkdetect'
setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
