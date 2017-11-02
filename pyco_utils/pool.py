from time import time


class LimitPool(object):
    '''
    短信发送控制器

    实现如下功能
    1. 根据手机号发送短信
    2. 10 分钟之内最多只能发送 300 条短信
    3. 对于同一个手机号，一分钟只能发送 1 条短信

    '''
    items = []
    _is_active = True

    # 缓存池队列的存储数据量的最大值
    limit = 300

    # 缓存数据的保持时间，默认十分钟
    gap_time = 10 * 60

    # 队列中第一个数据的时间戳
    timestamp_first = 0

    # 队列中最后一个数据的时间戳
    timestamp_last = 0

    @property
    def is_active(self):
        if not self._is_active:
            self.refresh()
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)

    def config(self, **kwargs):
        # 这是个单例模式的类，所以更新配置应该使用这个接口
        self.limit = kwargs.get('limit', self.limit)
        self.gap_time = kwargs.get('gap_time', self.gap_time)

    def count(self):
        c = len(self.items)
        return c

    def clear(self):
        # 清理超时的数据
        ts = self.timestamp_last - self.gap_time
        if ts > self.timestamp_first:
            ds = []
            for i, m in enumerate(self.items):
                ct = m['created_time']
                if ct >= ts:
                    ds = self.items[i:]
                    self.timestamp_first = ct
                    break
            self.items = ds

    def refresh(self):
        # 检查缓存池，如果过量，更新状态
        self.clear()
        if self.count() > self.limit:
            self._is_active = False
            print('数据溢出，混存池即将冷却。')
        return self._is_active

    def push(self, data):
        '''
        入口，缓存池进数据，
        先检查冷却状态，如果可以存放数据，成功后要更新
        '''
        if self.is_active:
            data['created_time'] = int(time())
            self.items.append(data)
            self.timestamp_last = int(time())
            self.refresh()
            return data


class CyberPool(LimitPool):
    # 爆栈后的冷却时间，默认十分钟
    cool_time = 10 * 60

    def config(self, **kwargs):
        # 这是个单例模式的类，所以更新配置应该使用这个接口
        super(CyberPool, self).config()
        self.cool_time = kwargs.get('cool_time', self.cool_time)

    def cool(self):
        # TODO 冷却机制
        ts = int(time()) - self.timestamp_last
        if ts > self.cool_time:
            self.is_active = True
        else:
            print('数据溢出危机未解除，仍然冷却中。')

    def refresh(self):
        # 检查缓存池，如果过量，更新状态
        super(CyberPool, self).refresh()
        if not self.is_active:
            self.cool()
