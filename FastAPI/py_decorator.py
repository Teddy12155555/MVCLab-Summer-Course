# FastAPI Basic Practice
import time

def print_func_name(func):
    def warp():
        print("Now use function '{}'".format(func.name))
        func()
    return warp


def print_time(func):
    def warp2():
        print('Now the Unix time is {}'.format(int(time.time())))
        func()
    return warp2

@print_func_name
def dog_bark():
    print("Bark !!!")


@print_func_name
def cat_miaow():
    print("Miaow ~~~")


@print_func_name
@print_time
def human_bark():
    print('Ohhhh BBQ !')


if __name__ == "__main__":
    dog_bark()
    # > Now use function 'dog_bark'
    # > Bark !!!

    cat_miaow()
    # > Now use function 'cat_miaow'
    # > Miaow ~~~

    human_bark()
    # > Now use function 'warp2'
    # > Now the Unix time is ....
    # > Ohhhh BBQ !