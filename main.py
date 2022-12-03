from fastapi import FastAPI
import json

app = FastAPI()


def file(x):  # Function to load specified file
    with open(x, 'r+') as file:
        return json.load(file)


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
