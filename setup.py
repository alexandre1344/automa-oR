from setuptools import setup
from version import VERSION

setup(
    name="AutomacaoRAS",
    version=VERSION,
    description="Sistema de Automação RAS",
    author="Alexandre-dev RJ",
    packages=[""],
    install_requires=[
        'selenium',
        'webdriver_manager',
        'Pillow',
        'requests',
        'tkinter'
    ],
    entry_points={
        'console_scripts': [
            'automacaoras=save_automação copy:main',
        ],
    },
)