import os
from bs4 import BeautifulSoup
import requests
import json
from sklearn.cluster import KMeans
import numpy


A = 600.0
B = -10.0
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)





def create_db():
    f = open("problemset.txt", "r")
    text = f.read()
    f.close()
    ProblemsetProblemsResult = json.loads(text)
    Problems = ProblemsetProblemsResult.get("result").get("problems")
    ProblemStatistics = ProblemsetProblemsResult.get(
        "result").get("problemStatistics")

    f = open('users.txt', 'r')
    text = f.read()
    f.close()
    UserResult = json.loads(text)

    AllTags = {}
    ProblemSet = {}
    for Problem in Problems:
        Problem_Id = str(Problem.get('contestId'))+str(Problem.get('index'))
        # 当没有rating的时候不采集
        if Problem.get('rating') == None:
            continue
        # 特殊题目不采集
        if "*special" in str(Problem.get('tags')):
            continue
        ProblemSet[Problem_Id] = Problem
        for tag in Problem.get('tags'):
            if(AllTags.get(tag) == None):
                AllTags[tag] = 1
            else:
                AllTags[tag] = 1+AllTags[tag]
    ResultTag = sorted(AllTags.items(), key=lambda item: item[1], reverse=True)
    
    print(ResultTag)
    f = open('tags.txt','w')
    f.write(json.dumps(ResultTag))
    f.close()
   
    

    for Problem in ProblemStatistics:
        Problem_Id = str(Problem.get('contestId'))+str(Problem.get('index'))
        GetProblem = ProblemSet.get(Problem_Id)
        if (GetProblem == None):
            continue
        else:
            GetProblem['solvedCount'] = int(Problem.get('solvedCount'))
            GetProblem['difficulty'] = A / \
                (GetProblem['solvedCount']+1.0)+GetProblem['rating']
    Tags = ResultTag
    t = 1
    p = 1
    MapTag = {}
    for item in Tags:
        tagname = item[0]
        print(tagname)
        count = item[1]
        MapTag[tagname] = (t,p)
        t = 1-t
        if (t == 1):
            p = p * 2
    point = []
    for ProblemName in ProblemSet:
        now_point = []
        Problem = ProblemSet[ProblemName]
        Problem_Id = str(Problem.get('contestId'))+str(Problem.get('index'))
        tags = Problem.get('tags')
        xx = 0
        yy = 0
        SetOftags = set(tags)

        for tag in tags:
            SetOftags.add(tag)
        for tag in Tags:
            if (tag[0] in SetOftags):
                now_point.append(90000.0/tag[1])
            else :
                now_point.append(0.0)
        #now_point.append(Problem.get('difficulty'))
        Problem['tags2point2d'] =now_point

        point.append(now_point)
        
            
    print(point)
    K = 150
    model = KMeans(n_clusters=K, n_jobs=4, max_iter=300000)
    result = model.fit_predict(point)
    index = 0
    for ProblemName in ProblemSet:
        Problem = ProblemSet[ProblemName]
        Problem['kmeans_result'] = result[index]
        Problem['kmeans_point'] = model.cluster_centers_[result[index]]
        index = index +1
    f = open('ProblemSetMY.txt','w')
    f.write(json.dumps(ProblemSet,cls=MyEncoder))
    f.close()

create_db()