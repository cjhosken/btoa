// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**  
 * \file
 * Generic array data type and methods
 */

#pragma once
#include "ai_color.h"
#include "ai_math.h"
#include "ai_matrix.h"
#include "ai_string.h"
#include "ai_vector.h"
#include "ai_api.h"
#include <stdint.h> // uint32_t etc

/** \defgroup ai_array AtArray API
 *
 *  \ref AtArray objects construction and manipulation.
 * 
 *  \details
 *  The AtArray object encapsulates an array of any of the Arnold built-in
 *  data types like \c AI_TYPE_BYTE, \c AI_TYPE_FLOAT, \c AI_TYPE_STRING, etc.
 *  Its API has easy-to-use accessor functions for reading and writing
 *  elements, and there are a number of functions for manipulating arrays 
 *  (such as copying them).
 *  An AtArray is specified by the element data type, the number of motion keys
 *  in the array, and the number of elements per motion key. The data is
 *  grouped together by motion keys.
 *
 * \{
 */

/** Generic array data type */
class AtArray;

AI_API         AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, ...);
AI_API         AtArray* AiArrayAllocate(uint32_t nelements, uint8_t nkeys, uint8_t type);
AI_API         void     AiArrayDestroy(AtArray* array);
AI_API         AtArray* AiArrayConvert(uint32_t nelements, uint8_t nkeys, uint8_t type, const void* data);
AI_API         void     AiArrayResize(AtArray* array, uint32_t nelements, uint8_t nkeys);
AI_API         AtArray* AiArrayCopy(const AtArray* array);
AI_API         bool     AiArraySetKey(AtArray* array, uint8_t key, const void* data);
AI_API         void*    AiArrayMap(AtArray* array);
AI_API         void*    AiArrayMapKey(AtArray* array, uint8_t key);
AI_API         void     AiArrayUnmap(AtArray* array);
AI_API AI_PURE uint32_t AiArrayGetNumElements(const AtArray* array);
AI_API AI_PURE uint8_t  AiArrayGetNumKeys(const AtArray* array);
AI_API AI_PURE uint8_t  AiArrayGetType(const AtArray* array);
AI_API AI_PURE size_t   AiArrayGetDataSize(const AtArray* array);
AI_API AI_PURE size_t   AiArrayGetKeySize(const AtArray* array);
AI_API AI_PURE AtVector AiArrayInterpolateVec(const AtArray* array, float time, uint32_t idx);
AI_API AI_PURE AtRGB    AiArrayInterpolateRGB(const AtArray* array, float time, uint32_t idx);
AI_API AI_PURE AtRGBA   AiArrayInterpolateRGBA(const AtArray* array, float time, uint32_t idx);
AI_API AI_PURE float    AiArrayInterpolateFlt(const AtArray* array, float time, uint32_t idx);
AI_API AI_PURE AtMatrix AiArrayInterpolateMtx(const AtArray* array, float time, uint32_t idx);

/** \name AtArray Getters
 *
 * \details
 * The following getter functions return the i'th element in an array of the
 * given type.
 * In case of out-of-bounds access, an error message is generated
 * \{
 */
AI_API AI_PURE bool      AiArrayGetBool (const AtArray* a, uint32_t i);
AI_API AI_PURE uint8_t   AiArrayGetByte (const AtArray* a, uint32_t i);
AI_API AI_PURE int       AiArrayGetInt  (const AtArray* a, uint32_t i);
AI_API AI_PURE uint32_t  AiArrayGetUInt (const AtArray* a, uint32_t i);
AI_API AI_PURE float     AiArrayGetFlt  (const AtArray* a, uint32_t i);
AI_API AI_PURE AtRGB     AiArrayGetRGB  (const AtArray* a, uint32_t i);
AI_API AI_PURE AtRGBA    AiArrayGetRGBA (const AtArray* a, uint32_t i);
AI_API AI_PURE AtVector2 AiArrayGetVec2 (const AtArray* a, uint32_t i);
AI_API AI_PURE AtVector  AiArrayGetVec  (const AtArray* a, uint32_t i);
AI_API AI_PURE AtMatrix  AiArrayGetMtx  (const AtArray* a, uint32_t i);
AI_API AI_PURE AtString  AiArrayGetStr  (const AtArray* a, uint32_t i);
AI_API AI_PURE void*     AiArrayGetPtr  (const AtArray* a, uint32_t i);
AI_API AI_PURE AtArray*  AiArrayGetArray(const AtArray* a, uint32_t i);
/*\}*/

/** \name AtArray Setters
 *
 * \details
 * The following functions write an element of a given type into the i'th position
 * in an array. If the write was succesful, these functions will return true, otherwise
 * a detailed error message will be logged and false will be returned.
 *
 * \{
 */
AI_API bool AiArraySetBool (AtArray* a, uint32_t i, bool val);
AI_API bool AiArraySetByte (AtArray* a, uint32_t i, uint8_t val);
AI_API bool AiArraySetInt  (AtArray* a, uint32_t i, int val);
AI_API bool AiArraySetUInt (AtArray* a, uint32_t i, uint32_t val);
AI_API bool AiArraySetFlt  (AtArray* a, uint32_t i, float val);
AI_API bool AiArraySetRGB  (AtArray* a, uint32_t i, AtRGB val);
AI_API bool AiArraySetRGBA (AtArray* a, uint32_t i, AtRGBA val);
AI_API bool AiArraySetVec2 (AtArray* a, uint32_t i, AtVector2 val);
AI_API bool AiArraySetVec  (AtArray* a, uint32_t i, AtVector val);
AI_API bool AiArraySetMtx  (AtArray* a, uint32_t i, AtMatrix val);
AI_API bool AiArraySetStr  (AtArray* a, uint32_t i, AtString val);
AI_API bool AiArraySetPtr  (AtArray* a, uint32_t i, void* val);
AI_API bool AiArraySetArray(AtArray* a, uint32_t i, AtArray* val);
/*\}*/

/*\}*/

#ifdef AI_CPU_COMPILER
// this is slower than the AtString version
inline bool AiArraySetStr(AtArray* a, uint32_t i, const char* val)
{
   return AiArraySetStr(a, i, AtString(val));
}
#endif

// Helper functions for compilers that warn about trivial objects being passed
// as variadic args:

// do not use these directly.
struct POD_tempf2{float f[2];};
struct POD_tempf3{float f[3];};
struct POD_tempf4{float f[4];};

inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector v1) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector v1, AtVector v2) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector v1, AtVector v2, AtVector v3) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector v1, AtVector v2, AtVector v3, AtVector v4) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3), reinterpret_type<POD_tempf3>(v4));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector v1, AtVector v2, AtVector v3, AtVector v4, AtVector v5) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3), reinterpret_type<POD_tempf3>(v4), reinterpret_type<POD_tempf3>(v5));
}

inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector2 v1) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf2>(v1));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector2 v1, AtVector2 v2) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf2>(v1), reinterpret_type<POD_tempf2>(v2));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector2 v1, AtVector2 v2, AtVector2 v3) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf2>(v1), reinterpret_type<POD_tempf2>(v2), reinterpret_type<POD_tempf2>(v3));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector2 v1, AtVector2 v2, AtVector2 v3, AtVector2 v4) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf2>(v1), reinterpret_type<POD_tempf2>(v2), reinterpret_type<POD_tempf2>(v3), reinterpret_type<POD_tempf2>(v4));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtVector2 v1, AtVector2 v2, AtVector2 v3, AtVector2 v4, AtVector2 v5) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf2>(v1), reinterpret_type<POD_tempf2>(v2), reinterpret_type<POD_tempf2>(v3), reinterpret_type<POD_tempf2>(v4), reinterpret_type<POD_tempf2>(v5));
}

inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGB v1) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGB v1, AtRGB v2) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGB v1, AtRGB v2, AtRGB v3) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGB v1, AtRGB v2, AtRGB v3, AtRGB v4) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3), reinterpret_type<POD_tempf3>(v4));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGB v1, AtRGB v2, AtRGB v3, AtRGB v4, AtRGB v5) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf3>(v1), reinterpret_type<POD_tempf3>(v2), reinterpret_type<POD_tempf3>(v3), reinterpret_type<POD_tempf3>(v4), reinterpret_type<POD_tempf3>(v5));
}

inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGBA v1) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf4>(v1));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGBA v1, AtRGBA v2) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf4>(v1), reinterpret_type<POD_tempf4>(v2));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGBA v1, AtRGBA v2, AtRGBA v3) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf4>(v1), reinterpret_type<POD_tempf4>(v2), reinterpret_type<POD_tempf4>(v3));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGBA v1, AtRGBA v2, AtRGBA v3, AtRGBA v4) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf4>(v1), reinterpret_type<POD_tempf4>(v2), reinterpret_type<POD_tempf4>(v3), reinterpret_type<POD_tempf4>(v4));
}
inline AtArray* AiArray(uint32_t nelements, uint8_t nkeys, int type, AtRGBA v1, AtRGBA v2, AtRGBA v3, AtRGBA v4, AtRGBA v5) {
   return AiArray(nelements, nkeys, type, reinterpret_type<POD_tempf4>(v1), reinterpret_type<POD_tempf4>(v2), reinterpret_type<POD_tempf4>(v3), reinterpret_type<POD_tempf4>(v4), reinterpret_type<POD_tempf4>(v5));
}
