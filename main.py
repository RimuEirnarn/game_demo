# pylint: disable=no-member
import pyray as pr
from props.game import Game
from props.runner import ModuleFlag, initialize

def main():
    game = Game()

    with initialize(
        800,
        450,
        "Hello, Cyrene~",
        (ModuleFlag.audio,)
    ):
        pr.set_target_fps(60)

    game.load()
    game.run()


if __name__ == "__main__":
    main()
