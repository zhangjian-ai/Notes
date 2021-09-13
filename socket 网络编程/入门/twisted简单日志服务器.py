from twisted.internet import reactor
from twisted.internet.protocol import Factory, connectionDone
from twisted.protocols.basic import LineReceiver
from twisted.python import failure


class SimpleLogger(LineReceiver):
    """自定义协议对象"""

    def connectionMade(self):
        print("Got connection from ", self.transport.client)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print(self.transport.client, "Disconnected")

    # def lineReceived(self, line):
    #     # self.transport.write("我在学你说话" + line)
    #     print(line)
    def dataReceived(self, data):
        self.transport.write(f"我在学你说话: {data.decode()}".encode())
        print(data.decode())


if __name__ == '__main__':
    factory = Factory()
    factory.protocol = SimpleLogger

    reactor.listenTCP(1234, factory)
    reactor.run()
