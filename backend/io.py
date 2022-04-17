

from launcher import threads
while True:
    print('input command:')
    command = input()
    if command == '1':
        out = threads()
        print(out)
    elif command == '2':
        out = shutdown()
    else:
        print('commandNameError')