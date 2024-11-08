// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Critical section type that helps when writing multi-platform threaded code
 */

#pragma once
#include "ai_api.h"
#include "ai_stats.h"

/** \defgroup ai_critsec Mutex API
 * \{
 */

/**
 * Wrapper for Lockable type mutexes, such as std::mutex and
 * std::recursive_mutex. Use this so that the arnold profiler can keep track of
 * of the time spent blocked waiting to lock. For instance, you can replace the following C++11/14 code:
 * \code
 std::mutex my_mutex;
 std::lock_guard<std::mutex> my_guard(my_mutex);
 \endcode
 * with:
 * \code
  AtProfiledLockable<std::mutex> my_mutex;
  std::lock_guard<AtProfiledLockable<std::mutex>> my_guard(my_mutex);
 \endcode
 *
 * As a convenience, the AtMutex and AtRecursiveMutex type aliases can be used
 * so that instead one would write:
 * \code
  AtMutex my_mutex;
  std::lock_guard<AtMutex> my_guard(my_mutex);
 \endcode
 *
 * Note that starting with C++17 this can be further simplified to:
 * \code
  AtMutex my_mutex;
  std::lock_guard my_guard(my_mutex);
 \endcode
 */
template<class Mutex>
class AtProfiledLockable {
public:
   void lock()
   {
      AiProfileBlock("thread blocked");
      mutex.lock();
   }
   bool try_lock()
   {
      AiProfileBlock("thread blocked");
      return mutex.try_lock();
   }
   void unlock() { mutex.unlock(); }

   using mutex_type         = Mutex;

// native_handle() does not exist in VS 2022 v17.8 and newer
#if !defined(_MSC_VER) || _MSC_VER < 1937
   using native_handle_type = typename Mutex::native_handle_type;
   native_handle_type native_handle() { return mutex.native_handle(); }
#endif

   const mutex_type& get() const { return mutex; }
         mutex_type& get()       { return mutex; }

private:
   Mutex mutex;
};

// Visual Studio 2015, VS2015 Update 1, and maybe Update 2 will produce a warning when
// including mutex header. Upgrade VS compiler to at least VS 2015 Update 3 in order to use stl mutexes
#if !(defined _MSC_FULL_VER && _MSC_FULL_VER <= 190023918) // 190023918 is VS 2015 Update 2
# include <mutex>
/**
 * Convenience type aliases. See \ref AtProfiledLockable
 */
using AtMutex          = AtProfiledLockable<std::mutex>;
using AtRecursiveMutex = AtProfiledLockable<std::recursive_mutex>;
#endif

/*\}*/

/*\}*/
