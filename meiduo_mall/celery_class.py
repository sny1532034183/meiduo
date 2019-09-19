class Broker(object):
    """
        任务队列
    """

    def __init__(self):
        self.data_list = []


class Worker(object):
    """
        任务执行者
    """

    def delay(self, func, broker):
        if func in broker.data_list:
            func()


class Celery(object):
    def __init__(self):
        self.worker = Worker()
        self.broker = Broker()

    def add_list(self, func):
        """
            添加队列
        :param func:
        :return:
        """
        self.broker.data_list.append(func)


#################
# django

# 定义任务
def send_sms_code():
    print('send_sms_code')


app = Celery()
# app.add_list(send_sms_code)


app.worker.delay(send_sms_code, app.broker)
