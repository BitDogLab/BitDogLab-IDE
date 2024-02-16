# Installation

Open a terminal on this folder and create a virtual environment:

```console
python3 -m venv .venv
```

## Activate your python virtual environment:

### For Windows/PowerShell users:

```console
.venv/Scripts/Activate.ps1
```

### For Windows/cmd users:

```console
.venv/Scripts/activate.bat
```

### For bash users:

```console
. .venv/bin/activate
```

### For fish users:

```console
. .venv/bin/activate.fish
```

## Then install the required packages:

```console
.venv/bin/pip install -r python-requirements.txt
```

# Running Scripts

Every script must be run as a python module, from this exact folder. This is done by running:

```console
.venv/bin/python3 -m src.interface.<module_name>.<script_name>
```

For example, to run the `RGB-control/main.py` script, one should run:

```console
.venv/bin/python3 -m src.interface.RGB-control.main
```