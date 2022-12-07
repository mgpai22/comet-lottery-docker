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


def get_max_file(directory):
    # Use the glob function to get a list of all files in the directory that have an underscore in the name
    files = glob.glob(os.path.join(directory, '*_*'))

    # Use the os.path.normpath function to normalize the file names
    files = [os.path.normpath(f) for f in files]

    # Use a regular expression to find the number after the underscore in each file name
    pattern = re.compile(r'_(\d+)')

    # Find the maximum number in the file names
    max_num = max([int(pattern.search(f).group(1)) for f in files])

    # Find the file name with the maximum number
    max_file = [f for f in files if pattern.search(f).group(1) == str(max_num)][0]

    return max_file


def search_file_by_proxy_address(directory, value):
    files = glob.glob(os.path.join(directory, '*.json'))
    files = [os.path.normpath(f) for f in files]
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
        if data['Lottery']['proxyContract']['contract'] == value:
            return file


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lottery")
async def display_lottery():
    return file('lotteryConf.json')


@app.get("/service")
async def display_service():
    service_owner_file = file('serviceOwner.json')
    dict = {
        "cometId": service_owner_file['cometId'],
        "cometTicketPrice": service_owner_file['cometTicketPrice'],
        "timeBeforeUnlockMS": service_owner_file['timeBeforeUnlockMS'],
        "distributionAddress": service_owner_file['distributionAddress'],
        "singletonName": service_owner_file['singletonName'],
        "singletonDesc": service_owner_file['singletonDesc'],
        "ticketName": service_owner_file['ticketName'],
        "ticketDesc": service_owner_file['ticketDesc'],
        "oracleNFT": service_owner_file['oracleNFT']
    }
    return dict


@app.get("/latest_lottery_history")
async def display_latest_lottery_history():
    return file(get_max_file(lottery_directory))

@app.get("/latest_service_history")
async def display_latest_service_history():
    service_owner_file = file(get_max_file(lottery_directory))
    dict = {
        "cometId": service_owner_file['cometId'],
        "cometTicketPrice": service_owner_file['cometTicketPrice'],
        "timeBeforeUnlockMS": service_owner_file['timeBeforeUnlockMS'],
        "distributionAddress": service_owner_file['distributionAddress'],
        "singletonName": service_owner_file['singletonName'],
        "singletonDesc": service_owner_file['singletonDesc'],
        "ticketName": service_owner_file['ticketName'],
        "ticketDesc": service_owner_file['ticketDesc'],
        "oracleNFT": service_owner_file['oracleNFT']
    }
    return dict


@app.get("/lottery_by_proxy_address/{address}")
async def lottery_by_proxy_address(address: str):
    lottery_file = search_file_by_proxy_address(lottery_directory, address)
    return file(lottery_file)
