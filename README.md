# D&D Characters Dataset

After creating my [first Version of a dataset with 1.2 Million Characters](https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test) pulled from dndbeyond, I now want to try again but get more characters and more detailled info about them. My general method will be the same as before (using the dndbeyond backend API to scrape characters) but I want to save them in a database this time. Last time I simply created csv files which were prone to crashing and getting corrupted when my code / hardware would fail. Now I would like to set this up in way where I can run my script in a VM on GCP and have it save each character (or batch of them) every few seconds. This requires both additional setup and analysis to find a good way to represent the data.


## Roadmap
- [x] Get sample character reponse from API to analyze
- [ ] Create goal for what data to extract and how to save it
- [ ] Write python script to get all data
- [ ] Set up GCP environment with VM to run script
- [ ] Publish dataset on Kaggle
- [ ] Analyze dataset

### Get sample character reponse from API to analyze
This step was easy as I pretty much just redid what I had done before. By checking the network tab while loading a dndbeyond character, one can see the backend API calls being made to this endpoint: ```https://character-service.dndbeyond.com/character/v5/character/{YOUR_CHARACTER_ID}?includeCustomItems=true```

This returns a json file like [sample_reponse.json](sample_reponse.json) which contains all info about the character in about 10.000 - 15.000 lines. This is way to much for me. I am looking to reduce the data I actually save to about what I have noted down in [target.json](target.json). So time to come up with a way to save this!

### Create goal for what data to extract and how to save it