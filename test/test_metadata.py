from src.metadata import *


def test1():
    # loc = "D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"
    loc = "D:/Movies/Christina_Perri-Lovestrong-Deluxe_Edition/02-christina_perri-arms.flac"
    format = get_format(loc)
    print format.read_tags(['cover'])
