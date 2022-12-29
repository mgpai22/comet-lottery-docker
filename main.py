from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import glob
import re

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


service_directory = 'history/service/'
lottery_directory = 'history/lottery/'


def file(x):  # Function to load specified file
    with open(x, 'r+') as file:
        return json.load(file)


def get_singleton_dir(directory, singleton: str, pattern: str):
    # Use the glob function to get a list of all files in the directory that have an underscore in the name
    files = glob.glob(os.path.join(directory, '*_*'))

    # Use the os.path.normpath function to normalize the file names
    files = [os.path.normpath(f) for f in files]

    # Use a regular expression to find the number after the underscore in each file name

    # Add all values after '_' to a list
    list_of_singleton_ids = []
    for f in files:
        match = re.search(pattern, f)
        if match:
            matched = match.group(1)
            print(matched)
            list_of_singleton_ids.append(matched)
    try:
        index = list_of_singleton_ids.index(singleton)
        return files[index]
    except ValueError:
        pass

    return -1


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lottery")
async def display_lottery():
    return file('lotteryConf.json')

@app.get("/lottery/{id}")
async def display_lottery_by_id(id: str):
    directory = get_singleton_dir(lottery_directory, id, "lottery_(.*?)\.json")
    if directory == -1:
        dict = {
            'error': 'not found, please try a different id'
        }
        return dict
    return file(directory)


@app.get("/service")
async def display_service():
    service_owner_file = file('serviceOwner.json')
    dict = {
        "cometId": service_owner_file['cometId'],
        "cometTicketPrice": service_owner_file['cometTicketPrice'],
        "winnerChance": service_owner_file['winnerChance'],
        "timeBeforeUnlockMS": service_owner_file['timeBeforeUnlockMS'],
        "distributionAddress": service_owner_file['distributionAddress'],
        "singletonName": service_owner_file['singletonName'],
        "singletonDesc": service_owner_file['singletonDesc'],
        "ticketName": service_owner_file['ticketName'],
        "ticketDesc": service_owner_file['ticketDesc'],
        "oracleNFT": service_owner_file['oracleNFT']
    }
    return dict

@app.get("/service/{id}")
async def display_service_by_id(id: str):
    directory = get_singleton_dir(service_directory, id, "serviceOwner_(.*?)\.json")
    if directory == -1:
        dict = {
            'error': 'not found, please try a different id'
        }
        return dict
    service_owner_file = file(directory)
    dict = {
        "cometId": service_owner_file['cometId'],
        "cometTicketPrice": service_owner_file['cometTicketPrice'],
        "winnerChance": service_owner_file['winnerChance'],
        "timeBeforeUnlockMS": service_owner_file['timeBeforeUnlockMS'],
        "distributionAddress": service_owner_file['distributionAddress'],
        "singletonName": service_owner_file['singletonName'],
        "singletonDesc": service_owner_file['singletonDesc'],
        "ticketName": service_owner_file['ticketName'],
        "ticketDesc": service_owner_file['ticketDesc'],
        "oracleNFT": service_owner_file['oracleNFT']
    }
    return dict

