
# I would recommend running these commands one by one but I think they should all work together (I warned you)

# add your info
MONGO_USER="" 
MONGO_PW=""

# SSH into VM (E2 was big enough for me)

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

# setup venv (rename if you use another repo)
cd ~/dnd-characters-dataset-24
python3 -m venv env
source env/bin/activate

# install requirements
pip install -r requirements.txt

# setup secrets (this is still terrible and I should learn to use env variables in my script)
cat << EOF > my_secrets.py
user_name = $MONGO_USER
password = "$MONGO_PW
EOF

# start the script
python main.py

# There is one more confirmation required here. Just press "Y" when prompted.