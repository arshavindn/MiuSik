from src.metadata import *


def test1():
    loc = "D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"
    format = get_format(loc)
    print format.read_all()
