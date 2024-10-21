#!/usr/bin/env bash

# APT PACKAGES
packages=()
sudo apt-get update && sudo apt-get upgrade
sudo apt-get --ignore-missing install $packages
