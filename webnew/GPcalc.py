import numpy as np

def gpcalc(coursecodes,units,scores):


    for i in range(len(units)):
        units[i] = int(units[i])

    for i in range(len(scores)):
        scores[i] = int(scores[i])

    gradescore = []
    gradeletters = []
    unitsarr = np.array(units)
    totalunits = sum(unitsarr)

    for score in scores:
        if int(score) >= 70:
            grade = 5
            gradescore.append(grade)
            gradeletter = 'A'
            gradeletters.append(gradeletter)

        elif score < 70 and score >= 60:
            grade = 4
            gradescore.append(grade)
            gradeletter = 'B'
            gradeletters.append(gradeletter)

        elif score < 60 and score >= 50:
            grade = 3
            gradescore.append(grade)
            gradeletter = 'C'
            gradeletters.append(gradeletter)

        elif score < 50 and score >= 45:
            grade = 2
            gradescore.append(grade)
            gradeletter = 'D'
            gradeletters.append(gradeletter)

        elif score < 45 and score >= 40:
            grade = 1
            gradescore.append(grade)
            gradeletter = 'E'
            gradeletters.append(gradeletter)

        elif score < 40 :
            grade = 0
            gradescore.append(grade)
            gradeletter = 'F'
            gradeletters.append(gradeletter)

        else:
            grade = -1
            gradescore.append(grade)
            gradeletter = 'invalid'
            gradeletters.append(gradeletter)
            #print(score, " is an invalid score ")


    gradescorearr = np.array(gradescore)

    gradepointarr = gradescorearr * unitsarr
    totalgradepoint = sum(gradepointarr)

    GPA = totalgradepoint/totalunits


    #for coursecode, grade in zip(coursecodes,gradescore):
     #   pass
        #print('{couresecode} : {grade}\n'.format(coursecode=coursecode,grade=grade))

    #print('This is GradepointAverage : {GPA}'.format(GPA = GPA))

    return GPA, gradeletters