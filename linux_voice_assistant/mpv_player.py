# mpv_player.py
from typing import Union, List, Callable, Optional

from .player.libmpv import LibMpvPlayer


class MpvMediaPlayer:
    """
    Linux Voice Assistant MediaPlayer implementation based on libmpv.

    This class provides the MediaPlayer interface expected by LVA and
    delegates all playback logic to LibMpvPlayer.
    """

    def __init__(self, device: str | None = None) -> None:
        self._player = LibMpvPlayer(device=device)
        self._done_callback: Optional[Callable[[], None]] = None

    def play(
        self,
        url: Union[str, List[str]],
        done_callback: Optional[Callable[[], None]] = None,
        stop_first: bool = False,
    ) -> None:
        """
        Play a media URL.

        Args:
            url: Media URL or list of URLs (LVA currently uses a single URL).
            done_callback: Optional callback invoked when playback finishes.
            stop_first: Kept for API compatibility; currently unused.
        """
        # LVA currently only uses single URLs
        if isinstance(url, list):
            url = url[0]

        self._done_callback = done_callback
        self._player.play(url, done_callback=done_callback, stop_first=stop_first)

    def pause(self) -> None:
        """Pause playback."""
        self._player.pause()

    def resume(self) -> None:
        """Resume playback."""
        self._player.resume()

    def stop(self) -> None:
        """Stop playback and invoke the done callback if present."""
        self._player.stop()
        if self._done_callback:
            self._done_callback()
            self._done_callback = None

    def set_volume(self, volume: float) -> None:
        """
        Set playback volume.

        Args:
            volume: Volume in percent (0.0–100.0).
        """
        self._player.set_volume(volume)

    def duck(self, factor: float = 0.5) -> None:
        """
        Temporarily reduce volume.

        Args:
            factor: Volume multiplier (0.0–1.0).
        """
        self._player.duck(factor)

    def unduck(self) -> None:
        """Restore volume after ducking."""
        self._player.unduck()