

# Create your views here.
from operator import truediv
import os
from re import X
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.conf import settings
import numpy as np
import pickle
from django.core import serializers
import json
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries
import datetime
from .fazscore import fazscore

# Create your views here.
def signup(request):
    if request.method=='POST':
        form=MemberSignup(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            arr=np.array([])
            str=arr.tostring()
            obj=userProfile.objects.create(id=model_instance,projdata=str,blogdata=str)
            obj.save()
            return redirect('/connect/login')
        else:
            print(form.errors)
            return redirect('/connect/signup')

    form=MemberSignup()
    return render(request,'connect/signup.html',{'forms':form})

def createproject(request):
    if request.method=='POST':
        try:
            try:
                userid=request.session['id']
            except:
                return redirect('/connect/login')
            data=request.POST
            name=data.get('name','no name')
            filed=data.get('name','no field')
            number_of_people=data.get('number_of_people',1)
            projshortdesc=data.get('projshortdesc','')
            starttime=request.POST['starttime_year']+'-'+request.POST['starttime_month']+'-'+request.POST['starttime_day']
            time=data.get('time',30)
            techstack=data.get('techstack','programming')
            filed=addfields(projshortdesc)
            pobj=Project.objects.create(name=name,field=filed,time=time,starttime=starttime,projshortdesc=projshortdesc,number_of_people=number_of_people,techstack=techstack)
            pobj.save()
            mobj=Member.objects.filter(mid=userid)[0]
            pobj.created_by.add(mobj)
            msg='success'
        except:
            msg='failure'
        return render(request,'connect/createproject.html',{'forms':CreateProject,'msg':msg})

    
    form=CreateProject()
    return render(request,'connect/createproject.html',{'forms':form})


def login(request):
    if request.method=='POST':
        data=request.POST
        id=data['id']
        member=Member.objects.filter(mid=id)
        if len(member)==0:
            return redirect('/connect/signup')
        else:
            if data['password']==member[0].password:
                request.session['id']=id
                request.session.set_expiry(30000)
                return redirect('/connect/recd')
            else:
                return redirect('/connect/login')
        return redirect('/connect/login')
    
    else:
        form=Login()
        return render(request,'connect/login.html',{'forms':form})


def myprofile(request):
    try:
        userid=request.session['id']
        mem=Member.objects.filter(mid=userid)
        if len(mem)==0:
            return redirect('/connect/login')
        proj=Project.objects.filter(created_by=mem[0])
        blog=Blog.objects.filter(created_by=mem[0])
        blogs=[]
        projects=[]
        for i in range(len(proj)):
            p=proj[i]
            projects.append(p)
        for i in range(len(blog)):
            b=blog[i]
            blogs.append(b)
        return render(request,'connect/myprofile.html',{'projects':projects,'blogs':blogs})

    except:
        return redirect('/connect/login')


def deleteproject(request):
    pid=request.GET.get('id','')
    Project.objects.filter(pid=pid).delete()
    return redirect('/connect/myprofile')
    
    
def createblog(request):
    if request.method=='POST':
        try:
            try:
                userid=request.session['id']
            except:
                return redirect('/connect/login')
            data=request.POST
            title=data.get('title','no name')
            body=data.get('body','no body')
            field=data.get('field','no field')
            field=addfields(body)
            bobj=Blog.objects.create(title=title,body=body,field=field)
            bobj.save()
            mobj=Member.objects.filter(mid=userid)[0]
            bobj.created_by.add(mobj)
            msg='success'
        except:
            msg='failure'
        return render(request,'connect/createblog.html',{'forms':CreateBlog,'msg':msg})

    form=CreateBlog()
    return render(request,'connect/createblog.html',{'forms':form})


def deleteblog(request):
    bid=request.GET.get('id','')
    Blog.objects.filter(bid=bid).delete()
    return redirect('/connect/myprofile')

def logout(request):
    try:
        del request.session['id']
        return redirect('/connect/login')
    except:
        return redirect('/connect/login')

def addfields(projshortdesc):
   targets=['ML', 'android', 'blockchain', 'cloud', 'webdev'] 
   filename=os.path.join(settings.BASE_DIR,'connect\\mlmodels\\vector.pickel')
   vec=pickle.load(open(filename,'rb'))
   filename=os.path.join(settings.BASE_DIR,'connect\\mlmodels\\tfidf.pickel')
   tfidf=pickle.load(open(filename,'rb'))
   filename=os.path.join(settings.BASE_DIR,'connect\\mlmodels\\nlpmodel.pickel')
   clf=pickle.load(open(filename,'rb'))
   vect=vec.transform([projshortdesc])
   vect=tfidf.transform(vect)
   cl=clf.predict(vect)
   return targets[cl[0]]

def recommend(request):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np 
    from sklearn.metrics.pairwise import cosine_similarity
    transformer=TfidfVectorizer(stop_words='english')
    pall=Project.objects.all()
    ball=Blog.objects.all()
    palllist=[] 
    balllist=[]
    for i in range(len(pall)):
        palllist.append([pall[i].projshortdesc])
    for i in range(len(ball)):
        balllist.append([ball[i].body])
    try:
        userid=request.session['id']
    except:
        return redirect('/connect/login')
    up=userProfile.objects.get(pk=userid)
    projids=np.frombuffer(up.projdata,dtype='int')
    blogids=np.frombuffer(up.blogdata,dtype='int')
    # projids=np.array([6])
    # blogids=np.array([6])
    projects=[]
    blogs=[]
    if len(projids)==0:
        proj=Project.objects.all()
        for i in range(len(proj)):
            if i>=5:
                break
            p=proj[i]
            projects.append(p)
    else:
        proj=Project.objects.all()
        projids=projids.tolist()
        projs=Project.objects.filter(pid__in=projids)
        proj_text=[]
        proj_ids=[]
        for i in range(len(proj)):
            p=proj[i]
            proj_ids.append(p.pid)
            proj_text.append(p.projshortdesc)
        proj_tfidf=transformer.fit_transform(proj_text)
        projs_ids=[]
        projs_text=[]
        for i in range(len(projs)):
            p=projs[i]
            projs_ids.append(p.pid)
            projs_text.append(p.projshortdesc)
        projs_tfidf=transformer.transform(projs_text)
        simidx=np.argsort(cosine_similarity(proj_tfidf,projs_tfidf),axis=0)[::-1]
        resids=[]
        for i in range(len(simidx)):
            resids.append(proj_ids[simidx[i][0]])
        for i in range(len(resids)):
            if resids[i] not in projs_ids:
                resproj=Project.objects.get(pk=resids[i])
                projects.append(resproj)
            

    if len(blogids)==0:
        blog=Blog.objects.all()
        for i in range(len(blog)):
            if i>=5:
                break
            p=blog[i]
            blogs.append(p)
    else:
        blog=Blog.objects.all()
        blogids=blogids.tolist()
        blogss=Blog.objects.filter(bid__in=blogids)
        blog_text=[]
        blog_ids=[]
        for i in range(len(blog)):
            p=blog[i]
            blog_ids.append(p.bid)
            blog_text.append(p.body)
        blog_tfidf=transformer.fit_transform(blog_text)
        blogs_ids=[]
        blogs_text=[]
        for i in range(len(blogss)):
            p=blogss[i]
            blogs_ids.append(p.bid)
            blogs_text.append(p.body)
        blogs_tfidf=transformer.transform(blogs_text)
        simidx=np.argsort(cosine_similarity(blog_tfidf,blogs_tfidf),axis=0)[::-1]
        resids=[]
        for i in range(len(simidx)):
            resids.append(blog_ids[simidx[i][0]])
        for i in range(len(resids)):
           if resids[i] not in blogs_ids:
               b=Blog.objects.get(pk=resids[i])
               blogs.append(b)
    return render(request,'connect/home.html',{'projects':projects,'blogs':blogs})


def handleLikes(request,type,id):
        userid=request.session['id']
        site=request.GET.get('site')
        if type=='proj':
            m=userProfile.objects.get(pk=userid)
            list1=m.projdata
            arr=np.frombuffer(list1,dtype='int')
            x=np.where(arr==id)
            if x[0].size==0: 
                arr=np.append(arr,id)
            else:
                arr=np.delete(arr,np.where(arr==id))
            m.projdata=arr.tostring()
            m.save()
        elif type=='blog':
            m=userProfile.objects.get(pk=userid)
            list1=m.blogdata
            arr=np.frombuffer(list1,dtype='int')
            x=np.where(arr==id)
            if x[0].size==0: 
                arr=np.append(arr,id)
            else:
                arr=np.delete(arr,np.where(arr==id))
            m.blogdata=arr.tostring()
            m.save()
        print(request)
        return redirect('/connect/'+site)
    



def allitems(request,cat):
    try:
        userid=request.session['id']
    except:
        return redirect('/connect/login')
    up=userProfile.objects.get(pk=userid)
    projids=np.frombuffer(up.projdata,dtype='int')
    blogids=np.frombuffer(up.blogdata,dtype='int')
    projects=[]
    blogs=[]
    if cat=='all':
        projs=Project.objects.all()
        for i in range(len(projs)):
            cur=projs[i]
            
            if cur.pk in projids:
                res={}
                res['pid']=cur.pk
                res['name']=cur.name
                res['time']=cur.time
                res['starttime']=cur.starttime
                res['projshortdesc']=cur.projshortdesc
                res['field']=cur.field
                res['number_of_people']=cur.number_of_people
                res['created_by']=cur.created_by.all()
                res['techstack']=cur.techstack
                res['like']=True
                projects.append(res)
            else:
                res={}
                res['pid']=cur.pk
                res['name']=cur.name
                res['time']=cur.time
                res['starttime']=cur.starttime
                res['projshortdesc']=cur.projshortdesc
                res['field']=cur.field
                res['number_of_people']=cur.number_of_people
                res['created_by']=cur.created_by
                res['techstack']=cur.techstack
                res['like']=False
                projects.append(res)
        blogss=Blog.objects.all()
        for i in range(len(blogss)):
            cur=blogss[i]
            if cur.pk in blogids:
                res={}
                res['bid']=cur.bid
                res['title']=cur.title
                res['field']=cur.field
                res['body']=cur.body
                res['created_by']=cur.created_by
                res['like']=True
                blogs.append(res)
            else:
                res={}
                res['bid']=cur.bid
                res['title']=cur.title
                res['field']=cur.field
                res['body']=cur.body
                res['created_by']=cur.created_by
                res['like']=False
                blogs.append(res)
        return render(request,'connect/all.html',{'projects':projects,'blogs':blogs,'type':'explore/all'})

    else:
        projs=Project.objects.filter(field=cat)
        for i in range(len(projs)):
            cur=projs[i]
            if cur.pk in projids:
                res={}
                res['pid']=cur.pk
                res['name']=cur.name
                res['time']=cur.time
                res['starttime']=cur.starttime
                res['projshortdesc']=cur.projshortdesc
                res['field']=cur.field
                res['number_of_people']=cur.number_of_people
                res['created_by']=cur.created_by.all()
                res['like']=True
                projects.append(res)
            else:
                res={}
                res['pid']=cur.pk
                res['name']=cur.name
                res['time']=cur.time
                res['starttime']=cur.starttime
                res['projshortdesc']=cur.projshortdesc
                res['field']=cur.field
                res['number_of_people']=cur.number_of_people
                res['created_by']=cur.created_by
                res['like']=False
                projects.append(res)
        blogss=Blog.objects.filter(field=cat)
        for i in range(len(blogss)):
            cur=blogss[i]
            if cur.pk in blogids:
                res={}
                res['bid']=cur.bid
                res['title']=cur.title
                res['body']=cur.body
                res['created_by']=cur.created_by
                res['like']=True
                blogs.append(res)
            else:
                res={}
                res['bid']=cur.bid
                res['title']=cur.title
                res['body']=cur.body
                res['created_by']=cur.created_by
                res['like']=False
                blogs.append(res)
        return render(request,'connect/all.html',{'projects':projects,'blogs':blogs,'type':'explore/'+cat})

def parsingdate(date):
    j=str(date).split('-')
    j=j[::-1]
    k='-'.join(j)
    return k

def data1():
    #x=[['11-10-1202', 'Grocery', 8886], ['12-10-1202', 'Grocery', 8866], ['14-10-1202', 'Grocery', 8896], ['16-10-1202', 'Grocery', 6866], ['18-10-1202', 'Grocery', 8866]]
    targets=['ML', 'android', 'blockchain', 'cloud', 'webdev'] 
    today=datetime.datetime.now()
    today=str(today).split(' ')[0]
    today=today.split('-')
    enddate=datetime.date(int(today[0]),int(today[1]),int(today[2]))
    delta=datetime.timedelta(days=7)
    delta1=datetime.timedelta(days=1)
    stdate=enddate-4*delta
    res=[]
    while stdate<=enddate:
        print(stdate)
        nextdate=stdate+delta
        for i in targets:
            k=[]
            p=Project.objects.filter(field=i,starttime__range=(stdate,nextdate-delta1))
            k.append(parsingdate(stdate))
            k.append(i)
            k.append(len(p))
            b=Blog.objects.filter(field=i,created_at__range=(stdate,nextdate-delta1))
            k[2]+=len(b)
            res.append(k)
        stdate=nextdate
    return res


def calcscore(data):
    scores=[]
    for i in range(1,len(data)):
        scores.append(fazscore(0.8,data[0:i]).score(data[i]))
    return scores
def data2(res):
    temp=[]
    i=0
    dates=[]
    for i in range(5):
        dates.append(res[i][0])
    ml=[]
    for i in range(5):
        ml.append(res[i][2])
    android=[]
    for i in range(5,10):
        android.append(res[i][2])
    block=[]
    for i in range(10,15):
        block.append(res[i][2])
    cloud=[]
    for i in range(15,20):
        cloud.append(res[i][2])
    webdev=[]
    for i in range(20,25):
        webdev.append(res[i][2])
    mlsc=calcscore(ml)
    androidsc=calcscore(android)
    blocksc=calcscore(block)
    cloudsc=calcscore(cloud)
    webdevsc=calcscore(webdev)
    res=[]
    print(len(mlsc))
    for i in range(len(mlsc)):
        res.append([dates[i+1],"ML",mlsc[i]])
    for i in range(len(androidsc)):
        res.append([dates[i+1],"android",androidsc[i]])
    for i in range(len(webdevsc)):
        res.append([dates[i+1],"webdev",webdevsc[i]])
    for i in range(len(blocksc)):
        res.append([dates[i+1],"blockchain",blocksc[i]])
    for i in range(len(cloudsc)):
        res.append([dates[i+1],"cloud",cloudsc[i]])   
    return res


def chart(request):

   data = data1()
   data3=data.copy()
   data3.sort(key = lambda x: x[1])
   d2=data2(data3)
   print(d2)
   schema = [{
  "name": "Time",
  "type": "date",
  "format": "%d-%m-%Y"
}, {
  "name": "Type",
  "type": "string"
}, {
  "name": "No.of items",
  "type": "number"
}]
   fusionTable = FusionTable(schema, data)
   timeSeries = TimeSeries(fusionTable)

   timeSeries.AddAttribute('chart', '{}')
   timeSeries.AddAttribute('series', '"Type"')
   timeSeries.AddAttribute('yaxis', '[{"title":"No.of items"}]')

   fusionTable1 = FusionTable(schema, d2)
   timeSeries1 = TimeSeries(fusionTable1)

   timeSeries1.AddAttribute('chart', '{}')
   timeSeries1.AddAttribute('series', '"Type"')
   timeSeries1.AddAttribute('yaxis', '[{"title":"Rate"}]')


   # Create an object for the chart using the FusionCharts class constructor
   fcChart = FusionCharts("timeseries", "ex2", 700, 450, "chart-1", "json", timeSeries)
   fcChart2= FusionCharts("timeseries","ex1",700,450,"chart-2","json",timeSeries1)  
   # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
   return  render(request,'trends.html',{'output' : fcChart.render(),'output1':fcChart2.render()})

def updateproject(request,id):
    if request.method=='POST':
        try:
            try:
                userid=request.session['id']
            except:
                return redirect('/connect/login')
            data=request.POST
            name=data.get('name','no name')
            filed=data.get('name','no field')
            number_of_people=data.get('number_of_people',1)
            projshortdesc=data.get('projshortdesc','')
            starttime=request.POST['starttime_year']+'-'+request.POST['starttime_month']+'-'+request.POST['starttime_day']
            time=data.get('time',30)
            techstack=data.get('techstack','programming')
            filed=addfields(projshortdesc)
            pobj=Project.objects.get(pk=id)
            pobj.name=name
            pobj.number_of_people=number_of_people
            pobj.projshortdesc=projshortdesc
            pobj.starttime=starttime
            pobj.time=time
            pobj.field=filed
            pobj.techstack=techstack
            pobj.save()
            msg='success'
        except:
            msg='failure'
        pobj=Project.objects.get(pk=id)
        forms=CreateProject(initial={'name':pobj.name,'field':pobj.field,'number_of_people':pobj.number_of_people,'projshortdesc':pobj.projshortdesc,'starttime':pobj.starttime,'time':pobj.time,'techstack':pobj.techstack})
        return render(request,'connect/updateproject.html',{'forms':forms,'msg':msg})

    
    pobj=Project.objects.get(pk=id)
    form=CreateProject(initial={'name':pobj.name,'field':pobj.field,'number_of_people':pobj.number_of_people,'projshortdesc':pobj.projshortdesc,'starttime':pobj.starttime,'time':pobj.time,'techstack':pobj.techstack})
    return render(request,'connect/updateproject.html',{'forms':form})

def updateblog(request,id):
    if request.method=='POST':
        try:
            try:
                userid=request.session['id']
            except:
                return redirect('/connect/login')
            data=request.POST
            title=data.get('title','no name')
            body=data.get('body','no body')
            field=data.get('field','no field')
            field=addfields(body)
            bobj=Blog.objects.get(pk=id)
            bobj.title=title
            bobj.body=body
            bobj.field=field
            bobj.save()
            msg='success'
        except:
            msg='failure'
        bobj=Blog.objects.get(pk=id)
        form=CreateBlog(initial={'title':bobj.title,'body':bobj.body})
        return render(request,'connect/updateblog.html',{'forms':form,'msg':msg})

    bobj=Blog.objects.get(pk=id)
    form=CreateBlog(initial={'title':bobj.title,'body':bobj.body})
    return render(request,'connect/updateblog.html',{'forms':form})
