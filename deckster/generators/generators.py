import logging
import os
import importlib
import importlib.util
from deckster.common import configs
from pathlib import Path

logger = logging.getLogger("deckster")
GENERATORS_DIR = os.path.expanduser(configs.read_config("generators_dir"))

class generator:
    def __init__(self, generator, args = {}):
        self.generator = generator
        self.args = args


def init_generators():
    logger.debug("Reading generators...")
    gens = configs.read_config("generators")
    if gens is None: return None
    active_gen = []
    for gen in gens:
        if "enabled" in gen:
            if gen["enabled"]:
                active_gen.append(generator(gen["generator"], gen["args"] if "args" in gen else {}))
                logger.info(f"Generator \"{gen['generator']}\" activated!")
    return active_gen

def execute_generators():
    gens = init_generators()
    if gens is None: return None
    for gen in gens:
        if gen.generator.startswith("builtins."):
            logger.debug(f"Starting builtin generator 'generators.{gen.generator}'")
            generator = importlib.import_module(f"deckster.generators.{gen.generator}", None)
        else:
            path =  os.path.join(GENERATORS_DIR, gen.generator.replace(".", "/") + ".py")
            if os.path.isfile(path):
                spec = importlib.util.spec_from_file_location(gen.generator.split(".")[-1], path)
                generator = importlib.util.module_from_spec(spec)
                logger.debug(f"Importing custom generator '{gen.generator}' from '{path}'")
                spec.loader.exec_module(generator)
            else:
                logger.error(f"File '{path}' does not exist.")
                raise FileNotFoundError(f"File '{path}' does not exist.")
        generator.main(gen.args)
    