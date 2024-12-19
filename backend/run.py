from launcher import threads, shutdown
from logging_config import setup_logging

if __name__ == '__main__':
    setup_logging()
    out = threads()

    while True:
        print('input command:')
        command = input()
        if command == '1':
            out = threads()
            print('out', out)
        elif command == '2':
            out = shutdown()
        else:
            print('commandNameError')

# import time 
# import multiprocessing

# def t1():
#     time.sleep(4)
#     print('hellow')

# if __name__ == '__main__':
#     t = multiprocessing.Process(target=t1, args=())
#     t.start()
#     print('xo xo')