#!/system/bin/sh
# Thor Forever launcher. No Battle.net/update invocation.
KIT=/sdcard/Download/Thor-Forever
USR=/data/user/0/com.ludashi.aibench/files/usr
case "${WINEPREFIX-}" in
    /data/user/*/com.ludashi.aibench/files/usr/*) USR=${WINEPREFIX%%/files/usr/*}/files/usr ;;
esac
case "$USR" in *'/../'*|*'/./'*|*/..|*/.) exit 3 ;; esac
ROOT="$USR/home/thor-forever/release-v1"
RUNTIME="$ROOT/runtime"
GL_DIR="$ROOT/graphics"
DRIVER="$ROOT/driver"
PREFIX="$ROOT/prefix"
STAGE="$ROOT/game"
GAME="$STAGE/_classic_beta_"
n=1
while [ "$n" -le 10000 ]; do
    OUT="$KIT/INSTALLED-WOW-$n"
    if mkdir "$OUT" 2>/dev/null; then break; fi
    n=$((n + 1))
done
[ "$n" -le 10000 ] || exit 2
exec >"$OUT/result.txt" 2>&1 </dev/null
tf_stage=preflight
trap 'tf_status=$?; print -r -- "SCRIPT_EXIT=$tf_status STAGE=$tf_stage"' EXIT
[ -f "$KIT/installer/discover-game.sh" ] || exit 3
. "$KIT/installer/discover-game.sh"
tf_discover_game "$USR" || { print -r -- 'STOP: a unique standard game installation was not found.'; exit 4; }
SOURCE=$TF_GAME_DIR
[ -s "$ROOT/components-ready" ] && [ -s "$ROOT/game-ready" ] || exit 5
[ -s "$PREFIX/system.reg" ] && [ ! -L "$ROOT" ] && [ ! -L "$PREFIX" ] || exit 6
# Refuse a copied executable that has become stale after a Battle.net update.
cmp -s "$SOURCE/WowB-ARM64.exe" "$GAME/WowB-ARM64.exe" || exit 7
cmp -s "$RUNTIME/lib/wine/aarch64-windows/ntdll.dll" "$PREFIX/drive_c/windows/system32/ntdll.dll" || exit 8
[ -s "$GAME/WowB-ARM64.exe" ] || exit 9
[ -s "$GAME/WTF/Config-Thor-Forever.wtf" ] || exit 10
for dll in dxgi.dll d3d11.dll; do
    cmp -s "$KIT/payload/$dll" "$PREFIX/drive_c/windows/system32/$dll" || exit 11
done
fail() { print -r -- "STOP: $1"; exit 12; }
# GameHub's process wrapper drops inherited fd9, so external flock cannot use it.
# Atomic directory lock with shell PID/start-time/boot identity instead.
LOCK="$USR/home/wow-private-launch.lockdir"
IFS= read -r boot_id </proc/sys/kernel/random/boot_id || fail 'Cannot identify the current device boot.'
get_stamp()
{
    proc_stamp=
    case "$1" in ''|*[!0-9]*) return 1 ;; esac
    [ -r "/proc/$1/stat" ] || return 1
    IFS= read -r proc_stat <"/proc/$1/stat" || return 1
    proc_tail=${proc_stat##*) }
    set -f
    set -- $proc_tail
    set +f
    [ "$#" -ge 20 ] || return 1
    shift 19
    proc_stamp="$boot_id:$1"
}
get_stamp "$$" || fail 'Cannot identify this launcher process.'
self_stamp="$proc_stamp"
if ! mkdir "$LOCK" 2>/dev/null; then
    [ -f "$LOCK/owner" ] && [ ! -L "$LOCK" ] && [ ! -L "$LOCK/owner" ] || fail 'Launch lock needs inspection; its owner could not be verified.'
    read -r owner_pid owner_stamp <"$LOCK/owner" || fail 'Cannot read the launch lock.'
    if get_stamp "$owner_pid" && [ "$proc_stamp" = "$owner_stamp" ]; then
        fail 'Another WoW launch is already active.'
    fi
    # Remove only our stale owner marker and then its empty lock directory.
    rm "$LOCK/owner" && rmdir "$LOCK" || fail 'Cannot release the old launch lock.'
    mkdir "$LOCK" || fail 'Another launch acquired the lock.'
fi
print -r -- "$$ $self_stamp" >"$LOCK/owner" || exit 4
cleanup_lock()
{
    read -r owner_pid owner_stamp <"$LOCK/owner" || return
    if [ "$owner_pid" = "$$" ] && [ "$owner_stamp" = "$self_stamp" ]; then
        rm "$LOCK/owner"
        rmdir "$LOCK"
    fi
}
trap cleanup_lock EXIT
trap 'exit 130' INT TERM HUP

export WINEPREFIX="$PREFIX" WINEARCH=win64 WINEESYNC=0
export WINELOADER="$RUNTIME/bin/wine" WINESERVER="$RUNTIME/bin/wineserver"
export PATH="$RUNTIME/bin:$PATH"
export LD_LIBRARY_PATH="$GL_DIR:$RUNTIME/lib:$RUNTIME/lib/wine/aarch64-unix${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_PRELOAD="$GL_DIR/trace.so${LD_PRELOAD:+:$LD_PRELOAD}"
export WINEDATADIR="$RUNTIME/share/wine" XDG_DATA_DIRS="$RUNTIME/share" WINEDLLPATH="$RUNTIME/lib/wine"
export WINEDLLOVERRIDES='dxgi,d3d11=n,b'
export WINEDEBUG='-all,err+all' WINEMU_REPLACED_DRIVER="$DRIVER"
export DXVK_LOG_LEVEL=info
export DXVK_LOG_PATH="Z:\\sdcard\\Download\\Thor-Forever\\INSTALLED-WOW-$n"
export DXVK_CONFIG='dxvk.enableGraphicsPipelineLibrary = False; dxgi.maxFrameRate = 30'
export MESA_LOG_LEVEL=warn MESA_LOG_FILE="$OUT/mesa.log"
unset WINEBUILDDIR LIBGL_ALWAYS_INDIRECT DXVK_SHADER_DUMP_PATH
trap 'tf_status=$?; print -r -- "SCRIPT_EXIT=$tf_status STAGE=$tf_stage"; "$WINESERVER" -k; cleanup_lock' EXIT
tf_stage=restart-test-prefix
"$WINESERVER" -k
/system/bin/toybox timeout -k 2 10 "$WINESERVER" -w || exit 13
tf_stage=game
cd "$GAME" || exit 18
print -r -- 'Starting WoW in the fresh prefix with separate WTF, Cache and Logs.'
"$WINELOADER" "$GAME/WowB-ARM64.exe" -d3d11 -config Config-Thor-Forever.wtf >"$OUT/wine.log" 2>&1
tf_result=$?
print -r -- "WOW_EXIT=$tf_result"
print -r -- 'TEST_FINISHED'
exit "$tf_result"
