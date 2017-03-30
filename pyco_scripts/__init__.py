from manager import Manager
# pip install manage.py

manager = Manager()


@manager.command
def command(args, kwargs=''):
    '''
    eg: python manage.py command args --kwargs='xxx'
    '''
    print(args, type(args))
    print(kwargs, type(kwargs))




if __name__ == '__main__':
    manager.main()
