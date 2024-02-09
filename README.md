# D&D Characters Dataset

After creating my [first Version of a dataset with 1.2 Million Characters](https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test) pulled from dndbeyond, I now want to try again but get more characters and more detailled info about them. My general method will be the same as before (using the dndbeyond backend API to scrape characters) but I want to save them in a database this time. Last time I simply created csv files which were prone to crashing and getting corrupted when my code / hardware would fail. Now I would like to set this up in way where I can run my script in a VM on GCP and have it save each character (or batch of them) every few seconds. This requires both additional setup and analysis to find a good way to represent the data.

> [!NOTE]
> I was a bit worried about how WotC would react to this so I sent them an E-Mail and they said: 
>>"We are responding to let you know that upon review of the description of your project, it looks like your request is covered by our Wizards of the Coast Fan Content Policy, which you can find [here](https://company.wizards.com/en/legal/fancontentpolicy)."

## Roadmap
- [x] Get sample character reponse from API to analyze
- [x] Create goal for what data to extract and how to save it
- [X] Write python script to get all data
- [X] Set up GCP environment with VM to run script
- [ ] Actually get the data
- [ ] Analyze dataset
- [ ] Publish dataset on Kaggle

### Get sample character reponse from API to analyze
This step was easy as I pretty much just redid what I had done before. By checking the network tab while loading a dndbeyond character, one can see the backend API calls being made to this endpoint: ```https://character-service.dndbeyond.com/character/v5/character/{YOUR_CHARACTER_ID}?includeCustomItems=true```

This returns a json file like [sample_reponse.json](sample_reponse.json) which contains all info about the character in about 10.000 - 15.000 lines. This is way to much for me. I am looking to reduce the data I actually save to about what I have noted down in [target.json](target.json). So time to come up with a way to save this!

### Create goal for what data to extract and how to save it
Turns out I'm not the only one that likes JSON, so I looked into MongoDB. Basically it allows me to save the characters as json without having to flatten (hopefully this will not be annoying when it gets to the analysis part). So I set up a free account and created my first collection. It was surpirsingly easy to get it working and start sending json from my script. 

### Write python script to get all data
The script is split into different files. The file [async_get.py](async_get.py) contains a function that uses ```asyncio``` and ```aiohttp``` to get a character url and returns the reponse json. I pretty much straight copied from [here](https://stackoverflow.com/questions/53021448/multiple-async-requests-simultaneously) and changed some variable names. This way I can fetch like 10.000 characters at the same time and don't have to wait for them to all come in one by one.

The file [parse_character.py](parse_character.py) has the function that parses the character. This could really have been a class (ik you told me Carsten) but oh well, it's just a long function that picks out everything I want to save and returns a dict with the parsed info.

The [main.py](main.py) starts the process. There one can set the amount of characters to fetch. It also handles the database connection and saving.

### Set up GCP environment with VM to run script
According to [this article on dndbeyond](https://www.dndbeyond.com/posts/1648-2023-unrolled-a-look-back-at-a-year-of-adventure?page=5) there were 180 million characters / NPCs played last year with 6 million being added. Now, I don't quite believe the 180 million be relevant for me here (famous last words?) but I expect that the number of characters is like 30 - 50 million.

My first few tests tell me that it takes about 30 seconds to get 10.000 characters on my local machine. This would equal about 40 hours or so of running perfectly smooth to get 50 million characters. Doesn't sound impossible but I would really like to try and get this whole thing to run on a GCP cluster or maybe as a batch job in Cloud Run. 

So I set up a GCP VM (E2 with basic settings and allow HTTPs) hosted in the US because I assume that the dndbeyond servers are there as well. I wrote down all steps after the creation of the VM in [deployme.sh](deployme.sh) so anyone can follow. Basically it installs all required tools, clones this repo and then runs the script. Now it is just a question of time until I have all the data.

## Actually get the data
This was not as easy as I had hoped. I initially used a MongoDB Atlas serverless instance. This a big mistake. The way the script is written, it sent 40 Million writes to the DB which cost me about 120$ over he span of a few hours while I was sleeping. So I stopped my script and looked for an alternative.

What I landed on was to simply host a mongoDB instance on another VM in the same GCP Zone. This doesn't incur any addidional costs since I still have my free credits from google cloud. It did require some setup but was very managable. I used a 250GB SSD for this instance as the 40 million characters I had collected in my first attempt already took up about 50GB of space.

The writes were becoming very slow after a a few hours of letting my script run and after some searching I found that creating an index by running `db.characters.createIndex({ char_id: 1 })` solved this issue. If I understand correctly, it was caused by the DB searching for the Character ID every time I inserted a new character, which meant searching though millions of documents for each of 10.000 Characters per batch - obviously a slow process.

