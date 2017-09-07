# Pairmhai Backend
**Work In Progress (WIP)**

# Install Guide

## option 1 (using pip)
1. install requirement library by `[pip|pip3] install -r requirements.txt`
2. run server by `[python|python3] manage.py runserver`
3. the server will run on **http://localhost:8000**

## option 2 (using [conda](https://conda.io/docs/))
1. install requirement library by `conda create --name pairmhai -c conda-forge --file requirement_conda.txt` (first time ONLY)
2. activate by `source activate pairmhai`
3. (optional) validate by run `conda info --envs` the star (`*`) should be on pairmhai name like this...
```
# conda environments:
#
pairmhai              *  /Users/kamontat/anaconda3/envs/pairmhai
root                     /Users/kamontat/anaconda3
```
2. run server by `[python|python3] manage.py runserver`
3. the server will run on **http://localhost:8000**

# Documentation
1. [Document link](doc/README.md)

# Contribution
1. [format](doc/contribution/README.md)
2. [how to](doc/contribution/Howto.md)
