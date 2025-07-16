@default:
    just --list

bumpversion:
  bumpversion patch

build:
  uv build

release:
  uv release

