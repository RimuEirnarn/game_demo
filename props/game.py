# pylint: disable=no-member
"""Game instance"""
import pyray as pr

from props.audio import (
    AudioManager,
    MusicHandler
)
from props.runner import draw
from props.config import ConfigSchema

class Game:
    """Game instance"""
    def __init__(self, config: ConfigSchema):
        self.soundmgr = AudioManager({
            "newpage": MusicHandler("external/NewPage.mp3", 1)
        })
        self.config = config

    def load(self):
        """load"""
        self.soundmgr.load()

        bgm = self.soundmgr.get("newpage", MusicHandler)
        bgm.play()

    def update(self):
        """Update"""
        self.soundmgr.update()

    def draw(self):
        """Draw"""
        width, height = self.config['resolution']
        pr.clear_background(pr.BLACK)
        text = "Hello, Cyrene~"
        text_size = pr.measure_text_ex(pr.get_font_default(), text, 20, 2)

        pr.draw_text(
            "Hello, Cyrene~",
            int((width // 2) - (text_size.x // 2)),
            int((height // 2) - (text_size.y // 2)),
            20,
            (0xff, 0xc5, 0xd3, 0xff)
        )

    def run(self):
        """Run"""
        try:
            while not pr.window_should_close():
                self.update()
                with draw():
                    self.draw()
        finally:
            self.unload()
            pr.close_window()

    def unload(self):
        """Unload"""
        self.soundmgr.unload()
