# Sway Display Manager

## Overview

`swaydm` automatically detects and configures connected displays from defined profiles.

The tool is written to solve a specific issue that occurs when using ultra-wide monitor PBP mode outputs connected through a multi-monitor dock, i.e. inconsistent dock output names from name re-enumeration and displays with similar manufacturer identifiers. This combination breaks existing solutions like [Kanshi](https://gitlab.freedesktop.org/emersion/kanshi) in two ways: connector names (e.g. DP-[1-9]) may change after suspend or re-docking, breaking profiles that match by name; and **Kanshi** does not allow duplicate output identifiers within the same profile, making it impossible to configure displays in the mentioned setup.

### Profile Selection

`swaydm` solves this issue by matching the capabilities of each physical output against a profile's declared display, by name or vendor identifier, and its requested modes, rather than just the id. Profile displays are walked in order, and each is paired with the first unclaimed output that satisfies both checks. This lets a profile disambiguate outputs that share an identical identifier by pairing each display entry to the mode it actually reports.

#### Limitations

Matching still breaks down when two outputs share **both** the same identifier and the same mode, for example, a PBP-split ultra-wide where both halves report identical resolution/refresh. In that case identity + mode matching can't tell the outputs apart, and assignment falls back to declaration order, which may not match the physical layout.

### Architecture

`swaydm` runs as a daemon that listens for display hot-plug events via `i3ipc`. When an output change is detected, it compares connected displays against configured profiles by matching the display name (connector name or manufacturer, model, serial) and reported modes; matched profiles are applied over the `sway` socket. `swaydm` can also be used as the client to communicate with the running daemon to switch profiles manually.

## Configuration

The configuration file can be specified with the `-c/--config` option; otherwise, the default configurations paths will be used: `$XDG_CONFIG_HOME/swaydm/config.yaml` or `$XDG_CONFIG_HOME/swaydm.yaml`.

### Example

```yaml
profiles:
  - name: home
    displays:
      - name: "Samsung Electric Company LC49G95T H4ZR601140"
        alias: SIDE_OUTPUT
        mode:
          width: 1760
          height: 1440
          refresh: 60
          scale: 1.0
        position:
          x: 0
          y: 0
      - name: "Samsung Electric Company LC49G95T H4ZR601140"
        alias: MAIN_OUTPUT
        mode:
          width: 3360
          height: 1440
          refresh: 60
          scale: 1.0
        position:
          x: 1760
          y: 0

    commands:
      - "workspace number 1, move workspace to output {MAIN_OUTPUT}"
      - "workspace number 1"

  - name: home-manual-select
    auto: false
    displays:
      - name: "Samsung Electric Company LC49G95T H4ZR601140"
        alias: SIDE_OUTPUT
        mode:
          width: 1760
          height: 1440
          refresh: 60
          scale: 1.0
        position:
          x: 0
          y: 0
      - name: "Samsung Electric Company LC49G95T H4ZR601140"
        alias: MAIN_OUTPUT
        mode:
          width: 3360
          height: 1440
          refresh: 60
          scale: 1.0
        position:
          x: 1760
          y: 0

  - name: laptop
    displays:
      - name: "eDP-1"
        mode:
          width: 2256
          height: 1504
          refresh: 60
          scale: 1.0
        position:
          x: 0
          y: 0
```

## Installation

### UV

```sh
uv pip install git+https://github.com/arekisannda/sway-display-manager.git
```

### Nix

```sh
nix profile install github:arekisannda/sway-display-manager
```

## Usage

### Start process

```sh
swaydm daemon
```

### Switch profile

```sh
swaydm switch <profile>
```

## Alternatives

[Shikane](https://gitlab.com/w0lff/shikane) is a more general and actively maintained solution for the same problem. `swaydm` is purpose-built for the narrower dock/PBP-with-duplicate-identifiers case described above and is developed for use specifically for the [Sway](https://swaywm.org/) compositor.
