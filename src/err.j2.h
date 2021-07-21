#ifndef ERR_H_
#define ERR_H_

#include <errno.h>
/*
 * Simple error code handling and preserving.
 *
 * Call e_begin_function at the begin of the function
 * and call e_ret_fail in replace of the return statement
 * when you want to exit the function in case of an error.
 *
 * During the function execution you can use e_save_errno
 * and e_save_err_code
 * to save an error code into a temporal variable.
 * The former saves the errno variable while the latter
 * saves the value passed as parameter.
 *
 * The errno variable will be set (restored) to that value on e_ret_fail.
 *
 * Also you can use e_perror and e_perrorf to print to stderr
 * a message. The functions also save the error code like e_save_err_code.
 * You'll need to pass explicitly errno if that's the value you want to preserve.
 *
 * The difference between e_perror and e_perrorf is that the former
 * does not allow a format string (works like perror) while the latter it
 * does (works like fprintf)
 *
 * To use any of those you must include stdio.h and string.h.
 * */
#define e_begin_function int _err_last_errno = 0

#define e_save_err_code(v) do { _err_last_errno = (v); } while(0)
#define e_save_errno do { _err_last_errno = errno; } while(0)
#define e_remember_errno _err_last_errno

#define e_perrorf(v, fmt, ...) do { \
    _err_last_errno = (v); \
    fprintf(stderr, "[%s:%d] "fmt": %s\n", __FUNCTION__, __LINE__,  __VA_ARGS__, strerror(_err_last_errno)); } while(0)

#define e_perror(v, msg) do { \
    _err_last_errno = (v); \
    fprintf(stderr, "[%s:%d] %s: %s\n", __FUNCTION__, __LINE__,  (msg), strerror(_err_last_errno)); } while(0)

#define e_ret_fail(v) do { if (_err_last_errno) { errno = _err_last_errno; } ; return (v); } while(0)
#define e_ret_void_fail do { if (_err_last_errno) { errno = _err_last_errno; } ; return; } while(0)
#define e_ret_void do { if (_err_last_errno) { errno = _err_last_errno; } ; return; } while(0)

#endif
