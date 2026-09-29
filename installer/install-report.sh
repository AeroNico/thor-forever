#!/system/bin/sh
# Source before enabling the installer's EXIT trap. No personal paths in report.
tf_install_report() {
    tf_report_code=$1
    if [ "$tf_report_code" = 0 ]; then
        tf_report_state=PREPARED_NOT_VALIDATED
        tf_report_message='Files prepared. Android launch and persistence tests are still required.'
    else
        tf_report_state=STOPPED
        case "$TF_PHASE" in
            payload) tf_report_message='Required component files are missing or failed verification.' ;;
            storage) tf_report_message='Internal storage could not be checked or is insufficient.' ;;
            extraction) tf_report_message='Runtime extraction failed. Keep this attempt for diagnosis.' ;;
            components) tf_report_message='Component copy or verification failed.' ;;
            prefix) tf_report_message='The separate Windows environment could not be initialized.' ;;
            dxvk) tf_report_message='Graphics components could not be installed or verified.' ;;
            game) tf_report_message='The separate game layout could not be prepared.' ;;
            *) tf_report_message='Preparation stopped before completion.' ;;
        esac
    fi
    {
        print -r -- "STATUS=$tf_report_state"
        print -r -- "PHASE=$TF_PHASE"
        print -r -- "EXIT_CODE=$tf_report_code"
        print -r -- "$tf_report_message"
        print -r -- 'Existing GameHub runtime and startup entry were not replaced.'
        print -r -- 'Do not delete or overwrite an unfinished attempt automatically.'
    } >"$TF_INSTALL/result.txt"
}
