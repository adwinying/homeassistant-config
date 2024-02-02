# ESPHome Devices

ESPHome Device configs goes here.

## Setup

1. Install [nix](https://github.com/DeterminateSystems/nix-installer) with flakes enabled

2. Install [direnv](https://github.com/direnv/direnv)

3. Allow direnv to run in this directory using `direnv allow`

## Useful commands

- Init new device

```bash
$ esphome wizard [filename].yaml
```

- Build and run

```bash
$ esphome run [filename].yaml
```
