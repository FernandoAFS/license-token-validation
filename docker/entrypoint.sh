#!/bin/sh
set -e

DATA_PATHS="/.config/ /keys /tokens"
USER=${USER:-"token:token"}

CMD_SERVER="gosu $USER tini -- token-server"
CMD_CLIENT="gosu $USER tini -- token-client"

# CHOWN WORKDIR NO MATTER WHAT.
if [ "$(id -u)" = '0' ]; then
    chown -R "$USER" . || exit 1
fi

# this if will check if the first argument is a flag
# but only works if all arguments require a hyphenated flag
# -v; -SL; -f arg; etc will work, but not arg1 arg2
if [ "$#" -eq 0 ] || [ "${1#-}" != "$1" ]; then
    set -- "$CMD_SERVER" "$@"
fi

for d in $DATA_PATHS
do
    if [ -d "$d" ]; then
        chown "$USER" "$d"
    fi
done

# check for the expected command
if [ "$1" = 'server' ]; then
    shift
    exec $CMD_SERVER $@
fi

if [ "$1" = 'client' ]; then
    shift
    exec $CMD_CLIENT $@
fi

# else default to run whatever the user wanted like "bash" or "sh"
exec "$@"

