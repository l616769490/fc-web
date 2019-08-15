def  func(user, name):
    print(user)


if __name__ == "__main__":
    d = {'name':'aaa', 'age':18}
    print(func.__code__.co_argcount)
