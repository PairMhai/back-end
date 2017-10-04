# Pairmhai Backend [![CircleCI](https://img.shields.io/circleci/project/github/PairMhai/Backend/dev.svg?style=flat-square)](https://circleci.com/gh/PairMhai/Backend)
**Work In Progress (WIP)**

# Install Guide
1. anaconda is required to set envrionment [link](https://www.anaconda.com/download/)
    - the command line interface (cli) is enough.

## To install
1. create require envrionment by `conda create --name pairmhai --file requirements_conda.txt` (first time **ONLY**)
2. activate environment by `source activate pairmhai`
3. (optional) validate by run `conda info --envs` the star (`*`) should be on pairmhai name like this...
```
# conda environments:
#
pairmhai              *  ~/anaconda3/envs/pairmhai
root                     ~/anaconda3
```
4. install more needed library by `pip install -r requirements.txt`
5. setup database:
    1. `./utils.sh m` - to migrate database
    2. `./utils.sh l` - to load fixture data
    3. `./utils.sh t` - to test
6. run server by `./utils.sh s` or `python manage.py runserver`
7. the server will run on **http://localhost:8000**

## To deploy
1. setup [buildpack](https://github.com/weibeld/heroku-buildpack-run): `heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-run.git`
2. add heroku remote: `git remote add heroku https://git.heroku.com/guarded-brook-49660.git`
3. run push command: `git push heroku <local-branch>:master`

# Documentation
1. [Document link](doc/README.md)
2. [utils.sh](doc/utils.md)

# To do list
- Implement validation of models  [link](https://docs.djangoproject.com/en/dev/ref/validators/#regexvalidator)
- Gettext to enable translation [link](https://docs.python.org/3/library/gettext.html)

# Contribution
[Need to know](doc/contributions/README.md)
