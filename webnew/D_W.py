
guess = int(input('your guess: ' ))
secret = int(input('your secret: '))

def d_w(guess, secret):
    numw = 0
    numd = 0
    i = 0
    guess = str(guess)
    secret = str(secret)

    for x in guess:
        if x in secret:
            numw += 1
            if guess[i] == secret[i]:
                numd += 1
        i += 1

    result = 'you have {numd} dead, {numw} wounded.'.format(numd=numd,numw=numw)
    return result

print(d_w(guess, secret))