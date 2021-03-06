### Author: <lefred$inuits,be>

global mysql_user
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')

global mysql_pwd
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD') 

class dstat_plugin(dstat):
    """
    Plugin for MySQL 5 Keys.
    """

    def __init__(self):
        self.name = 'mysql5 key status'
        self.nick = ('used', 'read', 'writ', 'rreq', 'wreq')
        self.vars = ('Key_blocks_used', 'Key_reads', 'Key_writes', 'Key_read_requests', 'Key_write_requests')
        self.type = 'f'
        self.width = 4
        self.scale = 1000

    def check(self): 
        global MySQLdb
        import MySQLdb
        try:
            self.db = MySQLdb.connect(user=mysql_user, passwd=mysql_pwd)
        except:
            raise Exception, 'Cannot interface with MySQL server'

    def extract(self):
        try:
            c = self.db.cursor()
            c.execute("""show global status like 'Key_%';""")
            lines = c.fetchall()
            for line in lines:
                if len(line[1]) < 2: continue
                if line[0] in self.vars:
                    self.set2[line[0]] = float(line[1])

            for name in self.vars:
                self.val[name] = self.set2[name] * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
