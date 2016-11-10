import koboldfs
import koboldfs.client

c = koboldfs.client.Client('demo', servers=['127.0.0.1:9999', '127.0.0.1:9998', '127.0.0.1:9997', '127.0.0.1:9996'])

c.put('motd', '/etc/rc.conf')
c.commit()
