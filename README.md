# TXPsybot - Web chatbot with llmmemory

## Requirments:
```shell
Anaconda3: https://www.anaconda.com/download/
```
## Create a python virtual enviroment with anaconda
```shell
user@xyz:~/git-repos$ conda create -n yourenvname python=3.10 anaconda
```
## Activate the enviroment
```shell
user@xyz:~/git-repos$ conda activate yourenvname
```
## Clone the repository and navigate inside
```shell
(yourenvname) user@xyz:~/git-repos$ https://github.com/sappyb/llmmemory.git
(yourenvname) user@xyz:~/git-repos$ cd ./llmmemory
(yourenvname) user@xyz:~/git-repos/llmmemory$ 
```
## Run setup
```shell
pip install -r requirements.txt -e .
```

in windows
```shell
pip install -r requirements.txt
```

## Run
```shell
streamlit run app.py
```

## Description

1. Solves congitive states of students
2. Knowledge stored in vector databases
3. Added Memory to conversation
