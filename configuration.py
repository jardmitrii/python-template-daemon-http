pidfile = '/var/run/mydaemon.pid'
listen_address = 'localhost'
listen_port = 8080

log_format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
mainlog = '/var/log/pybilling/'

if __name__ == '__main__':
    print 'Configuration file!'
