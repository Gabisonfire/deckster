import setuptools
import json
import os
from pathlib import Path
from subprocess import check_call
from setuptools.command.install import install

APP_NAME = "Deckster"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        cfg_path = f"{str(Path.home())}/.config/{APP_NAME}.json"
        if not os.path.exists(cfg_path):            
            cfg = open(cfg_path, 'x')
            j = dict(
            jackett_apikey="",
            jackett_url="http://127.0.0.1:9117",
            jackett_indexer="all",
            description_length=100,
            exclude="",
            results_limit=20,
            client_url="",
            display="grid",
            torrent_client="transmission",
            torrent_client_username="",
            torrent_client_password="",
            download_dir=""
            )
            json.dump(j, cfg, indent=4)
        install.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Deckster",
    version="0.1",
    author="Gabisonfire",
    author_email="gabisonfire@github.com",
    description="##############",
    keywords="streamdeck",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ['deckster = deckster.deckster:main']
        },
    url="https://github.com/Gabisonfire/Deckster",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Communications :: File Sharing",
    ],
    install_requires=["playsound==1.3.0", "Pillow==8.3.2", "requests==2.23.0", "streamdeck==0.8.5", "apscheduler==3.8.1"],
    cmdclass={
        'install': PostInstallCommand
    },

)
