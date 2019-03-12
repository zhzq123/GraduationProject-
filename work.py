from flask import Flask, url_for, redirect, render_template, request, flash
import math
import kmeans
from sklearn.cluster import KMeans
from queue import PriorityQueue as PQueue
import matplotlib.pyplot as plt
import numpy
import time
import json
import random
import requests
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

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


def get_commend(handle):
    """
    得到该用户前600发提交
    """
    print('start')
    if (cache.get(handle) != None):
        return json.loads(cache.get(handle))
    HandleUrl = "http://codeforces.com/api/user.status?handle=%s&from=1&count=600" % (
        handle)
    text = requests.get(HandleUrl, headers={}).text
    if (text == None):
        return {"status": "error"}
    print('ok')
    SubmissionSet = json.loads(text).get('result')
    if (SubmissionSet == None):
        return {"status": "error"}
    AcProblemSetUp20 = set()
    AllACProblem = set()
    AllSubmission = {}
    f = open('ProblemSetMY.txt', 'r')
    text = f.read()
    f.close()
    ProblemSet = json.loads(text)
    MaxRatingAcProblem = PQueue(maxsize=20)
    for Submission in SubmissionSet:
        ProblemId = str(Submission.get('problem').get('contestId')) + \
            str(Submission.get('problem').get('index'))
        if (ProblemSet.get(ProblemId) == None):
            continue
        if (Submission.get('verdict') == 'OK'):
            AllACProblem.add(ProblemId)
            if (MaxRatingAcProblem.full()):
                MaxRatingAcProblem.get()
            MaxRatingAcProblem.put(ProblemSet.get(ProblemId).get('difficulty'))
        if (Submission.get('verdict') == 'OK' and len(AcProblemSetUp20) < 20):
            AcProblemSetUp20.add(ProblemId)

        if (AllSubmission.get(ProblemId) == None):
            AllSubmission[(ProblemId)] = 1
        else:
            AllSubmission[ProblemId] = AllSubmission[ProblemId]+1
    print('ok')
    if (len(AcProblemSetUp20) == 0):
        return {"status": "error"}
    else:
        Result = {}
        max_rating = 0.0
        max_sub = 0
        max_label = -1
        real_rating = 0.0
        tot = MaxRatingAcProblem.qsize()
        while not MaxRatingAcProblem.empty():
            real_rating = real_rating+MaxRatingAcProblem.get()
        real_rating = real_rating / (1.0*tot)
        SetOfLabels = set()
        for problemid in AcProblemSetUp20:
            Result[problemid] = AllSubmission[problemid]
            max_rating = max(max_rating, ProblemSet.get(
                problemid).get('difficulty'))
            SetOfLabels.add(ProblemSet.get(problemid).get('kmeans_result'))
            if (AllSubmission[problemid] > max_sub):
                max_sub = AllSubmission[problemid]
                max_label = ProblemSet.get(problemid).get('kmeans_result')
        commend_problem_highest_error_rate_set = []
        commend_problem_untouch_set = []
        if max_sub > 3:
            for problemname in ProblemSet:
                problem = ProblemSet[problemname]
                if (problemname in AllACProblem):
                    continue
                if (random.randint(0, 20) >= 10):
                    continue
                if (problem.get('kmeans_result') == max_label and math.fabs(real_rating-problem.get('difficulty')) < 300.0):
                    commend_problem_highest_error_rate_set.append(problem)
                    if len(commend_problem_highest_error_rate_set) >= 5:
                        break
        for problemname in ProblemSet:
            problem = ProblemSet[problemname]
            if (problemname in AllACProblem):
                continue
            if (problem.get('kmeans_result') not in SetOfLabels and math.fabs(real_rating-problem.get('difficulty')) < 300.0
                    and problem.get('difficulty') > real_rating):
                if (problem.get('difficulty') < real_rating and random.randint(0, 20) >= 10):
                    continue
                if (random.randint(0, 20) >= 10):
                    continue
                commend_problem_untouch_set.append(problem)
                if len(commend_problem_untouch_set) >= 5:
                    break
        cache.set(handle, json.dumps({"status": "ok", "result": Result,
                                      "real_rating": real_rating,
                                      "commend_problem_highest_error_rate_set": commend_problem_highest_error_rate_set,
                                      "commend_problem_untouch_set": commend_problem_untouch_set}, cls=MyEncoder))
        return {"status": "ok", "result": Result,
                "real_rating": real_rating,
                "commend_problem_highest_error_rate_set": commend_problem_highest_error_rate_set,
                "commend_problem_untouch_set": commend_problem_untouch_set}
# create_db()


# print(get_commend('tourist'))


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.route('/')
def hello_world():
    return render_template('a.html')


@app.route('/get/', methods=['POST'])
def get():
    handle = request.form.get('handle')
    result = get_commend(handle)
    if (result.get('status') != 'ok'):
        flash('没有这个用户')
        return render_template('a.html')
    ACProblem = result.get('result')
    real_rating = result.get('real_rating')
    commend_problem_highest_error_rate_set = result.get(
        'commend_problem_highest_error_rate_set')
    commend_problem_untouch_set = result.get('commend_problem_untouch_set')

    return render_template('result.html', handle=handle, real_rating=real_rating,
                           commend_problem_highest_error_rate_set=commend_problem_highest_error_rate_set,
                           commend_problem_untouch_set=commend_problem_untouch_set)


if __name__ == '__main__':
    app.run(debug=True)
