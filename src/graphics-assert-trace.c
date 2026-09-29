/* SPDX-License-Identifier: MIT
 * Original diagnostic helper. It forwards fatal assertions, never suppresses them.
 * Output may contain local paths; logs are private and must not ship in releases.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <unwind.h>
#include <string.h>
/* Preserve fatal assertions; only record their origin before forwarding. */
static _Unwind_Reason_Code frame(struct _Unwind_Context *ctx, void *unused)
{
    (void)unused;
    void *pc = (void *)_Unwind_GetIP(ctx);
    Dl_info info = {0};
    if (dladdr(pc, &info))
        fprintf(stderr, "ASSERT_FRAME pc=%p module=%s offset=%lx symbol=%s\n",
                pc, info.dli_fname, (unsigned long)((char *)pc - (char *)info.dli_fbase),
                info.dli_sname ? info.dli_sname : "?");
    return _URC_NO_REASON;
}
__attribute__((noreturn)) void __assert2(const char *file, int line,
                                       const char *function, const char *expression)
{
    fprintf(stderr, "GRAPHICS_ASSERT pid=%d file=%s line=%d function=%s expression=%s\n",
            getpid(), file, line, function, expression);
    _Unwind_Backtrace(frame, NULL);
    FILE *maps = fopen("/proc/self/maps", "r");
    if (maps) {
        char row[2048];
        while (fgets(row, sizeof(row), maps)) {
            if (strstr(row, ".so") || strstr(row, "/wine"))
                fprintf(stderr, "ASSERT_MAP %s", row);
        }
        fclose(maps);
    }
    fflush(stderr);
    typedef void (*assert_fn)(const char *, int, const char *, const char *);
    assert_fn original = (assert_fn)dlsym(RTLD_NEXT, "__assert2");
    if (original) original(file, line, function, expression);
    abort();
}
