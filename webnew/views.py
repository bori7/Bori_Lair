from django.http import HttpResponse
from django.shortcuts import render
from . import GPcalc, D_W
import operator
import random
from pymongo import MongoClient

Myclient = MongoClient('mongodb://oluwabori:moses2490@ds331548.mlab.com:31548/heroku_z0sxdn7q',connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
mydb = Myclient.get_default_database()
Mycol = mydb["oluwabori"]


'''
def Database(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]


    username = request.GET['usernamesignin']
    password = request.GET['passwordsignin']
    coursecode = request.GET['coursecode']
    courseunit = request.GET['courseunit']
    score = request.GET['score']

    mydict = {"username" : username, 'Password':password, 'CourseCode':coursecode,
              'CourseUnit':courseunit, 'Score': score}

    x = mycol.insert_one(mydict)
    return mycol
    
'''



'''
def home(request):
    return HttpResponse('<hi>Welcome, This is working</hi>')

def downloads(request):
    return HttpResponse('<hi>Welcome, This is where you download</hi>')
'''


def add_user(request, col = Mycol):

    username = request.POST['usernamesignin']
    password = request.POST['passwordsignin']

    global name

    name = username.lower()
    password = password

    if col.find({'username': name}).count():
        iup = col.find_one({'username': name})
        passwordreal =  iup['Password']
        if str(password) == str(passwordreal):
            pass
        else:
            return render(request, 'doesnotexist.html',{'message':'Wrong username or password'})

    else:
        return render(request, 'signup.html', {'message':'that user does not exist'})

    for lu in col.find({'username': name}):
        Login_name = lu['username']
        Login_name = Login_name.capitalize()

    return render(request, 'loggedin.html',{'username':Login_name})


def home(request):

    return render(request,'index.html')

def downloads(request):
    return HttpResponse('<hi>Welcome, This is where you download</hi>')

def result(request):

    article = request.GET['coursecode']
    words = article.split()
    word_count = len(words)
    dict_words = {}

    for word in words:
        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1
    var_dict = sorted(dict_words.items(),key = operator.itemgetter(1),reverse=True)
    age = request.GET['user_age']
    name = request.GET['user_name']
    message = f"hello {name}, you are {age} years old"
    return render(request,'result.html',{'message':message, 'article':article,'word_count':word_count, 'dict_words': var_dict})


'''def GPAcalculate(request):
    course_codes =[]
    course_units =[]
    scores = []
    coursecode = request.GET['coursecode']
    course_codes.append(coursecode)
    courseunit = request.GET['courseunit']
    course_units.append(courseunit)
    score = request.GET['score']
    scores.append(score)
    GPA = GPcalc.gpcalc(course_codes,course_units,scores)

    return GPA'''

def GPAcalcu(request,col = Mycol):

    username = name
    iup = col.find_one({'username': username})

    if  'courses' in iup.keys():
        pass
    else:
        col.update_one({'username': username},
                       {"$set": {'courses': {'coursecodes': [],
                                             'courseunits': [],
                                             'scores': []}}})

    iup = col.find_one({'username': username})
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']

    if len(codes) == 0:
        codes, units, scores = ['None'] , ['None'], ['None']
        col.update_one({'username': name},
                       {"$set": {'courses': {'coursecodes': codes, 'courseunits': units, 'scores': scores}}})
    else:
        pass



    index = []
    for i in range(len(codes)):
        index.append(i+1)

    zipped = list(zip(index, codes, units, scores))
    return render(request, 'GPA.html', {'coursecodes':codes,'units':units,'scores':scores,'zip': zipped})


def GPAcalcuadd(request, col=Mycol):

    coursecode = request.POST['coursecode']
    courseunit = request.POST['courseunit']
    score = request.POST['score']

    user = col.find_one({'username': name})

    user['courses']['coursecodes'].append(coursecode)
    newcourses = user['courses']['coursecodes']
    user['courses']['courseunits'].append(courseunit)
    newunits = user['courses']['courseunits']
    user['courses']['scores'].append(score)
    newscores = user['courses']['scores']

    col.update_one({'username': name},
                   {"$set": {'courses': {'coursecodes': newcourses,'courseunits': newunits,'scores': newscores}}})

    iup = col.find_one({'username': name})

    #table work
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']

    if 'None' in codes:
        codes.remove('None')
        units.remove('None')
        scores.remove('None')
        col.update_one({'username': name},
                       {"$set": {'courses': {'coursecodes': codes, 'courseunits': units, 'scores': scores}}})

    else:
        pass

    iup = col.find_one({'username': name})
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']

    index = []
    for i in range(len(codes)):
        index.append(i+1)

    zipped = list(zip(index, codes, units, scores))
    return render(request, 'GPA.html', {'coursecodes':codes,'units':units,'scores':scores,'zip': zipped})



def GPAcalcudel(request, col=Mycol):

    index = request.POST['index']
    index = int(index) - 1

    iup = col.find_one({'username': name})

    #table work
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']

    codes.remove(codes[index])
    units.remove(units[index])
    scores.remove(scores[index])
    col.update_one({'username': name},
                       {"$set": {'courses': {'coursecodes': codes, 'courseunits': units, 'scores': scores}}})


    if len(codes) == 0:
        codes, units, scores = ['None'] , ['None'], ['None']
        col.update_one({'username': name},
                       {"$set": {'courses': {'coursecodes': codes, 'courseunits': units, 'scores': scores}}})
    else:
        pass


    iup = col.find_one({'username': name})
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']

    index = []
    for i in range(len(codes)):
        index.append(i+1)


    zipped = list(zip(index, codes,units,scores))
    return render(request, 'GPA.html', {'coursecodes':codes,'units':units,'scores':scores,'zip': zipped})


def GPAresult(request, col = Mycol):

    iup = col.find_one({'username': name})
    codes = iup['courses']['coursecodes']
    units = iup['courses']['courseunits']
    scores = iup['courses']['scores']
    index = []
    for i in range(len(codes)):
        index.append(i+1)



    if 'None' in codes:
        GPA = 'NULL'
    else:
        GPA, gradeletters = GPcalc.gpcalc(codes, units, scores)
        GPA = "{:.2f}".format(GPA)

    zipped = list(zip(index, codes, units, scores, gradeletters))

    return render(request, 'GPAresult.html',
                  {'coursecodes':codes,'units':units,'scores':scores,'zip': zipped, 'GPA':GPA})


def signup(request):
    message = ''
    return render(request,'signup.html',{'message':message})


def addsignup(request, col=Mycol):

    usernamesignup = request.POST['usernamesignup']
    passwordsignup = request.POST['passwordsignup']
    passwordcheck = request.POST['passwordcheck']

    usernamesignup = usernamesignup.lower()

    if col.find({'username': usernamesignup}).count():
        message = "that user exists"
        return render(request, 'doesnotexist.html', {'message': message})

    else:
        pass

    if str(passwordsignup) != str(passwordcheck):
        message = 'passwword validation failed'
        return render(request, 'signup.html', {'message': message})
    else:
        pass

    passwordsignup = passwordsignup.lower()
    col.insert_one({'username':usernamesignup,'Password':passwordsignup})


    return render(request, 'index.html')

def loggedin(request,col=Mycol):

    for lu in col.find({'username':name}):
        Login_name = lu['username']
        Login_name = Login_name.capitalize()

    return render(request, 'loggedin.html',{'username':Login_name})


def forgotpassword(request):

    return render(request, 'forgotpassword.html')


def keyreset(request,col = Mycol):

    usernamereset = request.POST['usernamereset']
    passwordreset = request.POST['passwordreset']
    passwordcheckreset = request.POST['passwordcheckreset']

    if col.find({'username': usernamereset}).count():
        pass
    else:
        message = 'this user does not exist'
        return render(request, 'resetpassword.html', {'message': message })

    if str(passwordreset) != str(passwordcheckreset):
        message = 'passwword validation failed'
        return render(request, 'resetpassword.html', {'message': message})
    else:
        pass

    myquery = {'username': usernamereset}
    newvalues = {"$set": {"Password": passwordreset}}

    col.update_one(myquery, newvalues)

    return render(request, 'index.html')


def resetpassword(request):

    return render(request, 'resetpassword.html',{'message': ''})



def DandW(request, col = Mycol):

    username = name
    iup = col.find_one({'username': username})

    if 'D_W' in iup.keys():
        pass
    else:
        col.update_one({'username': username},
                       {"$set": {'D_W': {'guess1': [],
                                         'guess2': [],
                                         'score1': [],
                                         'score2': [],
                                         'secret1': "0000",
                                         'secret2': "0000"}}})


    iup = col.find_one({'username': username})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    if len(guess1) == 0:

        guess1, score1 = ['None'], ['None']
        col.update_one({'username': name},
                       {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                 'score1': score1, 'score2' : score2,
                                 'secret1': secret1, 'secret2': secret2 }}})
    else:
        pass

    iup = col.find_one({'username': username})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    if len(guess2) == 0:

        guess2, score2 = ['None'], ['None']
        col.update_one({'username': name},
                       {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                         'score1': score1, 'score2': score2,
                                         'secret1': secret1, 'secret2': secret2}}})
    else:
        pass



    index1 = []
    for i in range(len(guess1)):
        index1.append(i + 1)

    index2 = []
    for i in range(len(guess2)):
        index2.append(i + 1)

    zipped1 = list(zip(index1, guess1, score1))
    zipped2 = list(zip(index2, guess2, score2))
    return render(request, 'D&W.html', {'zip1': zipped1, 'zip2': zipped2})


def aboutDandW(request):

    return render(request, 'aboutD&W.html')

def CompPlay(request, col = Mycol):


    secert = ''.join(map(str, random.sample(range(10), 4)))


    username = name
    iup = col.find_one({'username': username})


    if 'CompD_W' in iup.keys():
        pass
    else:
        col.update_one({'username': username},
                       {"$set": {'CompD_W': {'Compguess': [],
                                         'Compscore': [],
                                         'Compsecret':secert}}})


    iup = col.find_one({'username': username})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']

    if len(guess) == 0:

        guess, score = ['None'], ['None']
        col.update_one({'username': name},
                       {"$set": {'CompD_W': {'Compguess': guess,
                                 'Compscore': score,
                                 'Compsecret':secret}}})
    else:
        pass

    iup = col.find_one({'username': username})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']

    index = []
    for i in range(len(guess)):
        index.append(i + 1)


    zipped = list(zip(index, guess, score))

    return render(request, 'compD&W.html', {'zip': zipped, 'username': username})


def Compsubmit(request, col = Mycol):

    username = name
    iup = col.find_one({'username': username})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']


    gue = request.POST['guess']

    olu = str(gue)
    um = []
    for i in olu:
        if olu.count(i) > 1:
            um.append(True)
        else:
            um.append(False)

    if True in um:
        return render(request, 'Comperrorrepeat.html',{'message':'a digit in your guess is recurring'})
    else:
        pass

    if len(olu) < 4:
        return render(request, 'Comperrorrepeat.html',{'message':'your guess has to be 4 digits'})
    else:
        pass


    nl = len(guess) + 1

    if str(gue) == str(secret):

        return render(request, 'Compwinner_D&W.html', { 'nl': nl,
                                                   'secret': secret})
    else:
        pass

    res = D_W.d_w(gue, secret)

    user = col.find_one({'username': name})
    user['CompD_W']['Compguess'].append(gue)
    newguess = user['CompD_W']['Compguess']
    user['CompD_W']['Compscore'].append(res)
    newscore = user['CompD_W']['Compscore']

    col.update_one({'username': name},
                   {"$set": {'CompD_W': {'Compguess': newguess,
                                         'Compscore': newscore,
                                         'Compsecret': secret}}})


    iup = col.find_one({'username': name})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']


    if 'None' in guess:
        guess.remove('None')
        score.remove('None')
        col.update_one({'username': name},
                       {"$set": {'CompD_W': {'Compguess': guess,
                                             'Compscore': score,
                                             'Compsecret': secret}}})

    else:
        pass

    iup = col.find_one({'username': name})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']

    index = []
    for i in range(len(guess)):
        index.append(i + 1)


    zipped = list(zip(index, guess, score))

    return render(request, 'compD&W.html', {'zip': zipped,'username':username})


def secret_1(request):
    return render(request, 'secret1.html')

def secret_2(request):
    return render(request, 'secret2.html')


def hide_1(request, col = Mycol):

    secret = request.POST['secret1']

    olu = str(secret)
    um = []
    for i in olu:
        if olu.count(i) > 1:
            um.append(True)
        else:
            um.append(False)

    if True in um:
        return render(request, 'errorrepeat.html', {'message': 'a digit in your secret number is recurring'})
    else:
        pass

    if len(olu) < 4:
        return render(request, 'errorrepeat.html', {'message': 'the secret number has to be 4 digits'})
    else:
        pass


    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    col.update_one({'username': name},
                   {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                     'score1': score1, 'score2': score2,
                                     'secret1': secret, 'secret2': secret2}}})
    index = []
    for i in range(len(guess1)):
        index.append(i + 1)

    zipped = list(zip(index, guess1, score1, guess2, score2))
    return render(request, 'D&W.html', {'zip': zipped})


def hide_2(request,col = Mycol):

    secret = request.POST['secret2']

    olu = str(secret)
    um = []
    for i in olu:
        if olu.count(i) > 1:
            um.append(True)
        else:
            um.append(False)

    if True in um:
        return render(request, 'errorrepeat.html', {'message': 'a digit in your secret number is recurring'})
    else:
        pass

    if len(olu) < 4:
        return render(request, 'errorrepeat.html', {'message': 'the secret number has to be 4 digits'})
    else:
        pass


    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    col.update_one({'username': name},
                   {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                     'score1': score1, 'score2': score2,
                                     'secret1': secret1, 'secret2': secret}}})

    index = []
    for i in range(len(guess1)):
        index.append(i + 1)

    zipped = list(zip(index, guess1, score1, guess2, score2))
    return render(request, 'D&W.html', {'zip': zipped})

def submit1(request, col = Mycol):

    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']


    if secret2 == "0000" :
        return render(request, 'errorsecret.html',{'mess':'P2'})

    else:
        pass

    guess = request.POST['guess1']

    olu = str(guess)
    um = []
    for i in olu:
        if olu.count(i) > 1:
            um.append(True)
        else:
            um.append(False)

    if True in um:
        return render(request, 'errorrepeat.html',{'message':'a digit in your guess is recurring'})
    else:
        pass

    if len(olu) < 4:
        return render(request, 'errorrepeat.html',{'message':'your guess has to be 4 digits'})
    else:
        pass

    P = 1
    nl = len(guess1) + 1

    if str(guess) == str(secret2):

        return render(request, 'winner_D&W.html', {'P': P, 'nl': nl,
                                                   'secret1': secret1,
                                                   'secret2': secret2})
    else:
        pass

    res = D_W.d_w(guess, secret2)

    user = col.find_one({'username': name})
    user['D_W']['guess1'].append(guess)
    newguess = user['D_W']['guess1']
    user['D_W']['score1'].append(res)
    newscore = user['D_W']['score1']



    col.update_one({'username': name},
               {"$set": {'D_W': {'guess1': newguess, 'guess2': guess2,
                                 'score1': newscore, 'score2': score2,
                                 'secret1': secret1, 'secret2': secret2}}})

    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    if 'None' in guess1:
        guess1.remove('None')
        score1.remove('None')
        col.update_one({'username': name},
                   {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                     'score1': score1, 'score2': score2,
                                     'secret1': secret1, 'secret2': secret2}}})
    else:
        pass



    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    index1 = []
    for i in range(len(guess1)):
        index1.append(i + 1)

    index2 = []
    for i in range(len(guess2)):
        index2.append(i + 1)

    zipped1 = list(zip(index1, guess1, score1))
    zipped2 = list(zip(index2, guess2, score2))


    return render(request, 'D&W.html', {'zip1': zipped1, 'zip2': zipped2})

def submit2(request, col = Mycol):


    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']


    if secret1 == "0000"  :
        return render(request, 'errorsecret.html',{'mess':'P1'})

    else:
        pass

    guess = request.POST['guess2']



    olu = str(guess)
    um = []
    for i in olu:
        if olu.count(i) > 1:
            um.append(True)
        else:
            um.append(False)

    if True in um:
        return render(request, 'errorrepeat.html', {'message': 'a digit in your guess is recurring'})
    else:
        pass

    if len(olu) < 4:
        return render(request, 'errorrepeat.html', {'message': 'the guess has to be 4 digits'})
    else:
        pass



    P = 2
    nl = len(guess2) + 1

    if str(guess) == str(secret1):

        return render(request, 'winner_D&W.html', {'P': P, 'nl': nl,
                                                   'secret1': secret1,
                                                   'secret2': secret2})
    else:
        pass



    res = D_W.d_w(guess, secret1)

    user = col.find_one({'username': name})
    user['D_W']['guess2'].append(guess)
    newguess = user['D_W']['guess2']
    user['D_W']['score2'].append(res)
    newscore = user['D_W']['score2']

    col.update_one({'username': name},
               {"$set": {'D_W': {'guess1': guess1, 'guess2': newguess,
                                 'score1': score1, 'score2': newscore,
                                 'secret1': secret1, 'secret2': secret2}}})

    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    if 'None' in guess2:
        guess2.remove('None')
        score2.remove('None')
        col.update_one({'username': name},
                    {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                        'score1': score1, 'score2': score2,
                                      'secret1': secret1, 'secret2': secret2}}})
    else:
        pass

    iup = col.find_one({'username': name})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    index1 = []
    for i in range(len(guess1)):
        index1.append(i + 1)

    index2 = []
    for i in range(len(guess2)):
        index2.append(i + 1)

    zipped1 = list(zip(index1, guess1, score1))
    zipped2 = list(zip(index2, guess2, score2))


    return render(request, 'D&W.html', {'zip1': zipped1, 'zip2': zipped2})


def winner(request, col =Mycol):

    iup = col.find_one({'username': name})
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']


    n = request.POST['n']

    if n == "1":
        P = 2
        nl = len(guess2)
    elif n == "2":
        P = 1
        nl = len(guess1)

    if 'None' in guess1 or 'None' in guess2:
        nl = 'None'
    else:
        pass

    if  secret1 == "0000" :
        secret1 = 'None'
    else:
        pass

    if  secret2 == "0000" :
        secret2 = 'None'
    else:
        pass

    return render(request, 'winner_D&W.html',{'P' : P,'nl': nl,
                                              'secret1':secret1,
                                              'secret2':secret2})


def Compwinner(request, col =Mycol):


    iup = col.find_one({'username': name})
    guess = iup['CompD_W']['Compguess']
    secret = iup['CompD_W']['Compsecret']


    nl = len(guess)

    if 'None' in guess:
        nl = 'None'
    else:
        pass


    return render(request, 'Compwinner_D&W.html',{'nl': nl,
                                              'secret1':secret})


def loser(request, col =Mycol):

    iup = col.find_one({'username': name})
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']


    n = request.POST['n']

    if n == "1":
        P = 1
        nl = len(guess1)
    elif n == "2":
        P = 2
        nl = len(guess2)

    if 'None' in guess1 or 'None' in guess2:
        nl = 'None'
    else:
        pass

    if  secret1 == "0000" :
        secret1 = 'None'
    else:
        pass

    if  secret2 == "0000" :
        secret2 = 'None'
    else:
        pass

    return render(request, 'loser_D&W.html',{'P' : P,'nl': nl,
                                              'secret1':secret1,
                                              'secret2':secret2})


def reset(request, col=Mycol):

    username = name

    guess1, score1 = ['None'], ['None']
    guess2, score2 = ['None'], ['None']
    secret1, secret2 = '0000', '0000'

    col.update_one({'username': name},
                       {"$set": {'D_W': {'guess1': guess1, 'guess2': guess2,
                                         'score1': score1, 'score2': score2,
                                         'secret1': secret1, 'secret2': secret2}}})

    iup = col.find_one({'username': username})
    guess1 = iup['D_W']['guess1']
    guess2 = iup['D_W']['guess2']
    secret1 = iup['D_W']['secret1']
    secret2 = iup['D_W']['secret2']
    score1 = iup['D_W']['score1']
    score2 = iup['D_W']['score2']

    index1 = []
    for i in range(len(guess1)):
        index1.append(i + 1)

    index2 = []
    for i in range(len(guess2)):
        index2.append(i + 1)

    zipped1 = list(zip(index1, guess1, score1))
    zipped2 = list(zip(index2, guess2, score2))
    return render(request, 'D&W.html', {'zip1': zipped1, 'zip2': zipped2})

def Compreset(request, col=Mycol):

    username = name

    guess = ['None']
    score = ['None']
    secret = ''.join(map(str,random.sample(range(10), 4)))

    col.update_one({'username': name},
                   {"$set": {'CompD_W': {'Compguess': guess,
                                         'Compscore': score,
                                         'Compsecret': secret}}})


    iup = col.find_one({'username': username})
    guess = iup['CompD_W']['Compguess']
    score = iup['CompD_W']['Compscore']
    secret = iup['CompD_W']['Compsecret']


    index = []
    for i in range(len(guess)):
        index.append(i + 1)

    zipped = list(zip(index, guess, score))

    return render(request, 'compD&W.html', {'zip': zipped,
                                            'username':username})


def giveup(request,col = Mycol):

    iup = col.find_one({'username': name})
    secret = iup['CompD_W']['Compsecret']

    return render(request, 'giveup.html', {'secret':secret})