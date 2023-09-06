# socat-manager

`socat-manager` listens on an Unix socket and spawns `socat` processes according to the received arguments.

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
