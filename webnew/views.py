from django.http import HttpResponse
from django.shortcuts import render
from . import GPcalc




import operator
'''
def home(request):
    return HttpResponse('<hi>Welcome, This is working</hi>')

def downloads(request):
    return HttpResponse('<hi>Welcome, This is where you download</hi>')

'''
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
    var_dict=sorted(dict_words.items(),key = operator.itemgetter(1),reverse=True)
    age = request.GET['user_age']
    name = request.GET['user_name']
    message = f"hello {name}, you are {age} years old"
    return render(request,'result.html',{'message':message, 'article':article,'word_count':word_count, 'dict_words': var_dict})



def GPAcalc(request):
    course_codes =[]
    course_units =[]
    scores = []
    #coursecode = request.GET['coursecode']
    #course_codes.append(coursecode)
    #courseunit = request.GET['courseunit']
    #course_units.append(courseunit)
    #score = request.GET['score']
    #scores.append(score)
    #GPA = GPcalc.gpcalc(course_codes,course_units,scores)
    GPA = GPcalc
    return render(request, 'GPA.html',{'GPA':GPA})

def GPAresult(request):

    GPA = GPcalc
    return render(request, 'GPAresult.html',{'GPA':GPA})

def signup(request):

    return render(request, 'signup.html')

def loggedin(request):
    #username = request.GET['username']
    username = 'LOVE'
    return render(request, 'loggedin.html',{'username':username})

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