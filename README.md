# Pairmhai Backend [![CircleCI](https://img.shields.io/circleci/project/github/PairMhai/Backend/dev.svg?style=flat-square)](https://circleci.com/gh/PairMhai/Backend)
**Work In Progress (WIP)**

# Install Guide
1. anaconda is required to set envrionment [link](https://www.anaconda.com/download/)
    - the command line interface (cli) is enough.

## To install
1. create require envrionment by `conda create --name pairmhai --file requirement_conda.txt` (first time **ONLY**)
2. activate envrionment by `source activate pairmhai`
3. (optional) validate by run `conda info --envs` the star (`*`) should be on pairmhai name like this...
```
# conda environments:
#
pairmhai              *  ~/anaconda3/envs/pairmhai
root                     ~/anaconda3
```
4. install more needed library by `pip install -r requirements.txt`
5. load database testing data by run `./utils.sh load <database-type>`
    - support type
        - user
        - class
6. run server by `python manage.py runserver`
7. the server will run on **http://localhost:8000**

# Documentation
1. [Document link](doc/README.md)
2. [utils.sh](doc/utils.md)

# Contribution
[Need to know](doc/contributions/README.md)
