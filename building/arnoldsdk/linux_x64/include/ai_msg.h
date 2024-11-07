// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for logging messages of different severities - info, warnings, errors
 */

#pragma once
#include "ai_api.h"
#include <stdint.h> // uint32_t etc
#include <stddef.h>

class AtUniverse;
struct AtParamValueMap;

/** \defgroup ai_msg Message Logging API
 * 
 * Log management and operation.
 * 
 * \{
 */

#if !defined(__AI_FILE__)
#define __AI_FILE__ __FILE__
#endif
#if !defined(__AI_LINE__)
#define __AI_LINE__ __LINE__
#endif
#if !defined(__AI_FUNCTION__)
#define __AI_FUNCTION__ __FUNCTION__
#endif

/**
 * \name Severity Codes
 * \{
 */
#define AI_SEVERITY_INFO       0x00    /**< regular information message */ 
#define AI_SEVERITY_WARNING    0x01    /**< warning message             */
#define AI_SEVERITY_ERROR      0x02    /**< error message               */
#define AI_SEVERITY_FATAL      0x03    /**< fatal error message         */
/*\}*/

/**
 * \name Logging Flags
 * \{
 */
#define AI_LOG_NONE            0x0000  /**< don't show any messages                                  */
#define AI_LOG_INFO            0x0001  /**< show all regular information messages                    */
#define AI_LOG_WARNINGS        0x0002  /**< show warning messages                                    */
#define AI_LOG_ERRORS          0x0004  /**< show error messages                                      */
#define AI_LOG_DEBUG           0x0008  /**< show debug messages                                      */
#define AI_LOG_STATS           0x0010  /**< show detailed render statistics                          */
#define AI_LOG_ASS_PARSE       0x0020  /**< show .ass-file parsing details                           */
#define AI_LOG_PLUGINS         0x0040  /**< show details about plugins loaded                        */
#define AI_LOG_PROGRESS        0x0080  /**< show progress messages at 5% increments while rendering  */
#define AI_LOG_NAN             0x0100  /**< show warnings for pixels with NaN's                      */
#define AI_LOG_TIMESTAMP       0x0200  /**< prefix messages with a timestamp (elapsed time)          */
#define AI_LOG_BACKTRACE       0x0400  /**< show stack contents after abnormal program termination (\c SIGSEGV, etc) */
#define AI_LOG_MEMORY          0x0800  /**< prefix messages with current memory usage                */
#define AI_LOG_COLOR           0x1000  /**< add colors to log messages based on severity             */
#define AI_LOG_STATUS          0x2000  /**< flag associated with messages reporting overall status   */
/** set all flags at once
 *  (except AI_LOG_STATUS, since status messages use the logging callback mechanism but are not intended to appear in the log)
*/
#define AI_LOG_ALL                                            \
 ( AI_LOG_INFO       | AI_LOG_WARNINGS   | AI_LOG_ERRORS    | \
   AI_LOG_DEBUG      | AI_LOG_STATS      | AI_LOG_PLUGINS   | \
   AI_LOG_PROGRESS   | AI_LOG_NAN        | AI_LOG_ASS_PARSE | \
   AI_LOG_TIMESTAMP  | AI_LOG_BACKTRACE  | AI_LOG_MEMORY    | \
   AI_LOG_COLOR      )
/*\}*/

#ifndef AI_PRINTF_ARGS
#  ifdef __GNUC__
      // Enable printf-like warnings with gcc by attaching
      // AI_PRINTF_ARGS to printf-like functions.  Eg:
      //
      // void foo (const char* fmt, ...) AI_PRINTF_ARGS(1,2);
      //
      // The arguments specify the positions of the format string and the the
      // beginning of the varargs parameter list respectively.
#     define AI_PRINTF_ARGS(fmtarg_pos, vararg_pos) __attribute__ ((format (printf, fmtarg_pos, vararg_pos) ))
#  else
#     define AI_PRINTF_ARGS(fmtarg_pos, vararg_pos)
#  endif
#endif

/** Custom message callback, as passed to AiMsgSetCallback() */ 
typedef void (*AtMsgCallBack)(int logmask, int severity, const char* msg_string, int tabs);

/** Custom message callback, as passed to AiMsgRegisterCallback()
 * 
 * The following items will be passed to the callback through the \c metadata list:
 *
 *  <table>
 *  <tr><th>Name<th>Type<th>Description
 *  <tr><td>universe<td> Universe*<td>Universe this log message refers to
 *  </table>
 */
typedef void (*AtMsgExtendedCallBack)(int logmask, int severity, const char* msg_string, AtParamValueMap* metadata, void* user_ptr);

AI_API void AiMsgSetLogFileName(const char* filename);
AI_API void AiMsgSetLogFileFlags(const AtUniverse* universe, int flags);
AI_API void AiMsgSetConsoleFlags(const AtUniverse* universe, int flags);
AI_API int  AiMsgGetLogFileFlags(const AtUniverse* universe);
AI_API int  AiMsgGetConsoleFlags(const AtUniverse* universe);

AI_API void AiMsgSetMaxWarnings(int max_warnings);
AI_API AI_DEPRECATED void AiMsgSetCallback(AtMsgCallBack func);
AI_API AI_DEPRECATED void AiMsgAddCallback(AtMsgCallBack func);
AI_API AI_DEPRECATED void AiMsgResetCallback();
AI_API unsigned int AiMsgRegisterCallback(AtMsgExtendedCallBack func, int mask, void* user_ptr);
AI_API void         AiMsgDeregisterCallback(unsigned int callback_id);
AI_API void         AiMsgSetCallbackMask(unsigned int callback_id, int mask);
AI_API int          AiMsgGetCallbackMask(unsigned int callback_id);

#ifdef AI_GPU_COMPILER
# define AiMsgInfo(format, ...)    // do nothing
# define AiMsgDebug(format, ...)   // do nothing
# define AiMsgWarning(format, ...) // do nothing
# define AiMsgError(format, ...)   // do nothing
# define AiMsgFatal(format, ...)   // do nothing
#else
AI_API void AiMsgInfo(const char* format, ...) AI_PRINTF_ARGS(1,2);
AI_API void AiMsgDebug(const char* format, ...) AI_PRINTF_ARGS(1,2);
AI_API void AiMsgWarning(const char* format, ...) AI_PRINTF_ARGS(1,2);
AI_API void AiMsgError(const char* format, ...) AI_PRINTF_ARGS(1,2);
AI_API void AiMsgFatal(const char* format, ...) AI_PRINTF_ARGS(1,2);
#endif

AI_API void AiMsgTab(int tabinc);

AI_API size_t   AiMsgUtilGetUsedMemory();
AI_API uint32_t AiMsgUtilGetElapsedTime();

AI_API void AiMsgSystemInfo(const AtUniverse* universe);

/*\}*/
