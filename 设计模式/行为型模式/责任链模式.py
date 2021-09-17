'''
责任链模式：使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。将这些对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。
角色：
    - 抽象处理者(Handler)
    - 具体处理者(ConcreteHandler)
    - 客户端(Client)
适用场景：
    - 有多个对象可以处理一个请求，那个对象处理由运行时决定
    - 在不明确接收者的情况下，向多个对象中的一个提交一个请求
优点：
    - 降低耦合度：一个对象无需知道是其他哪一个对象处理请求
'''

from abc import abstractmethod, ABCMeta


class Handler(metaclass=ABCMeta):
    @abstractmethod
    def handle_request(self, day):
        pass


class PresidentHandler(Handler):
    def handle_request(self, day):
        if day <= 10:
            print("总经理批准假期：%s" % day)
        else:
            print("请你离职！！")


class DepartmentHandler(Handler):
    def handle_request(self, day):
        if day <= 5:
            print("部门主管批准假期：%s" % day)
        else:
            print("部门主管权限不足！")
            PresidentHandler().handle_request(day)


class ProjectHandler(Handler):
    def handle_request(self, day):
        if day <= 3:
            print("项目主管批准假期：%s" % day)
        else:
            print("项目主管权限不足！")
            DepartmentHandler().handle_request(day)


# client
day = 3
p = ProjectHandler()
p.handle_request(day)
