global glob
import glob

class dstat_postfix(dstat):
    def __init__(self):
        self.name = 'postfix'
        self.type = 'd'
        self.width = 4
        self.scale = 100
        self.vars = ('incoming', 'active', 'deferred', 'bounce', 'defer')
        self.nick = ('inco', 'actv', 'dfrd', 'bnce', 'defr')
        self.init(self.vars, 1)

    def check(self):
        if not os.access('/var/spool/postfix/active', os.R_OK):
            raise Exception, 'Cannot access postfix queues'
        return True

    def extract(self):
        for item in self.vars:
            self.val[item] = len(glob.glob('/var/spool/postfix/'+item+'/*/*'))

# vim:ts=4:sw=4:et
