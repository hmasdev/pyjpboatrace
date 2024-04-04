#!/bin/bash

# pyjpboatrace/__init__.py の ^__version__ *= *("|')(v?\d+\.\d+\.\d+.*)("|')$ を __version__ = "$VER" に変更する
sed -i -e "s/^__version__ *= *(\"|')(v?\d+\.\d+\.\d+.*)(\"|')$/__version__ = \"$VER\"/g" pyjpboatrace/__init__.py