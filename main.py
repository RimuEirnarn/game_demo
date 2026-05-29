# pylint: disable=no-member
import pyray as pr
from props.game import Game
from props.runner import ModuleFlag, initialize
from props.config import ConfigSchema, load_config, write_config

CONFIG_PATH = "transient/config.toml"
default_config: ConfigSchema = {
    "resolution": (1920, 1080),
    "max_fps": 60
}

def main():
    try:
        config = load_config(CONFIG_PATH)
    except FileNotFoundError:
        config = default_config
        write_config(CONFIG_PATH, config)
    game = Game(config)


    with initialize(
        config['resolution'][0],
        config['resolution'][1],
        "Hello, Cyrene~",
        (ModuleFlag.audio,)
    ):
        pr.set_target_fps(config['max_fps'])

    game.load()
    game.run()


if __name__ == "__main__":
    main()
