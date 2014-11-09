import datetime as dt


class Log(object):
    def success(self, msg):
        self.log(msg, '[+]')

    def error(self, msg):
        self.log(msg, '[!]')

    def log(self, msg, prefix='[i]'):
        print '{} {} {}'.format(
            prefix, dt.datetime.now().isoformat(), msg
        )
