from pyco_utils.decorators import (
    pf_time,
    reduce,
    retry,
    retry_api,
    _retry_api,
)

fac = lambda n: reduce(lambda x, y: x * y, range(1, n + 1))


def test_pf_time():
    @pf_time
    def test_fac(n):
        m = fac(n)
        return m

    test_fac(1)
    test_fac(2)
    test_fac(3)
    test_fac(10)


def test_retry_api():
    @retry
    def fac0(n):
        return fac(n)

    @retry_api()
    def fac1(n):
        return fac(n)

    @_retry_api
    def fac2(n):
        return fac(n)

    f0 = fac0(5)
    f1 = fac1(5)
    f2 = fac2(5)
    assert f1 == f2 == f0


if __name__ == '__main__':
    test_pf_time()
    test_retry_api()
