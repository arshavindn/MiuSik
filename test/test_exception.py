# -*- coding: utf-8 -*-


def test1(loc):
    try:
        loc = loc.decode('utf-8')
    except UnicodeDecodeError:
        pass

    print loc
    print


def test2(loc):
    try:
        test1(loc)

        print "yolo"

        try:
            print 2 / 0
        except ZeroDivisionError:
            pass

        print "It passes."
    except Exception, e:
        print e
        print "Oh no!"

test2("Nguyễn Thị Thanh Ngân")
