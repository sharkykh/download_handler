# download_handler

Send a post-process request to Medusa / SickRage directly from your download client.

## Installation
Clone this repository in a convenient location using git:
```shell
git clone https://github.com/sharkykh/download_handler.git
```
### OR
Download and extract the [zip file](https://github.com/sharkykh/download_handler/archive/master.zip)/[tar.gz file](https://github.com/sharkykh/download_handler/archive/master.tar.gz) to a convenient location.

### Usage:

```shell
$ download_handler.py -h
usage: download_handler.py [-h] --label LABEL path

positional arguments:
  path           full path to downloaded folder

optional arguments:
  -h, --help     show this help message and exit
  --label LABEL  torrent label
```

### In your download client, find the "Run external program" setting and set the file path with the currect arguments.
#### uTorrent:
```shell
"C:\path\to\download_handler.pyw" "%D" --label "%L"
```

#### qBittorrent:
```shell
"C:\Python27\python.exe" "C:\path\to\download_handler.pyw" "%R" --label "%L"
```
