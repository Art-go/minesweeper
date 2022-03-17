from setuptools import setup
import py2exe
import pyglet
import random
import base64
import json

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows=['main.py'],
    zipfile=None
)
