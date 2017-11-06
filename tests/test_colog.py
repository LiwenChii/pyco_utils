"""

__get__,__getattr__和__getattribute都是访问属性的方法，但不太相同。
object.__getattr__(self, name)
当一般位置找不到attribute的时候，会调用getattr，返回一个值或AttributeError异常。

object.__getattribute__(self, name)
无条件被调用，通过实例访问属性。如果class中定义了__getattr__()，则__getattr__()不会被调用
（除非显示调用或引发AttributeError异常）

object.__get__(self, instance, owner)
如果class定义了它，则这个class就可以称为descriptor。
owner是所有者的类，instance是访问descriptor的实例，
如果不是通过实例访问，而是通过类访问的话，instance则为None。

（descriptor的实例自己访问自己是不会触发__get__，而会触发__call__，只有descriptor作为其它类的属性才有意义。）

"""

from pyco_utils.colog import Mlog


class A(Mlog):
    as1 = 1111

    def api_x(self, a, b='x'):
        return a + 2, b + 'xx'


a = A()
a.api_x(1)
print(111111111111111, a.api_x(11))
print(a.api_x.__name__)
print(a.as1)
print(a.as2)
print(a.as3(2, 3, c=11111))

# print(a.as1(1,2))
