#!/bin/sh

# replace process with server, always use 8118 port internally, caddy will proxy the railway-assigned port, localhost listen
exec /opt/typesense-server --api-address 127.0.0.1 --api-port 8118