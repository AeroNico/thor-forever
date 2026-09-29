#!/system/bin/sh
# Internal library: caller supplies its dedicated, initialized installation root.
# Never run Battle.net against this layout: CASC Data is shared, not read-only.
tf_stage_game() (
    tf_source=$1
    tf_install=$2
    tf_template=$3
    tf_stage="$tf_install/game"
    tf_game="$tf_stage/_classic_beta_"
    # Check ancestors, not only the final directory. Platform aliases above the
    # app's home are handled by the component installer, not followed here.
    for tf_path in "$tf_install" "$tf_source"; do
        case "$tf_path" in *'/../'*|*'/./'*|*/..|*/.) exit 50 ;; esac
        while [ -n "$tf_path" ] && [ "$tf_path" != / ]; do
            [ ! -L "$tf_path" ] || exit 50
            case "$tf_path" in */home) break ;; esac
            case "$tf_path" in */*) tf_path=${tf_path%/*} ;; *) break ;; esac
        done
    done
    [ -s "$tf_install/components-ready" ] && [ ! -L "$tf_install/components-ready" ] || exit 51
    [ -s "$tf_source/WowB-ARM64.exe" ] && [ ! -L "$tf_source/WowB-ARM64.exe" ] || exit 52
    [ -s "$tf_template" ] && [ ! -L "$tf_template" ] || exit 53
    [ ! -e "$tf_stage" ] && [ ! -L "$tf_stage" ] || exit 54
    if [ -d "$tf_source/../Data" ] && [ ! -L "$tf_source/../Data" ]; then
        tf_data="$tf_source/../Data"
        tf_data_dest="$tf_stage/Data"
    elif [ -d "$tf_source/Data" ] && [ ! -L "$tf_source/Data" ]; then
        tf_data="$tf_source/Data"
        tf_data_dest="$tf_game/Data"
    else
        exit 55
    fi
    # Refuse suspicious executable/metadata links rather than silently omitting
    # one and producing an incomplete game. Never copy WTF, Account or caches.
    for tf_file in "$tf_source/"*.exe "$tf_source/"*.dll "$tf_source/"*.sig "$tf_source/.flavor.info" "$tf_source/../.build.info" "$tf_source/../.flavor.info"; do
        [ ! -L "$tf_file" ] || exit 56
        [ ! -e "$tf_file" ] || [ -f "$tf_file" ] || exit 56
    done
    mkdir "$tf_stage" || exit 57
    mkdir "$tf_game" "$tf_game/WTF" || exit 58
    for tf_file in "$tf_source/"*.exe "$tf_source/"*.dll "$tf_source/"*.sig "$tf_source/.flavor.info"; do
        [ -f "$tf_file" ] || continue
        cp "$tf_file" "$tf_game/${tf_file##*/}" || exit 59
        cmp -s "$tf_file" "$tf_game/${tf_file##*/}" || exit 59
    done
    for tf_file in .build.info .flavor.info; do
        [ -f "$tf_source/../$tf_file" ] || continue
        cp "$tf_source/../$tf_file" "$tf_stage/$tf_file" || exit 59
        cmp -s "$tf_source/../$tf_file" "$tf_stage/$tf_file" || exit 59
    done
    ln -s "$tf_data" "$tf_data_dest" || exit 60
    cp "$tf_template" "$tf_game/WTF/Config-Thor-Forever.wtf" || exit 61
    cmp -s "$tf_template" "$tf_game/WTF/Config-Thor-Forever.wtf" || exit 61
    print -r -- 'GAME_STAGED' >"$tf_install/game-ready" || exit 62
    print -r -- 'Separate game settings prepared. Shared Data is not read-only.'
)
