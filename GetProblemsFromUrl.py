import requests
import json
ProblemsUrl = "http://codeforces.com/api/problemset.problems"

ProblemsetProblems = requests.get(ProblemsUrl,headers={})

f = open('problemset.txt','w')
f.write(ProblemsetProblems.text)
f.close()
UsersUrl = 'http://codeforces.com/api/user.ratedList?activeOnly=true'

Users = requests.get(UsersUrl,headers = {})
# test 
f = open('users.txt','w')
f.write(Users.text)
f.close()