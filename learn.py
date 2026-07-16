'''
put in a gitrepo path to analyze its activity

'''

from git import Repo

# specify the local directory where the repository will be cloned
local_dir = '30-Days-Of-Python'


repo_url = "https://github.com/Asabeneh/30-Days-Of-Python.git"

repo = Repo.clone_from(repo_url, local_dir)

print(repo)