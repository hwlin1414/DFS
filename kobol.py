import koboldfs
import koboldfs.client

import StringIO

c = koboldfs.client.Client('demo', servers=['127.0.0.1:9999', '127.0.0.1:9998', '127.0.0.1:9997', '127.0.0.1:9996'])
#c = koboldfs.client.Client('demo', servers=['127.0.0.1:9998'])

c.put('rc.conf', '/etc/rc.conf')
c.commit()

#buf = ""
#o = StringIO.StringIO(buf)

#ret = c.get('motd', o)
#print ret
#if ret == True:
#    o.seek(0)
#    print o.read()

#c.delete('motd')
#c.commit()
