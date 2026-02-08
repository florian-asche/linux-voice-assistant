import logging
from typing import Union, List, Callable, Optional

from .player.libmpv import LibMpvPlayer


class MpvMediaPlayer:
    """
    LVA MediaPlayer implementation using libmpv.
    """

    def __init__(self, device: str | None = None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._player = LibMpvPlayer(device=device)
        self._done_callback: Optional[Callable[[], None]] = None

    def play(
        self,
        url: Union[str, List[str]],
        done_callback: Optional[Callable[[], None]] = None,
        stop_first: bool = True,
    ) -> None:
        self._log.info("Playing %s", url)

        if isinstance(url, list):
            url = url[0]

        self._done_callback = done_callback
        self._player.play(url, paused=False)

    def pause(self) -> None:
        self._player.pause()

    def resume(self) -> None:
        self._player.resume()

    def stop(self) -> None:
        self._player.stop()
        if self._done_callback:
            self._done_callback()
            self._done_callback = None

    def set_volume(self, volume: float) -> None:
        self._player.set_volume(volume)

    def duck(self, factor: float = 0.5) -> None:
        self._player.duck(factor)

    def unduck(self) -> None:
        self._player.unduck()
