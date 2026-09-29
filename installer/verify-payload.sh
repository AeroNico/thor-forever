#!/system/bin/sh
# Return a failure before installation if any pinned input differs.
# GameHub may prepend these exact diagnostics without a newline. Strip only
# recognized prefixes, then require the complete expected hash AND filename.
tf_checksum_line_matches()
{
    tf_check_line=$1
    tf_check_expected=$2
    while :; do
        case "$tf_check_line" in
            'Could not find memory region containing address /wine'*)
                tf_check_line=${tf_check_line#'Could not find memory region containing address /wine'} ;;
            'Could not find memory region containing address /box64'*)
                tf_check_line=${tf_check_line#'Could not find memory region containing address /box64'} ;;
            'Failed to inject process'*)
                tf_check_line=${tf_check_line#'Failed to inject process'} ;;
            *) break ;;
        esac
    done
    [ "$tf_check_line" = "$tf_check_expected" ]
}

tf_verify_payload()
{
    tf_payload=$1
    tf_report=$2
    while read -r tf_hash tf_name; do
        [ -n "$tf_hash" ] || continue
        tf_file="$tf_payload/$tf_name"
        [ -f "$tf_file" ] && [ ! -L "$tf_file" ] || {
            print -r -- "Missing component: $tf_name"; return 40;
        }
        /system/bin/toybox sha256sum "$tf_file" >"$tf_report" || return 41
        # Do not accept arbitrary prefix/suffix text or a partial digest match.
        tf_match=0
        while IFS= read -r tf_line || [ -n "$tf_line" ]; do
            if tf_checksum_line_matches "$tf_line" "$tf_hash  $tf_file"; then
                tf_match=1
            fi
        done <"$tf_report"
        [ "$tf_match" = 1 ] || { print -r -- "Checksum mismatch: $tf_name"; return 42; }
    done <<'THOR_HASHES'
41d22dca5c6ede633e59971f16bf180e449583648b4c804027e23353cce1a453 wine-runtime.tar
7da6a1fc8d741abd5b0404eca7a99fdf490c832626a290fb31689c38f5a3bcae d3d11.dll
35af848fd7e316113c54a13af2fe7e14760383d236fe29a6b8cd18f09e9c1f4e dxgi.dll
8aba6a640a60783e8c882066d3cd49e5155b07fc7e1a5dd0aa7009cef369465a libandroid-sysvshm.so
51c1b2c9d4c124923bbdc6fcf182629ca447dd20110bca0f1bae4aac12481401 libvulkan_freedreno.so
df76b24dd14b77e56727864702c4a589ebedb609bdf3bfdaefa30863101a9e8f libGL.so.1
82fc90739eadfbbe053d51ce18e3d1bdde4bcda5f204dfbfe3c6b5658027e319 trace.so
THOR_HASHES
    return 0
}
