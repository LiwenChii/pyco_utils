import time


class CachePool(object):
    '''
    缓存池，用来存放短信(MongoMixin的子类)，控制短信的发送

    '''
    data = []
    is_active = True

    # 缓存池队列的存储数据量的最大值
    maximum = 300

    # 队列中第一个数据的时间戳
    timestamp_first = 0

    # 队列中最后一个数据的时间戳
    timestamp_last = 0

    # 缓存数据的保持时间，默认十分钟
    hold_time = 10 * 60

    # 爆栈后的冷却时间，默认十分钟
    cool_time = 10 * 60

    def __init__(self, **kwargs):
        self.maximum = kwargs.get('maximum', self.maximum)
        self.hold_time = kwargs.get('hold_time', self.hold_time)
        self.cool_time = kwargs.get('cool_time', self.cool_time)

    def count(self):
        c = len(self.data)
        return c

    def clear(self):
        # 清理超时的数据
        ts = self.timestamp_last - self.hold_time
        if ts > self.timestamp_first:
            ds = []
            for i, m in enumerate(self.data):
                if m.created_time >= ts:
                    ds = self.data[i:]
                    self.timestamp_first = m.created_time
                    break
            self.data = ds

    def cool(self):
        # TODO 冷却机制
        if not self.is_active:
            ts = int(time.time()) - self.timestamp_last
            if ts > self.cool_time:
                self.is_active = True
            else:
                print('数据溢出危机未解除，仍然冷却中。')

    def is_cool(self):
        self.cool()
        return self.is_active

    def refresh(self):
        # 检查缓存池，如果过量，更新状态
        self.clear()
        if self.count() > self.maximum:
            self.is_active = False
            print('数据溢出，混存池即将冷却。')
        return self.is_active

    def push(self, item):
        '''
        入口，缓存池进数据，
        先检查冷却状态，如果可以存放数据，成功后要更新
        '''
        if self.is_cool():
            self.data.append(item)
            self.timestamp_last = int(time.time())
            self.refresh()
            return True
        else:
            return False


singleSmsPool = CachePool()
