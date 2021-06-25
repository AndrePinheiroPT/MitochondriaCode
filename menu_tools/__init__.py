from time import sleep

def line(length = 60):
    print('~' * length)

    
def countdown():
    print('Starting the simulation in:')
    for cout in range(3, 0, -1):
        print(cout)
        sleep(1)


def read_int(message):
    while True:
        try:
            value = int(input(message))
        except (ValueError, TypeError):
            print('ERROR: please, type a valid integer!')
            continue
        except (KeyboardInterrupt):
            print('The input of data was interrupted!')
            return 0
        else:
            return value
