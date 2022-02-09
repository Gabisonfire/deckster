import setuptools
import os
import re, io
from pathlib import Path
from shutil import copyfile
from setuptools.command.install import install

APP_NAME = "Deckster"

__version__ = "0.4.2"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        cfg_path = f"{str(Path.home())}/.config/{APP_NAME.lower()}/config.json"
        if not os.path.exists(cfg_path):
            os.mkdir(f"{str(Path.home())}/.config/{APP_NAME.lower()}")                      
            copyfile('config.json', cfg_path)
        install.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=f"{APP_NAME.lower()}-sd",
    version=__version__,
    author="Gabisonfire",
    author_email="gabisonfire@github.com",
    description="A service to manage your Streamdeck easily on Linux",
    keywords="streamdeck",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    include_package_data=True,
    packages=["deckster", "deckster.generators", "deckster.generators.builtins", "deckster.common", "deckster.plugins.builtins", "deckster.plugins.builtins.page", "deckster.plugins.builtins.web"],
    entry_points = {
        "console_scripts": ['deckster = deckster.deckster:main']
        },
    url="https://github.com/Gabisonfire/Deckster",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Hardware",
    ],
    install_requires=["playsound==1.3.0", "Pillow==9.0.0", "requests==2.23.0", "streamdeck==0.8.5", "apscheduler==3.8.1", "pyaml==21.8.3"],
    cmdclass={
        'install': PostInstallCommand
    },
)
