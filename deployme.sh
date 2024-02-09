

INSTANCE_NAME="scraper-instance"
GCP_ZONE="us-west4-b"


# deploy GCP VM

gcloud compute instances create $INSTANCE_NAME --zone=$GCP_ZONE --machine-type=e2-medium --tags=https-server


# SSH into VM (E2 was big enough for me)

gcloud compute ssh --zone $GCP_ZONE $INSTANCE_NAME
# go though process of creating ssh keys (enter 3 times)

cd ~

# install stuff we need
sudo apt update

# python and pip
echo "Y" | sudo apt install python3 python3-dev python3-venv
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

# tmux for close ssh session without script ending
sudo apt install tmux

# git to be able to clone
echo "Y" | sudo apt-get install git

# get repo
git clone https://github.com/MaximeBonnin/dnd-characters-dataset-24.git

# tmux is needed to be able to close the ssh connection without the script stopping
# ctrl + b -> d to detach from tmux session later
tmux 

# setup venv (rename if you use another repo)
cd ~/dnd-characters-dataset-24
python3 -m venv env
source env/bin/activate

# install requirements
pip install -r requirements.txt

# setup secrets (this is still terrible and I should learn to use env variables in my script)
# add your info
MONGO_USER="" 
MONGO_PW=""
HOST=""

cat << EOF > my_secrets.py
user_name = "$MONGO_USER"
password = "$MONGO_PW"
host = "$HOST"
EOF

# start the script
python main.py

# There is one more confirmation required here. Just press "Y" when prompted.

# ctrl + b -> d to detach from tmux session
# tmux attach to connect again