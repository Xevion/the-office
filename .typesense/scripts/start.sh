#!/bin/sh

# exit as soon as a single command finishes (any status), kill the rest
parallel --ungroup --halt now,done=1 ::: \
    "./start_caddy.sh" \
    "./start_typesense.sh"

# always exit with a failure status
false