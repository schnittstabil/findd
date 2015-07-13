from blinker import signal


class Progress(object):

    def __init__(self, task):
        self.progress_signal = signal('progress')
        self.task = task

    def start(self, sender, maxval=None):
        self.progress_signal.send(
            sender,
            task=self.task,
            state='start',
            maxval=maxval,
        )

    def update(self, sender, val=None):
        self.progress_signal.send(
            sender,
            task=self.task,
            state='update',
            val=val,
        )

    def finish(self, sender):
        self.progress_signal.send(
            sender,
            task=self.task,
            state='finish',
        )
