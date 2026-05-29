from pyray import load_sound, unload_sound, set_sound_volume, Sound, load_music_stream, unload_music_stream, set_music_volume, Music, play_music_stream, stop_music_stream, play_sound, stop_sound, update_music_stream, update_sound
from typing import NamedTuple, Literal, Any
from abc import ABC

class SoundInitializer(NamedTuple):
    var: Literal["sound", "music"]
    path: str

class AudioHandler(ABC):
    def __init__(self, path: str, volume: float = 0) -> None:
        self._path = path
        self._volume = volume
        self._data: Any | None = None

    def load(self):
        """Load Audio stream"""
        return NotImplemented

    def unload(self):
        """Unload Audio stream"""
        return NotImplemented

    def play(self):
        """Play Audio stream"""
        return NotImplemented

    def stop(self):
        return NotImplemented

    def update(self):
        return NotImplemented

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, val: float):
        if val < 0 or val > 1:
            raise ValueError("Volume must be between 1 and 0")
        self._volume = val

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        if not self._data:
            raise ValueError("Not initialized")
        return self._data

class SoundHandler(AudioHandler):
    def __init__(self, path: str, volume: float = 0) -> None:
        super().__init__(path, volume)
        self._data: Sound | None = None

    def load(self):
        self._data = load_sound(self._path)
        set_sound_volume(self.data, self.volume)

    def unload(self):
        unload_sound(self.data)

    def play(self):
        play_sound(self.data)

    def update(self):
        pass

    def stop(self):
        stop_sound(self.data)

class MusicHandler(AudioHandler):
    def __init__(self, path: str, volume: float = 0) -> None:
        super().__init__(path, volume)
        self._data: Music | None = None

    def load(self):
        self._data = load_music_stream(self._path)
        set_music_volume(self.data, self.volume)

    def unload(self):
        unload_music_stream(self.data)

    def play(self):
        play_music_stream(self.data)

    def update(self):
        update_music_stream(self.data)

    def stop(self):
        stop_music_stream(self.data)

class AudioManager:
    def __init__(self, initializers: dict[str, AudioHandler] | None = None, volume: float = 1.0):
        self._audio = {}
        self._initializers = initializers
        self._volume = volume

    def load(self):
        if self._initializers:
            for key, value in self._initializers.items():
                value.volume = self._volume
                value.load()
                self._audio[key] = value

    def unload(self):
        for audio in self._audio.values():
            audio.unload()
        self._audio.clear()

    def update(self):
        for audio in self._audio.values():
            if isinstance(audio, MusicHandler):
                audio.update()

    def get(self, name: str):
        return self._audio[name]
