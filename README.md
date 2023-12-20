# socat-manager

`socat-manager` listens on an Unix socket and spawns `socat` processes according to the received arguments.

## Dependencies

Please install `socat` before running the server.

```sh
sudo pkg update
sudo pkg install socat
```

## Usage

### Server

```sh
python server.py
```

### Client

```sh
python client.py ADD /dev/nmdm21B 10014
```

```
python client.py DEL /dev/nmdm21B 10014
```
