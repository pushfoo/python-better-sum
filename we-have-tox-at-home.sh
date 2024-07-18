#!/bin/bash

# https://knowyourmeme.com/memes/we-have-food-at-home

Usage() {
cat <<EOF
$0 [ PY_VERSION_OR_PATH ]

Temporary off-brand tox to get things done fast.

DISPOSABLE_VENV_NAME will be loaded in the following order:

1. The first argument
2. The environment variable
3. ".venv-disposable-python3" if none are specified

EOF
}

error() {
  cat <<< "ERROR: $@" 1>&2
}

if [ $# -gt 1 ]; then
  error "This script takes 0 or 1 arguments. Run with --help for more info."
  exit 1
elif [ $# -eq 0 ]; then
  WHICH_PY="python3"
elif [[ "$1" =~ ^python3\.[0-9]+$ ]]; then
  WHICH_PY="$1"
elif [ "$1" == "--help" ]; then
  Usage
  exit 0
fi

VENV_NAME=".venv-disposable-$WHICH_PY"
echo "Using venv name '$VENV_NAME'"

set -e
echo "Now in exit-on-error mode"

if [ -d "$VENV_NAME" ]; then
  echo "Venv '$VENV_NAME' already exists, deleting..."
  rm -r "$VENV_NAME"
fi

$WHICH_PY -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"
python -m pip install --upgrade pip
pip install -I -e .[dev]
mkdocs serve


while true; do
  read -p "Clean up '$VENV_NAME' (Y/n)?" yesno
  case $yesno in
    [Yy]* )
      deactivate
      rm -r "$VENV_NAME"
      break
      ;;
    [Nn*] )
      exit
      break
      ;;
    * ) echo "Please answer with Y/N."
  esac
done