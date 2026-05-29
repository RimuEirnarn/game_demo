import pyray as pr

from props.audio import (
    AudioManager,
    MusicHandler
)
from props.runner import draw


class Game:
    def __init__(self):
        self.soundmgr = AudioManager({
            "newpage": MusicHandler("external/NewPage.mp3", 1)
        })

    def load(self):
        self.soundmgr.load()

        bgm: MusicHandler = self.soundmgr.get("newpage")
        bgm.play()

    def update(self):
        self.soundmgr.update()

    def draw(self):
        pr.clear_background(pr.BLACK)

        pr.draw_text(
            "Hello, Cyrene~",
            300,
            225,
            20,
            pr.LIGHTGRAY
        )

    def run(self):
        try:
            while not pr.window_should_close():
                self.update()
                with draw():
                    self.draw()
        finally:
            self.unload()
            pr.close_window()

    def unload(self):
        self.soundmgr.unload()
