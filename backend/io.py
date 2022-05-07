from launcher import threads, shutdown
from gui import run

if __name__ == '__main__':
    out = threads()
    run.init(out)

    # while True:
    #     print('input command:')
    #     command = input()
    #     if command == '1':
    #         out = threads()
    #         print(out)
    #     elif command == '2':
    #         out = shutdown()
    #     else:
    #         print('commandNameError')

# import time 
# import multiprocessing

# def t1():
#     time.sleep(4)
#     print('hellow')

# if __name__ == '__main__':
#     t = multiprocessing.Process(target=t1, args=())
#     t.start()
#     print('xo xo')