import requests
from config import token
from time import sleep


def createGenerator(memes):
    for meme in memes:
        yield meme


def one():
    print(next_meme.__next__())


def two():
    print(next_meme.__next__())


if __name__ == '__main__':
    m = [1, 2, 3, 4, 5, 6, 7, 8]
    next_meme = createGenerator(m)
    one()
    two()
    print(next_meme.__sizeof__())
