import threading
import logging
from .base import AudioPlayer
from .state import PlayerState
import mpv


class LibMpvPlayer(AudioPlayer):

    def __init__(self, device: str | None = None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._state = PlayerState.IDLE
        self._state_lock = threading.Lock()

        self._last_volume: float = 100.0  # mpv Volume 0-100

        self._mpv = mpv.MPV(
            audio_display=False,
            log_handler=self._on_mpv_log,
            loglevel="error",
        )
        if device:
            self._log.info("Using audio device: %s", device)
            self._mpv["audio-device"] = device

    # -------- Core Methods --------

    def play(self, url: str, paused: bool = False) -> None:
        with self._state_lock:
            self._set_state(PlayerState.LOADING)

        self._mpv.pause = paused

        self._log.info("Loading media: %s (paused=%s)", url, paused)
        self._mpv.play(url)

    def pause(self):
        with self._state_lock:
            self._mpv.pause = True
            self._set_state(PlayerState.PAUSED)

    def resume(self):
        with self._state_lock:
            self._mpv.pause = False
            self._set_state(PlayerState.PLAYING)

    def stop(self):
        with self._state_lock:
            self._mpv.stop()
            self._set_state(PlayerState.IDLE)

    def state(self):
        with self._state_lock:
            return self._state

    # -------- Volume / Ducking --------

    def set_volume(self, volume: float):
        """
        volume: float 0.0-1.0
        """
        with self._state_lock:
            self._last_volume = volume * 100
            self._mpv.volume = self._last_volume

    def duck(self, factor: float = 0.5):
        with self._state_lock:
            self._last_volume = getattr(self, "_last_volume", self._mpv.volume)
            self._mpv.volume = self._last_volume * factor

    def unduck(self):
        with self._state_lock:
            self._mpv.volume = getattr(self, "_last_volume", self._mpv.volume)

    # -------- Internal Helpers --------

    def _on_mpv_log(self, level, prefix, text):
        if level in ("error", "fatal"):
            self._log.error("[mpv] %s", text.strip())
            with self._state_lock:
                self._set_state(PlayerState.ERROR)

    def _set_state(self, new_state: PlayerState):
        if self._state != new_state:
            self._log.debug("State %s → %s", self._state.name, new_state.name)
            self._state = new_state
