print("Hello!")

def test(l):
    for n in range(len(l)):
        l[n] = n
    print(l)

if __name__ == "__main__":
    l = [0]*10
    test(l)
    print(l)