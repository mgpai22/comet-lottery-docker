
# Comet Lottery Docker Deployment

Docker setup for easy running of comet lottery

For more information and to view source code please checkout the [main repo](https://github.com/mgpai22/comet-lottery)




## Master Node Runner
- This section is only for those who want to start their own lottery

  1. `git clone https://github.com/mgpai22/comet-lottery-docker.git` or download zip and extract
  
  2. change into directory 

  3. Go into each **_latest folder and edit the serviceOwner.json file
    - edit the mnemonic, it must have at least have one comet per new lottery so its reccommended to have a reasonable amount of tokens
    - edit the mnemonic pw (NOT WALLET PW), if there is no mnemonic, skip this step
    - edit the id of the comet token (does not have to be comet can be any token id just be mindful of the decimals of that token)
    - edit the price per ticket in comet (if you are using a different token like Neta, it has 6 decimal places so if you mean 100 Neta input 100000000)
    - edit winner chance, when a random person is selected, this is the chance in percent they have of winning
    - edit time before unlock which means how long in milliseconds until lottery ends and winner is selected. If winner does not get the chance and becomes a loser, the lottery moves to a new version (contracts stay same) and this new version again selects a winner after timeBeforeUnlockMS
    - edit the distribution address, this is where 10% of winning funds go to
    - edit the singleton name, this is what the token that identifies a new lottery is named
    - edit the description of the singleton 
    - edit the ticket name, this will be the name of each ticket someone buys. Version and count are added automatically
    - edit the ticket description
    - edit the oracle NFT and add a token id, with the help of an oracle singleton a random number is generated based on the token's box id
    - edit the nodeUrl (must be in the form of http://[ip or domain (port might not be need if a domain is there)]:PORT)
    - edit the apiUrl
    - [for additional configuration information click here](https://github.com/mgpai22/comet-lottery#serviceownerjson)
  4. Run `docker-compose up -d`

  ### Additonal Information

  - to check status or see logs run `docker-compose logs -f`
  - to stop everything run `docker-compose down`
  - if some modification is made to files manually make sure you stop and rerun with `docker-compose up -d --build`
  - 10k api is accessible via http://[your machine ip]:8088/docs
  - 100k api is accessible via http://[your machine ip]:8087/docs
  - 250k api is accessible via http://[your machine ip]:8086/docs
  - to reset a lottery set `timeStamp` inside `lotteryConf.json` to `"null"` this will **overwrite** your contracts with **new** contracts
  - once you stop your master node, there is no guarantee that the lottery will stop since other people may be running follower nodes. They will only copy your new contracts if their lottery ends or if the runner mannually sets timeStamp to `"null"`


## Follower Node Runner
- This section is for those who want to support decentralization by preventing a lottery from being suspended by running a follower node
  
  1. `git clone https://github.com/mgpai22/comet-lottery-docker.git` or download zip and extract
  
  2. change into directory 

  3. Go into each **_latest folder and edit the serviceOwner.json file
    - edit the mnemonic, if you process a transaction you will be rewarded with a bit of ERG or comet to the respective address
    - edit the mnemonic pw (NOT WALLET PW), if there is no mnemonic, skip this step
    - edit the nodeUrl (must be in the form of http://[ip or domain (port might not be need if a domain is there)]:PORT)
    - edit the apiUrl
    - note that followers **do not** need to fill in anything else, however for additional information go [here](https://github.com/mgpai22/comet-lottery#serviceownerjson)
  4. Run `docker-compose -f follower.yml up -d`


### Additional Information

- This can be run on any local (personal) machine since no api or ports need to be exposed to the internet
- to check status or see logs run `docker-compose -f follower.yml logs -f`
- stop the node with `docker-compose -f follower.yml down`
- if some modification is made to files manually make sure you stop and rerun with `docker-compose -f follower.yml up -d --build`
- if master node has abandoned lottery and you want to resync to their new one, set `timeStamp` inside `lotteryConf.json` to `"null"` this will **overwrite** your contracts with **new** contracts (remember, this needs to be done inside of each **_latest folder that you want to reset)
- api has not been made available in the follower.yml file, however, it should be easy to add if you follow the pattern in `docker-compose.yml`
