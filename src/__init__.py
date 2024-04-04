from setuptools import setup, find_packages
from colorama import Fore, Style
import colorama
import requests
from bs4 import BeautifulSoup
setup(
    name='stv_scrapper',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',  # BeautifulSoup package
        'requests',  # requests package
        'colorama',  # requests package
        'pandas',  # requests package
    ],
)