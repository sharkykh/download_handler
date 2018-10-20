# download_handler

Send a post-process request to Medusa / SickChill / SickRage directly from your download client.

## Requirements
1. Python (tested with version `2.7`, should work with newer versions as well)
2. [`requests`](https://pypi.org/project/requests/) Python package

## Installation
Clone this repository to a convenient location using `git`:
```shell
git clone https://github.com/sharkykh/download_handler.git
```
#### OR
Download and extract the [zip file](https://github.com/sharkykh/download_handler/archive/master.zip)/[tar.gz file](https://github.com/sharkykh/download_handler/archive/master.tar.gz) to a convenient location.

## Instructions
**First:** Update [the configuration values in the script](https://github.com/sharkykh/download_handler/blob/master/download_handler.py#L40-L72).  
**Then:** In your download client, find the "Run external program" setting and set the file path with the currect arguments.  

#### uTorrent:
```shell
"C:\path\to\download_handler.pyw" "%D" --label "%L"
```

#### qBittorrent:
```shell
"C:\Python27\python.exe" "C:\path\to\download_handler.pyw" "%R" --label "%L"
```

## Usage
```shell
$ download_handler.py -h
usage: download_handler.py [-h] --label LABEL path

positional arguments:
  path           full path to downloaded folder

optional arguments:
  -h, --help     show this help message and exit
  --label LABEL  torrent label
```

