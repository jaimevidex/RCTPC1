# Remote File Store over UDP + TCP

A small client/server pair that exposes a remote file API: the control channel runs over **UDP**, while the actual bytes move over **TCP** connections opened on demand.


## Design

The two protocols split the job:

- **UDP — control plane.** The client sends short text commands (*open*, *close*, *put*, *get*). Stateless, low latency, no connection to maintain while idle.
- **TCP — data plane.** A file transfer only exists while it is happening; the connection is opened, the bytes stream, the connection closes.

`open <port>` is the interesting part. The client binds a TCP socket on the given five-digit port and announces it to the server, so **either side can initiate** the transfer:

- `put <local> <remote>` — the client connects to the server's TCP port and uploads.
- `get <remote> <local>` — the server connects back to the client's listening port and downloads.

`close` tears the session down and resets the negotiated port.

## Run

Start the server, then the client:

```bash
# terminal 1
python3 server.py 9000

# terminal 2
python3 client.py localhost 9000
```

Then at the client prompt:

```
open 9500
put report.pdf report.pdf
get notes.txt notes_copy.txt
close
```

## Files

| File | Responsibility |
|---|---|
| `server.py` | UDP command loop, TCP listener, file store |
| `client.py` | Interactive shell, UDP commands, TCP transfers |
| `get_test.txt`, `put_test.txt` | Sample payloads |

## Notes

- Uses only the Python standard library (`socket`, `sys`, `os`).
- Fixed 1024-byte read buffer.
- Educational code: no authentication, no encryption, no path sanitisation — do not expose it to a network you do not control.
