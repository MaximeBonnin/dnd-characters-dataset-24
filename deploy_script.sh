
MY_PROJECT=""

cd ~

sudo apt update
echo "Y" | sudo apt install python3 python3-dev python3-venv
echo "Y" | sudo apt-get install git

sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

git clone https://github.com/MaximeBonnin/dnd-characters-dataset-24.git

# setup venv
cd ~/dnd-characters-dataset-24
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

cat << EOF > my_secrets.py
user_name = "PythonScript"
password = "jhwebrgfuansiasm31234"
EOF