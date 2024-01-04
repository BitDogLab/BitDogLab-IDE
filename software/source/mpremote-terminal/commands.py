import os, sys
import serial
import serial.tools.list_ports

def do_connect(state, *args):
    print(args)
    dev = args[0] if args is not None else "auto"
    print(dev)
    match dev:
        case "list":
            ports = sorted(serial.tools.list_ports.comports())
            if len(ports) == 0:
                state.appendToBuf('no device found')
                return
            for p in ports:
                state.appendToBuf(
                    "{} {} {:04x} {:04x} {} {}".format(
                        p.device,
                        p.serial_number,
                        p.vid if isinstance(p.vid, int) else 0,
                        p.pid if isinstance(p.pid, int) else 0,
                        p.manufacturer,
                        p.product
                    )
                )
        case "auto":
            for p in sorted(serial.tools.list_ports.comports()):
                if p.vid is not None and p.pid is not None:
                    state.appendToBuf(f"Connected to {p.device}")
                    state.connect(p.device, 115200)
                    assert(state.serial is not None)
                    return
            raise Exception("no device found")
        # more cases to be added


def do_disconnect(state, *args):
    if state.serial is None:
        return
    state.serial.close()
    state.serial = None

def do_eval(state, *args):
    buf = f"print({' '.join(args)})\r\n"
    print(buf)
    if state.connected:
        state.serial.write(
            buf.encode()
        )
    else:
        state.appendToBuf(f"not connected")

def do_exec(state, *args):
    buf = f"{' '.join(args)}\r\n"
    print(buf)
    if state.connected:
        state.serial.write(
            buf.encode()
        )
    else:
        state.appendToBuf(f"not connected")