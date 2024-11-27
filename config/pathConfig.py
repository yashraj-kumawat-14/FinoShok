import os

#creating initial configurations relavent to paths of files and folders
CUSTOMERPHOTOPATH = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/customerPhotos"
GUARRANTERPHOTOPATH = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/guarranterPhotos"
DEFAULTIMAGEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/defaultImages"
MODELPATH = f"{os.path.dirname(os.path.abspath(__file__))}/../model"
PROJECTPATH = f"{os.path.dirname(os.path.abspath(__file__))}/.."

ALLPATHS = [CUSTOMERPHOTOPATH, GUARRANTERPHOTOPATH, DEFAULTIMAGEPATH, MODELPATH, PROJECTPATH]