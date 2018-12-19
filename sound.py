from winsound import PlaySound, SND_LOOP
from sys import argv

SOUNDS = ['sounds/0.wav', 'sounds/1.wav', 'sounds/2.wav']  # звуки будильника

index = int(argv[1])
print(index)
try:
    PlaySound(SOUNDS[index], SND_LOOP)
except Exception:
    for sound in SOUNDS:
        try:
            PlaySound(sound, SND_LOOP)
            break
        except Exception:
            pass