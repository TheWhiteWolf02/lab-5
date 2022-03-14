#define _GNU_SOURCE
#include <dlfcn.h>
#include <unistd.h>
#include <assert.h>
#include <errno.h>
#include <sys/select.h>
#include <stdlib.h>

typedef int (*select_type) (int, fd_set * restrict, fd_set * restrict, fd_set * restrict, struct timeval * restrict);
int select(int nfds, fd_set * restrict readfds,
                  fd_set * restrict writefds, fd_set * restrict exceptfds,
                  struct timeval * restrict timeout) {
    static select_type orig = 0;
    if (drand48 () < 0.1) {
        errno = ENOMEM;
        return -1;
    }
    if (0 == orig) {
        orig = (select_type)dlsym (RTLD_NEXT, "select");
        assert (orig && "original select function not found");
    }
    return orig(nfds, readfds, writefds, exceptfds, timeout);
}
