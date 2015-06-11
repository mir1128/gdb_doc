import threading
class Writer:
    def __init__(self, message):
        self.message = message;
    def __call__(self):
        gdb.write(self.message)

class MyThread1(threading.Thread):
    def run(self):
        gdb.post_event(Writer("Hello "));

class MyThread2(threading.Thread):
    def run(self):
        gdb.post_event(Writer("World\n"));


MyThread1().start();
MyThread2().start();



