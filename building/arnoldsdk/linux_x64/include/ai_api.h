// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * DLL export prefix for API functions (necessary for multi-platform development)
 */

#pragma once

// Warn about the use of deprecated API
// This has been enabled by default since Arnold 7.0.1.0
#ifndef AI_ENABLE_DEPRECATION_WARNINGS
#define AI_ENABLE_DEPRECATION_WARNINGS 1
#endif

#ifdef __cplusplus
#define AI_EXTERN_C extern "C"
#else
#define AI_EXTERN_C extern
#endif

#if _MSC_VER && !__INTEL_COMPILER
// Currently the microsoft compiler does not support these annotations
# define AI_PURE_ATTRIBUTE
# define AI_CONST_ATTRIBUTE
#else
// GCC, Clang, and ICC are ok with these
# define AI_PURE_ATTRIBUTE  pure
# define AI_CONST_ATTRIBUTE const
#endif

#ifdef __CUDACC__
# define AI_API
# define AI_DEPRECATED
# define AI_PURE
# define AI_CONST
# define AI_UNAVAILABLE
#else
# ifdef _WIN32
// Public functions need a special declaration in Win32
#  ifdef _ARNOLDDLL
#   define AI_API AI_EXTERN_C __declspec(dllexport)
#  else
#   define AI_API AI_EXTERN_C __declspec(dllimport)
#  endif
#  if (defined(AI_ENABLE_DEPRECATION_WARNINGS) && AI_ENABLE_DEPRECATION_WARNINGS > 0)
#   define AI_DEPRECATED      __declspec(deprecated)
#  endif
#  define AI_PURE             __declspec(AI_PURE_ATTRIBUTE)
#  define AI_CONST            __declspec(AI_CONST_ATTRIBUTE)
#  define AI_UNAVAILABLE      __declspec(deprecated)
# else
#  if (defined(AI_ENABLE_DEPRECATION_WARNINGS) && AI_ENABLE_DEPRECATION_WARNINGS > 0)
#   define AI_DEPRECATED      __attribute__(( deprecated ))
#  endif
#  define AI_API  AI_EXTERN_C __attribute__(( visibility("default") ))
#  define AI_PURE             __attribute__(( AI_PURE_ATTRIBUTE ))
#  define AI_CONST            __attribute__(( AI_CONST_ATTRIBUTE ))
#  ifdef __clang__
#   define AI_UNAVAILABLE __attribute__((unavailable))
#  elif __GNUC__ >= 4 && __GNUC_MINOR__ >= 3 && !__INTEL_COMPILER
#   define AI_UNAVAILABLE __attribute__((error("This function is not allowed to be used")))
#  else
    // Using deprecated isn't quite strong enough, but it's the best we can do in this compiler
#   define AI_UNAVAILABLE __attribute__((deprecated))
#  endif
# endif
#endif

#if (!defined(AI_ENABLE_DEPRECATION_WARNINGS) || AI_ENABLE_DEPRECATION_WARNINGS == 0)
# define AI_DEPRECATED
#endif

// Suppress warnings for returning structs such as colors from functions with
// C linkage. These are POD types so it is safe. When we switch to C++ linkage
// we can remove these pragmas.
#ifdef __clang__
# pragma GCC diagnostic ignored "-Wreturn-type-c-linkage"
#elif defined (_MSC_VER)
# pragma warning( disable : 4190 )
#endif

// Hint to compiler for how to optimize conditional statements.  Only use this
// for very unlikely and likely conditions.  For instance, unlikely means
// happens .1% of the time, not 30% of the time.  The main transformation this
// causes is to move the unlikely code to the end of the function so that L1
// instruction cache is not polluted by rare code. See trac#4145
#if (defined(_MSC_VER) && !defined(__INTEL_COMPILER)) || defined(__CUDACC__)
#define   Ai_likely(expr) (expr)
#define Ai_unlikely(expr) (expr)
#else
#define   Ai_likely(expr) (__builtin_expect(!!(expr), true))
#define Ai_unlikely(expr) (__builtin_expect(!!(expr), false))
#endif

// This offers stronger guarantees than inline
#if defined(__INTEL_COMPILER) || defined(_MSC_VER)
# define AI_FORCEINLINE __forceinline
#else
# define AI_FORCEINLINE __attribute__ ((always_inline))
#endif

// ARNOLD_FORCEINLINE is deprecated since it adds "inline" keyword on gcc/clang
#if defined(__INTEL_COMPILER) || defined(_MSC_VER)
#define ARNOLD_FORCEINLINE AI_FORCEINLINE
#else
// assumes gcc/clang
#define ARNOLD_FORCEINLINE AI_FORCEINLINE inline
#endif

// CUDA compiler support
#ifdef __CUDACC__
# ifndef AI_DEVICE
#  define AI_DEVICE __device__
# endif
# ifndef AI_GPU_COMPILER
#  define AI_GPU_COMPILER
# endif
#define AI_GPU_NO_INLINE __noinline__
#define AI_GPU_FORCE_INLINE __forceinline__
#else
# ifndef AI_DEVICE
#  define AI_DEVICE
# endif
# ifndef AI_CPU_COMPILER
#  define AI_CPU_COMPILER
# endif
#define AI_GPU_NO_INLINE
#define AI_GPU_FORCE_INLINE
#endif

// Utility macro for optional methods
/// @cond internal
#define AI_OPTIONAL_METHOD_INSTALL(methods, name)                     \
static bool ai_install_##name() { methods.name = name; return true; } \
static const bool ai_installed_##name = ai_install_##name();
/// @endcond

/**
 * Whether a function call is blocking (synchronous) or not (asynchronous)
 */
enum AtBlockingCall
{
   AI_BLOCKING,     /**< synchronous, blocking call; returns when the task is done                       */
   AI_NON_BLOCKING  /**< asynchronous, non-blocking call; returns ASAP, task completes in the background */
};
