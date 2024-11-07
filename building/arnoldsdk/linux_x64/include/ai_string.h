// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * AtString class for fast comparisons
 */

#pragma once
#include "ai_api.h"

#include <stddef.h> 

/**
 * \defgroup ai_string AtString API
 *
 * AtString class for fast comparisons
 * \{
 */


////////////////////   private internal API functions.  ////////////////////////
//  Do not use these functions directly.  Instead use the AtString class
/// @cond internal
AI_API         const char* AiCreateAtStringData_private(const char*);
AI_API AI_PURE size_t      AiAtStringLength(const char*);
AI_API AI_PURE AI_DEVICE size_t AiAtStringHash(const char*);
/// @endcond
////////////////////////////////////////////////////////////////////////////////

/**
 * Arnold String allows for fast string comparisons.  Since it is expensive to
 * create, try to create an AtString once in a preprocess, for instance in
 * \c node_initialize, and then reuse it instead of creating it over and over, for
 * instance, in \c shader_evaluate where it could get called millions of times.
 * For string constants, use a <tt>static const</tt> in the function, or better
 * yet, in the global scope:
 *
 * \code
 * static const AtString some_string("some_string"); // this is created only once
 * void Foo() {
 *    func_that_uses_string(some_string);
 * }
 * \endcode
 *
 * The underlying string data contained by an AtString will exist over the
 * entire lifetime of the Arnold library.  If you unload the Arnold library in
 * your process, any AtString objects still in existence will become invalid
 * and using them will likely result in a crash or other undefined behavior.
 */
class AtString {
public:
   AI_DEVICE AtString() : data(NULL) { }

   /**
    * Creating an AtString from a char* is an expensive operation.  Try not to
    * do this often.  Copying AtString is just a fast pointer copy, so passing
    * AtString by value is fine.  Passing NULL to the AtString constructor is
    * valid and c_str() will then return NULL.
    */
   explicit AtString(const char* str) { data = AiCreateAtStringData_private(str); }

   /**
    * Comparing two AtString objects is an extremely fast pointer comparison.
    */
   AI_DEVICE bool operator== (const AtString &rhs) const { return data == rhs.data; }
   AI_DEVICE bool operator!= (const AtString &rhs) const { return data != rhs.data; }
   /**
    * Computing the length is a fast constant time operation.
    */
   size_t length() const { return AiAtStringLength(data); }

   /**
    * Returns true if underlying char* is NULL or "".
    */
#ifdef AI_CPU_COMPILER
   bool empty() const { return length() == 0; }
#else
   AI_DEVICE bool empty() const;
#endif

   /**
    * AtString will automatically call c_str() in most situations and so can be
    * automatically used in places that expect a \c char*.  However, functions
    * with a variable number of arguments (printf, AiMsg, ...) will require
    * manually converting to char* with the c_str() member function.
    *
    * \code
    * void Bar(const char* str);
    * void Foo(const AtString astr) {
    *    Bar(astr);                // passing AtString to a function that expects a const char* happens automatically
    *    const char* cstr = astr;  // likewise, passing an AtString to a const char* is automatic.  These have no overhead.
    *    printf("calling printf must use c_str() method: %s", astr.c_str());
    * } \endcode
    */
   operator const char*() const { return c_str(); }
   /**
    * Returns the string as a <tt>const char*</tt>.  Calling this directly is
    * not normally needed and instead an AtString can be directly used as if it
    * was a <tt>const char*</tt>.
    */
   AI_DEVICE const char* c_str() const { return data; }

   AI_DEVICE void clear() { data = NULL; }

   /**
    * Returns a hashed version of the string. This hash is not guaranteed to stay
    * the same across Arnold versions, it should not be written to file or used to
    * influence the look of a shader.
    */
   AI_DEVICE size_t hash() const { return AiAtStringHash(data); }

private:
   const char* data;
/// @cond internal
   friend void setAtStringInternalData(AtString &str, const char* data);

   // Comparing a char* with an AtString is not allowed since this would
   // require using a strcmp or casting the char* to AtString.  Both of these
   // are slow and users expect comparisons with AtString to be fast.  Since it
   // is too easy to accidentally do this slow comparison without realizing
   // it's slow, we make this a compiler error.  Note these are not defined on
   // purpose so that using these functions will cause a linker error.
   bool operator== (const char* rhs) const;
   bool operator!= (const char* rhs) const;
   AI_UNAVAILABLE friend inline bool operator==(const char* lhs, const AtString& rhs);
   AI_UNAVAILABLE friend inline bool operator!=(const char* lhs, const AtString& rhs);
/// @endcond
};

/**
 * Functor class to use as a hasher when you want to make a hash map or
 * hash set using AtString as a key.
 */
class AtStringHash
{
public:
    size_t operator() (const AtString &s) const { return s.hash(); }
};
/*\}*/
