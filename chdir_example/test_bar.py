from time import sleep

from path import path

here = path(__file__).abspath()

if __name__ == '__main__':
    import os
    import sys

    sys.path.append(here.parent)
    os.chdir(here.parent)

    from bar import Bar

    b = Bar('hello')
    #emit_signal('on_start')
    b.start()
    sleep(3)
    b.stop()
    #emit_signal('on_stop')
