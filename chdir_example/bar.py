from time import sleep
import multiprocessing

from path import path


class BarChild(object):
    STATES = dict(RUNNING=10, STOPPED=20)

    def __init__(self, conn, message):
        self.conn = conn
        self.message = message
        self.state = self.STATES['STOPPED']

    def main(self):
        while True:
            if self.conn.poll():
                command = self.conn.recv()
                if command == 'stop':
                    print '  got stop command'
                    self.state = self.STATES['STOPPED']
                    break
                elif command == 'start':
                    print '  got start command'
                    self.state = self.STATES['RUNNING']
            if self.state == self.STATES['RUNNING']:
                print self.message
                sleep(1.0)


class Bar(object):
    def __init__(self, message, auto_init=True):
        self.conn, self.child_conn = multiprocessing.Pipe()
        self.message = message
        if auto_init:
            self.child = self._launch_child()
        else:
            self.child = None

    def _launch_child(self):
        p = multiprocessing.Process(target=self._start_child)
        p.start()
        return p

    def _start_child(self):
        child = BarChild(self.child_conn, self.message)
        child.main()

    def start(self):
        print 'Bar.start()'
        if self.child is None:
            self.child = self._launch_child()
        self.conn.send('start')

    def stop(self):
        print 'Bar.stop()'
        self.conn.send('stop')
        self.child.join()
        if self.child:
            self.child.join()
        self.child = None


here = path(__file__).abspath()


if __name__ == '__main__':
    import os
    import sys

    sys.path.append(here.parent)
    os.chdir(here.parent)

    b = Bar('hello')
    b.start()
    sleep(3)
    b.stop()
