from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import PostForm
from .models import Post2
import datetime
import json
import pandas as pd

# Create your views here.
def post_list(request):
    return render(request, "home/start.html", {})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
        return redirect('show')
    else:
        form = PostForm()
    return render(request, 'home/form.html', {'form': form})

def show(request):
    days = {
        "Monday": '1',
        "Tuesday": '2',
        "Wednesday": '3',
        "Thursday": '4',
        "Friday": '5',
        "Saturday": '6',
        "sunday": '7'
    }
    treports=Post2.objects.all()
    k = treports[len(treports)-1]
    #our algorithm
    s = k.source
    d = k.dest
    f = k.date
    day,mnth,year = list(map(int,f.split('/')))
    mydate = datetime.date(year,mnth,day)  #year, month, day
    t=mydate.strftime("%A")
    date=days[t]
    file0 = 'home/static/FINALFLIGHTTEST.json'
    file1 = 'home/static/FINALTRAINTEST.json'
    with open(file0) as flight_file:
        dict_flight = json.load(flight_file)
    flight = pd.DataFrame.from_dict(dict_flight, orient='columns')
    flight.reset_index(level=0, inplace = True)
    with open(file1) as train_file:
        dict_train = json.load(train_file)
    # converting json dataset from dictionary to dataframe
    train = pd.DataFrame.from_dict(dict_train, orient='columns')
    train.reset_index(level=0, inplace=True)
    k = []
    for i in range(0,train.shape[0]):
        b = []
        if train.iloc[i,12] == s.upper():
            if train.iloc[i,7] == d.upper():
                c = list(str(train.iloc[i,5]))
                if date in c:
                    b.append(train.iloc[i,:])
                    k.append(b)
    g = []

    for i in range(0,flight.shape[0]):
        b = []
        if flight.iloc[i,7] == s.upper():
            if flight.iloc[i,10] == d.upper():
                c = list(str(flight.iloc[i,6]))
                if date in c:
                    b.append(flight.iloc[i,:])
                    g.append(b)
    report = pd.DataFrame()
    report2 = pd.DataFrame()
    for m in k:
        r = pd.DataFrame(m)
        report = pd.concat([report,r], axis = 0)
    for m in g:
        f = pd.DataFrame(m)
        report2 = pd.concat([report2,f], axis = 0)
    t = []
    q = []
    flightcon = []
    traincon = []
    for i in range(0,len(report)):
        p = list(report.iloc[i,:])
        t.append(p)

    for i in range(0,len(report2)):
        p = list(report2.iloc[i,:])
        q.append(p)
    print(len(t),len(q))
    #return render(request,"home/result.html",{"t":t, "q":q, "f":flightcon, "tr":traincon})

    f = 0
    h = 0
    if len(q) == 0:
        f = 1
    if len(t) == 0:
        h = 1

    fr = flight.shape[0]
    tr = train.shape[0]

    fsource = []
    for i in range(0,flight.shape[0]):
        if flight.iloc[i,7] not in fsource:
            fsource.append(flight.iloc[i,7])
    fdest = []
    for i in range(0,flight.shape[0]):
        if flight.iloc[i,10] not in fdest:
            fdest.append(flight.iloc[i,10])
            
    tdest = []
    for i in range(0,train.shape[0]):
        if train.iloc[i,7] not in tdest:
            tdest.append(train.iloc[i,7])
    tsource = []
    for i in range(0,train.shape[0]):
        if train.iloc[i,12] not in tsource:
            tsource.append(train.iloc[i,12])


    if f == 1:

        #pre processing connecting flights1
        lev3 = []
        for i in range(0,fr):
            if flight.iloc[i,10] == d.upper():
                if flight.iloc[i,7] not in lev3:
                    lev3.append(flight.iloc[i,7])
        #pre process connecting flights 02
        lev2 = []
        for i in range(0,fr):
            if flight.iloc[i,7] == s.upper():
                if flight.iloc[i,10] in fsource and train.iloc[i,10] != s.upper():
                    if flight.iloc[i,10] in lev3:
                        c = list(str(flight.iloc[i,6]))
                        if date in c:
                            dist = int(round(flight.iloc[i,13]/60))
                            hr = int(flight.iloc[i,9]/100)
                            rtime = dist + hr
                            if rtime > 23:
                                rtime = rtime%24
                                label = int(rtime) * 1000 
                            else:
                                label = rtime
                            d2 = flight.iloc[i,10]
                            fnum = flight.iloc[i,5]
                            l = (d2,label,fnum,i)
                            lev2.append(l)
        #STEP 3

        lev4 = []
        for i in lev3:
            count = 0
            for j in lev2:
                if i == j[0]:
                    lev4.append(j)
                    count = count + 1
                if count == 10:
                    break

        #connecting flights
        k = []
        for i in lev4:
            for j in range(0,fr):
                b = []
                w = []
                if flight.iloc[j,7] == i[0].upper() and flight.iloc[j,10] == d.upper():
                    hr = int(flight.iloc[j,9]/100)
                    if i[1] >= 1000:
                        newdate = str(int(date) + 1)
                        c = list(str(flight.iloc[j,6]))
                        if newdate in c:
                            #print("\n\n\t\tflight 01\n",flight.iloc[i[3],:])
                            #print("\n\n\t\tflight 02\n",flight.iloc[j,:])
                            b.append(flight.iloc[i[3],:])
                            w.append(flight.iloc[j,:])
                            k.append(b)
                            k.append(w)
                            break
                    else:
                        time = i[1]
                        if hr > time:
                            print("\n\n\t\tflight 01\n",flight.iloc[i[3],:])
                            print("\n\n\t\tflight 02\n",flight.iloc[j,:])
                            b.append(flight.iloc[i[3],:])
                            w.append(flight.iloc[j,:])
                            k.append(b)
                            k.append(w)
                            break 
        report3 = pd.DataFrame()
        for m in k:
            r = pd.DataFrame(m)
            report3 = pd.concat([report3,r], axis = 0) 
        for m in range(0,len(report3)):
            p = list(report3.iloc[i,:])
            flightcon.append(m)

    if h == 1:
        #pre process connecting trains
        lev1 = []
        for i in range(0,tr):
            if train.iloc[i,12] == s.upper():
                if train.iloc[i,7] in tsource and train.iloc[i,7] != s.upper():
                    c = list(str(train.iloc[i,5]))
                    if date in c:
                        dist = train.iloc[i,8]
                        if dist < 50:
                            time = 1
                        else:
                            time = int(dist/50)
                        print("time = ", time)
                        hr,_,_ = list(map(int,train.iloc[i,14].split(':')))
                        rtime = time + hr
                        if rtime > 23:
                            label = int(rtime/24) * 1000 
                            print("label = ", label)
                        else:
                            label = rtime
                            print("label = ", label)
                        d2 = train.iloc[i,7]
                        tnum = train.iloc[i,15]
                        l = (d2,label,tnum,i)
                        lev1.append(l)
        #connecting trains

        g = []
        for i in lev1:
            for j in range(0,tr):
                b = []
                w = []
                if train.iloc[j,12] == i[0].upper() and train.iloc[j,7] == d.upper():
                    hr,_,_ = list(map(int,train.iloc[j,14].split(':')))
                    if i[1] >= 1000:
                        day1 = i[1]/1000
                        newday = (int(date) + day1)%7
                        if newday == 0:
                            newday=7
                        c = list(str(train.iloc[j,5]))
                        if newday in c:
                            print("train 01\n\t",train.iloc[i[3],:])
                            print("train 02\n\t",train.iloc[j,:])
                            b.append(train.iloc[i[3],:])
                            w.append(train.iloc[j,:])
                            k.append(b)
                            k.append(w)
                    else:
                        time = i[1]
                        if hr > time:
                            print("train 01\n\t",train.iloc[i[3],:])
                            print("train 02\n\t",train.iloc[j,:])
                            b.append(train.iloc[i[3],:])
                            w.append(train.iloc[j,:])
                            k.append(b)
                            k.append(w)
                        else:
                            newday = (int(date) + 1)%7
                            if newday == 0:
                                newday=7
                            c = list(str(train.iloc[j,5]))
                            if newday in c:
                                print("train 01\n\t",train.iloc[i[3],:])
                                print("train 02\n\t",train.iloc[j,:])
                                b.append(train.iloc[i[3],:])
                                w.append(train.iloc[j,:])
                                k.append(b)
                                k.append(w)

        report4 = pd.DataFrame()
        for m in k:
            r = pd.DataFrame(m)
            report3 = pd.concat([report4,r], axis = 0) 
        for m in range(0,len(report4)):
            p = list(report4.iloc[i,:])
            traincon.append(m)



    return render(request,"home/result.html",{"t":t, "q":q, "f":flightcon, "tr":traincon})