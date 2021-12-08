"""
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
"""

from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    """抽象处理者"""

    @abstractmethod
    def handle_request(self, day) -> None:
        pass


class PresidentHandler(Handler):
    """具体处理者"""

    def handle_request(self, day) -> None:
        if day <= 3:
            print("部门经理审批通过")
        else:
            SubjectHandler().handle_request(day)


class SubjectHandler(Handler):
    """具体处理者"""

    def handle_request(self, day) -> None:
        if day <= 5:
            print("区域经理审批通过")
        else:
            ProjectHandler().handle_request(day)


class ProjectHandler(Handler):
    """具体处理者"""

    def handle_request(self, day) -> None:
        if day <= 10:
            print("总经理审批通过")
        else:
            print("驳回你丫的")


# client
if __name__ == '__main__':
    day = 11
    handler = PresidentHandler()
    handler.handle_request(day)
