
#guess = int(input('your guess: ' ))
#secret = int(input('your secret: '))

def d_w(guess, secret):
    numw = 0
    numd = 0
    i = 0
    guess = str(guess)
    secret = str(secret)

    for x in guess:
        if x in secret and  guess[i] == secret[i]:
            numd += 1
            numw +=0
        elif x in secret:
            numw += 1
            numd += 0
        i += 1

    result = '{numd} D : {numw} W'.format(numd=numd,numw=numw)
    return result

#print(d_w(guess, secret))