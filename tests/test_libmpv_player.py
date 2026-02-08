import time
import logging

from linux_voice_assistant.player.libmpv import LibMpvPlayer


logging.basicConfig(level=logging.DEBUG)

player = LibMpvPlayer()

player.play("https://icecast.radiofrance.fr/fip-midfi.mp3")
time.sleep(5)

player.pause()
time.sleep(2)

player.resume()
time.sleep(5)

player.stop()
time.sleep(2)

print("Final state:", player.state())
