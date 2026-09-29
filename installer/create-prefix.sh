#!/system/bin/sh
# Source this library; tf_create_prefix runs in a subshell to isolate environment.
# Caller supplies a validated runtime, NEW prefix path and scoped GL-shim folder.
# No archive extraction, downloads, original-prefix copying or recursive deletion.
tf_create_prefix() (
    tf_runtime=$1
    tf_prefix=$2
    tf_gl=$3
    case "$tf_prefix" in
        /data/user/*/com.ludashi.aibench/files/usr/home/thor-forever/*) ;;
        *) print -r -- 'ERROR: prefix must be inside the dedicated Thor Forever directory.'; exit 20 ;;
    esac
    case "$tf_prefix" in *'/../'*|*'/./'*|*/..|*/.) exit 20 ;; esac
    # Refuse symlinks inside the dedicated app-home subtree. Android itself
    # may alias /data/user/0 to /data/data; do not reject that platform alias.
    tf_boundary=${tf_prefix%%/home/thor-forever/*}/home
    tf_parent=$tf_prefix
    while [ "$tf_parent" != "$tf_boundary" ] && [ "$tf_parent" != / ] && [ -n "$tf_parent" ]; do
        [ ! -L "$tf_parent" ] || exit 21
        tf_parent=${tf_parent%/*}
    done
    [ ! -e "$tf_prefix" ] || { print -r -- 'ERROR: destination already exists; nothing overwritten.'; exit 22; }
    for tf_file in bin/wine bin/wineboot bin/wineserver; do
        [ -x "$tf_runtime/$tf_file" ] || exit 23
    done
    for tf_file in lib/wine/aarch64-windows/ntdll.dll lib/wine/aarch64-windows/cryptbase.dll lib/wine/i386-windows/cryptbase.dll; do
        [ -s "$tf_runtime/$tf_file" ] || exit 24
    done
    [ -s "$tf_gl/libGL.so.1" ] || exit 25
    # Parent is provisioned by the installer; mkdir is atomic for this prefix.
    mkdir "$tf_prefix" || exit 26
    mkdir -p "$tf_prefix/drive_c/windows/system32" "$tf_prefix/drive_c/windows/syswow64" "$tf_prefix/dosdevices" || exit 27
    ln -s ../drive_c "$tf_prefix/dosdevices/c:" || exit 28
    ln -s / "$tf_prefix/dosdevices/z:" || exit 28
    for tf_dll in ntdll.dll cryptbase.dll; do
        cp "$tf_runtime/lib/wine/aarch64-windows/$tf_dll" "$tf_prefix/drive_c/windows/system32/$tf_dll" || exit 29
    done
    cp "$tf_runtime/lib/wine/i386-windows/cryptbase.dll" "$tf_prefix/drive_c/windows/syswow64/cryptbase.dll" || exit 29
    export WINEPREFIX="$tf_prefix" WINEARCH=win64 WINEESYNC=0
    export WINELOADER="$tf_runtime/bin/wine" WINESERVER="$tf_runtime/bin/wineserver"
    export PATH="$tf_runtime/bin:$PATH"
    export LD_LIBRARY_PATH="$tf_gl:$tf_runtime/lib:$tf_runtime/lib/wine/aarch64-unix${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    export WINEDATADIR="$tf_runtime/share/wine" XDG_DATA_DIRS="$tf_runtime/share"
    export WINEDLLPATH="$tf_runtime/lib/wine" WINEDEBUG='-all,err+all'
    export WINEDLLOVERRIDES='mscoree,mshtml='
    unset WINEBUILDDIR LIBGL_ALWAYS_INDIRECT
    # Cleanup is restricted to this new prefix, never the user's active prefix.
    trap '"$WINESERVER" -k' EXIT
    cd "$tf_prefix" || exit 30
    /system/bin/toybox timeout -k 5 90 "$tf_runtime/bin/wineboot" -u || exit 31
    /system/bin/toybox timeout -k 5 20 "$WINESERVER" -w || exit 32
    for tf_file in system.reg user.reg; do
        [ -s "$tf_prefix/$tf_file" ] || exit 33
    done
    for tf_dll in ntdll.dll cryptbase.dll; do
        cmp -s "$tf_runtime/lib/wine/aarch64-windows/$tf_dll" "$tf_prefix/dosdevices/c:/windows/system32/$tf_dll" || exit 34
    done
    print -r -- 'BOOTSTRAP_COMPLETE' >"$tf_prefix/thor-bootstrap-complete"
    print -r -- 'New prefix initialized. Game/DXVK validation is still required.'
)
