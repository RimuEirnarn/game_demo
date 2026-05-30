# pylint: disable=no-member
"""Game instance"""
import pyray as pr

from props.audio import AudioManager, MusicHandler
from props.runner import draw
from props.config import ConfigSchema
from props.draw import draw_tiled_h, draw_tiled_v
from props.frame_helper import is_on_frame


class Game:
    """Game instance"""

    def __init__(self, config: ConfigSchema):
        self.soundmgr = AudioManager(
            {"newpage": MusicHandler("external/NewPage.mp3", 1)}
        )
        self.config = config
        self.textures: dict[str, pr.Texture] = {}
        self.scale = 4
        self.corner = 8 * self.scale
        self.hline_w = 4 * self.scale
        self.hline_h = 2 * self.scale
        self.vline_w = 2 * self.scale
        self.vline_h = 4 * self.scale
        self.width, self.height = config["resolution"]
        self.dragging = False
        self.drag_anchor = pr.Vector2(0, 0)

    def load(self):
        """load"""
        self.soundmgr.load()

        bgm = self.soundmgr.get("newpage", MusicHandler)
        bgm.play()
        for key, path in (
            ("frame_tl", "assets/window_topleft.png"),
            ("frame_tr", "assets/window_topright.png"),
            ("frame_bl", "assets/window_botleft.png"),
            ("frame_br", "assets/window_botright.png"),
            ("frame_v", "assets/window_vertical.png"),
            ("frame_h", "assets/window_horizontal.png"),
        ):
            texture = pr.load_texture(path)
            pr.set_texture_filter(texture, pr.TextureFilter.TEXTURE_FILTER_POINT)
            self.textures[key] = texture

    def update(self):
        """Update"""
        self.soundmgr.update()
        mouse = pr.get_mouse_position()
        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT) and is_on_frame(
            mouse.x,
            mouse.y,
            self.corner,
            self.vline_w,
            self.hline_h,
            self.width,
            self.height,
        ):
            self.drag_anchor = mouse

        if pr.is_mouse_button_released(pr.MouseButton.MOUSE_BUTTON_LEFT):
            self.dragging = False

        if self.drag_anchor.x != 0 and pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT):
            pos = pr.get_window_position()
            abs_ms = pr.Vector2(pos.x + mouse.x, pos.y + mouse.y)
            npos_x = int(abs_ms.x - self.drag_anchor.x)
            npos_y = int(abs_ms.y - self.drag_anchor.y)
            pr.set_window_position(npos_x, npos_y   )

    def draw(self):
        """Draw"""
        width, height = self.config["resolution"]
        background = (0, 0, 0, int(255 // 1.2))
        pr.clear_background((0, 0, 0, 0))
        pr.draw_rectangle(
            0 + self.vline_w,
            0 + self.hline_h,
            width - self.vline_w * 2,
            height - self.hline_h * 2,
            background,
        )
        text = "Hello, Cyrene~"
        text_size = pr.measure_text_ex(pr.get_font_default(), text, 20, 2)

        pr.draw_text(
            "Hello, Cyrene~",
            int((width // 2) - (text_size.x // 2)),
            int((height // 2) - (text_size.y // 2)),
            20,
            (0xFF, 0xC5, 0xD3, 0xFF),
        )
        self.draw_frame()

    def draw_frame(self):
        """Frame"""
        hline = self.textures["frame_h"]
        vline = self.textures["frame_v"]
        tl = self.textures["frame_tl"]
        tr = self.textures["frame_tr"]
        bl = self.textures["frame_bl"]
        br = self.textures["frame_br"]
        w, h = self.width, self.height
        scale = self.scale
        cw = self.corner  # scaled corner width/height = 32
        hline_h = self.hline_h
        vline_w = self.vline_w

        # ── Corners ──────────────────────────────────────────────
        # Top-left
        pr.draw_texture_ex(tl, pr.Vector2(0, 0), 0, scale, pr.WHITE)
        # Top-right
        pr.draw_texture_ex(tr, pr.Vector2(w - cw, 0), 0, scale, pr.WHITE)
        # Bottom-left
        pr.draw_texture_ex(bl, pr.Vector2(0, h - cw), 0, scale, pr.WHITE)
        # Bottom-right
        pr.draw_texture_ex(br, pr.Vector2(w - cw, h - cw), 0, scale, pr.WHITE)

        # ── Horizontal edges (top and bottom) ────────────────────
        inner_w = w - cw * 2
        draw_tiled_h(hline, cw, 0, inner_w, scale)  # top
        draw_tiled_h(hline, cw, h - hline_h, inner_w, scale)  # bottom

        # ── Vertical edges (left and right) ──────────────────────
        inner_h = h - cw * 2
        draw_tiled_v(vline, 0, cw, inner_h, scale)  # left
        draw_tiled_v(vline, w - vline_w, cw, inner_h, scale)  # right

    def run(self):
        """Run"""
        try:
            while not pr.window_should_close():
                self.update()
                with draw():
                    self.draw()
        finally:
            self.unload()

    def unload(self):
        """Unload"""
        self.soundmgr.unload()
        for texture in self.textures.values():
            pr.unload_texture(texture)
