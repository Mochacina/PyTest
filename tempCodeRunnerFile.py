print("Hello!")

def test(l):
    for n, i in enumerate(l):
        i = n
    print(l)

if __name__ == "__main__":
    l = [0]*10
    test(l)
    print(l)