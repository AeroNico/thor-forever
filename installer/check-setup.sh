#!/system/bin/sh
# Run inside the GameHub container, not from an ordinary Android shell.
# Private report only; no game files, settings, registry or account data are read.
case "$0" in */*) TF_DIR=${0%/*} ;; *) exit 2 ;; esac
exec >"$TF_DIR/setup-check.txt" 2>&1 </dev/null
print -r -- 'Thor Forever: read-only setup check'
[ -f "$TF_DIR/discover-game.sh" ] || { print -r -- 'The download is incomplete. Extract the entire package.'; exit 2; }
. "$TF_DIR/discover-game.sh"
TF_USR=/data/user/0/com.ludashi.aibench/files/usr
case "${WINEPREFIX-}" in
    /data/user/*/com.ludashi.aibench/files/usr/*)
        TF_USR=${WINEPREFIX%%/files/usr/*}/files/usr ;;
esac
if [ ! -r "$TF_USR/home/virtual_containers" ]; then
    print -r -- 'Cannot access this GameHub installation. Open Check-Setup.cmd from its container desktop.'
    print -r -- 'Only GameHub Lite Ludashi is supported by this prototype.'
    exit 12
fi
tf_discover_game "$TF_USR"
tf_result=$?
case "$tf_result" in
    0) print -r -- 'FOUND: one ARM64 Forever Beta installation.'
       print -r -- 'No path editing is needed for this standard layout.' ;;
    10) print -r -- 'NOT FOUND: install Forever Beta through Battle.net, or wait for custom-folder selection support.' ;;
    11) print -r -- 'MULTIPLE INSTALLATIONS: automatic selection was stopped. Folder selection is not implemented yet.' ;;
esac
print -r -- 'Nothing was installed or changed. Runtime/prefix installation is not enabled in this prototype.'
exit "$tf_result"
