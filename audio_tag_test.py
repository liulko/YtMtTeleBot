from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1, WOAR, TSO2

audio = MP3('The_Rasmus_-_Livin_in_a_World_Without_You_(musmore.com).mp3', ID3=ID3)

print(audio.pprint())