from django.http import HttpResponse
from django.shortcuts import render
from . import GPcalc
import operator

from pymongo import MongoClient

Myclient = MongoClient("mongodb://localhost:27017/")
mydb = Myclient["LairDatabase"]
Mycol = mydb["Users"]


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

    name = username
    password = password

    if col.find({'username': name}).count():
        pass
    else:
        col.insert_one({'username':name,'Password':password})

    for lu in col.find({'username': name}):
        Login_name = lu['username']
        Login_name = Login_name.capitalize()

    return render(request, 'loggedin.html',{'username':Login_name})


def home(request):

    return render(request,'index.html', {'key1':'I am going far'})

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

    zipped = list(zip(index, codes,units,scores))

    if 'None' in codes:
        GPA = 'NULL'
    else:
        GPA, gradeletters = GPcalc.gpcalc(codes, units, scores)

    zipped = list(zip(index, codes, units, scores, gradeletters))

    return render(request, 'GPAresult.html',
                  {'coursecodes':codes,'units':units,'scores':scores,'zip': zipped, 'GPA':GPA})


def signup(request):

    return render(request, 'signup.html')

def loggedin(request,col=Mycol):

    for lu in col.find({'username':name}):
        Login_name = lu['username']
        Login_name = Login_name.capitalize()

    return render(request, 'loggedin.html',{'username':Login_name})

def forgotpassword(request):
    return render(request, 'forgotpassword.html')

def DandW(request):
    return render(request, 'D&W.html')

def aboutDandW(request):
    return render(request, 'aboutD&W.html')

def CompPlay(request):
    return render(request, 'compD&W.html')

def secret_1(request):
    return render(request, 'secret1.html')

def secret_2(request):
    return render(request, 'secret2.html')

def winner(request):
    return render(request, 'winner_D&W.html')

def giveup(request):
    return render(request, 'giveup.html')