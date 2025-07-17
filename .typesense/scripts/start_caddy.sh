#!/bin/sh

# replace process with caddy, redirect stderr to stdout
exec caddy run --config Caddyfile --adapter caddyfile 2>&1