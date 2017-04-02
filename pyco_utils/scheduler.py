from datetime import datetime, timedelta
import time

from .logger import log
from .decorators import retry

ONE_DAY = 24 * 3600
ONE_HOUR = 3600
HALF_HOUR = 1800
ONE_MINUTE = 60
INFINITE_LIFE = -1
RETRY_COUNT = 3


def scheduler(func, *args, **kwargs):
    '''
    :param func: target func
    :param options : times, delay ,schedule,retry
    '''
    name = func.__name__
    delay = kwargs.pop('delay', False)
    period = kwargs.pop('period', ONE_DAY)
    retry_count = kwargs.pop('retry', RETRY_COUNT)
    times = int(kwargs.pop('times', INFINITE_LIFE))

    if isinstance(period, timedelta):
        period = period.seconds + period.days * ONE_HOUR
    else:
        period = int(period)

    if delay and isinstance(delay, int):
        time.sleep(delay)
        log('Scheduler gap {} seconds'.format(delay))

    while times:
        now = datetime.today()
        result = retry(func, count=retry_count)(*args, **kwargs)
        times -= 1
        if times > 0:
            msg = '[Scheduler] <{}> is running at {} , still < {} > times.'.format(name, now, times)
        else:
            tm = 0 - times + 1
            msg = '[Scheduler] <{}> is running at {} , already < {} > times.'.format(name, now, tm)
        log(msg, args=args, result=result, **kwargs)
        time.sleep(period)

    end = datetime.today()
    msg = '[Scheduler] <{}> ended at {}'.format(name, end)
    log(msg, delay=delay, perido=period, times=times)
