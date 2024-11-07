// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Node parameters
 */

#pragma once
#include "ai_array.h"
#include "ai_closure.h"
#include "ai_color.h"
#include "ai_enum.h"
#include "ai_math.h"
#include "ai_matrix.h"
#include "ai_vector.h"
#include "ai_api.h"
#include <stdint.h> // uint32_t etc

#ifdef _WIN32
#  ifndef WIN32_LEAN_AND_MEAN
#    define WIN32_LEAN_AND_MEAN
#  endif
#  ifndef VC_EXTRALEAN
#    define VC_EXTRALEAN
#  endif
#  ifndef NOMINMAX
#    define NOMINMAX
#  endif
// Force an include of windows.h to make sure it can't be included after this header
// (thanks to its own internal include guard) and the RGB() macro is not defined again
#  include <windows.h>
#  ifdef RGB
#    undef RGB
// The RGB() macro in WinGDI.h returns a COLORREF, which we know to be a DWORD, which
// in turn is an unsigned long, see:
// https://msdn.microsoft.com/en-us/library/windows/desktop/aa383751%28v=vs.85%29.aspx
// Let's recreate this as a function instead of as a macro.
inline constexpr unsigned long RGB(unsigned long r, unsigned long g, unsigned long b)
{
   return r | g << 8 | b << 16;
}
#  endif
#endif

// forward declaration
struct AtList;
struct AtNode;

/** \defgroup ai_params AtParamEntry API
 *  
 *  Querying and operation with node parameters.
 * 
 *  \details
 *  Methods like \ref AiNodeEntryGetParameter() return a \ref AtParamEntry object
 *  that can be used to query information about a given parameter.
 *  For a discussion of Arnold's object-oriented system of pluggable nodes, please
 *  refer to \ref ai_nodes and \ref ai_node_entry.
 * \{
 */ 

/** \name Parameter Types
 *
 *  See AtParamValue for the actual primitive data types that these macros refer to.
 * \{
 */
#define AI_TYPE_BYTE          0x00  /**< uint8_t (an 8-bit sized unsigned integer) */
#define AI_TYPE_INT           0x01  /**< int (32-bit integer)*/
#define AI_TYPE_UINT          0x02  /**< unsigned int (32-bit unsigned integer)*/
#define AI_TYPE_BOOLEAN       0x03  /**< bool (either true or false) */
#define AI_TYPE_FLOAT         0x04  /**< float (Single-precision floating point number) */
#define AI_TYPE_RGB           0x05  /**< RGB struct */
#define AI_TYPE_RGBA          0x06  /**< RGBA struct */
#define AI_TYPE_VECTOR        0x07  /**< XYZ vector or point */
#define AI_TYPE_VECTOR2       0x09  /**< XY vector or point */
#define AI_TYPE_STRING        0x0A  /**< AtString character string */
#define AI_TYPE_POINTER       0x0B  /**< Arbitrary pointer */
#define AI_TYPE_NODE          0x0C  /**< Pointer to an Arnold node */
#define AI_TYPE_ARRAY         0x0D  /**< AtArray */
#define AI_TYPE_MATRIX        0x0E  /**< 4x4 matrix */
#define AI_TYPE_ENUM          0x0F  /**< Enumeration (see \ref AtEnum) */
#define AI_TYPE_CLOSURE       0x10  /**< Shader closure */
#define AI_TYPE_USHORT        0x11  /**< unsigned short (16-bit unsigned integer) (used by drivers only) */
#define AI_TYPE_HALF          0x12  /**< 16-bit, half-precision float (used by drivers only) */
#define AI_TYPE_UNDEFINED     0xFF  /**< Undefined, you should never encounter a parameter of this type */
#define AI_TYPE_NONE          0xFF  /**< No type */
/* \}*/

/** \name Parameter Categories for User-Data
 * \{
 */
#define AI_USERDEF_UNDEFINED  0     /**< Undefined, you should never encounter a parameter of this category */
#define AI_USERDEF_CONSTANT   1     /**< User-defined: per-object parameter */
#define AI_USERDEF_UNIFORM    2     /**< User-defined: per-face parameter */
#define AI_USERDEF_VARYING    3     /**< User-defined: per-vertex parameter */
#define AI_USERDEF_INDEXED    4     /**< User-defined: per-face-vertex parameter */
/* \}*/

/**
 * Actual parameter value for each supported type
 */
class AtParamValue
{
public:
   AI_DEVICE bool          const& BOOL()    const{ return *reinterpret_type<bool      const*> (&data); }
   AI_DEVICE uint8_t       const& BYTE()    const{ return *reinterpret_type<uint8_t   const*> (&data); }
   AI_DEVICE int           const& INT()     const{ return *reinterpret_type<int       const*> (&data); }
   AI_DEVICE unsigned      const& UINT()    const{ return *reinterpret_type<unsigned  const*> (&data); }
   AI_DEVICE float         const& FLT()     const{ return *reinterpret_type<float     const*> (&data); }
   AI_DEVICE AtRGB         const& RGB()     const{ return *reinterpret_type<AtRGB     const*> (&data); }
   AI_DEVICE AtRGBA        const& RGBA()    const{ return *reinterpret_type<AtRGBA    const*> (&data); }
   AI_DEVICE AtVector      const& VEC()     const{ return *reinterpret_type<AtVector  const*> (&data); }
   AI_DEVICE AtVector2     const& VEC2()    const{ return *reinterpret_type<AtVector2 const*> (&data); }
   AI_DEVICE AtString      const& STR()     const{ return *reinterpret_type<AtString  const*> (&data); }
   AI_DEVICE void*         const& PTR()     const{ return *reinterpret_type<void*     const*> (&data); }
   AtMatrix*     const& pMTX()    const{ return *reinterpret_type<AtMatrix* const*> (&data); }
   AtArray*      const& ARRAY()   const{ return *reinterpret_type<AtArray*  const*> (&data); }
   AI_DEVICE AtClosureList const& CLOSURE() const{ return *reinterpret_type<AtClosureList const*>(&data); }

   AI_DEVICE bool          & BOOL()   { return *reinterpret_type<bool     *>    (&data); }
   AI_DEVICE uint8_t       & BYTE()   { return *reinterpret_type<uint8_t  *>    (&data); }
   AI_DEVICE int           & INT()    { return *reinterpret_type<int      *>    (&data); }
   AI_DEVICE unsigned      & UINT()   { return *reinterpret_type<unsigned *>    (&data); }
   AI_DEVICE float         & FLT()    { return *reinterpret_type<float    *>    (&data); }
   AI_DEVICE AtRGB         & RGB()    { return *reinterpret_type<AtRGB    *>    (&data); }
   AI_DEVICE AtRGBA        & RGBA()   { return *reinterpret_type<AtRGBA   *>    (&data); }
   AI_DEVICE AtVector      & VEC()    { return *reinterpret_type<AtVector *>    (&data); }
   AI_DEVICE AtVector2     & VEC2()   { return *reinterpret_type<AtVector2*>    (&data); }
   AI_DEVICE AtString      & STR()    { return *reinterpret_type<AtString *>    (&data); }
   AI_DEVICE void*         & PTR()    { return *reinterpret_type<void*    *>    (&data); }
   AtMatrix*     & pMTX()   { return *reinterpret_type<AtMatrix**>    (&data); }
   AtArray*      & ARRAY()  { return *reinterpret_type<AtArray* *>    (&data); }
   AI_DEVICE AtClosureList & CLOSURE(){ return *reinterpret_type<AtClosureList*>(&data); }

private:
   // 128 bits of raw data, naturally aligned to 64 bit so it properly works
   // with pointers.  This is big enough to hold up to four floats, as needed
   // by AtRGBA.
   uint64_t data[2];
};

/**
 * This represents a parameter of a given node type in Arnold.
 *
 * This holds details like the name, type and default value. The actual
 * contents of this struct are private. 
 */
struct AtParamEntry;

/**
 * \name AtParamEntry Methods
 * \{
 */
AI_API AI_PURE  AtString            AiParamGetName    (const AtParamEntry* pentry);
AI_API AI_PURE  uint8_t             AiParamGetType    (const AtParamEntry* pentry);
AI_API AI_PURE  uint8_t             AiParamGetSubType (const AtParamEntry* pentry);
AI_API AI_PURE  const AtParamValue* AiParamGetDefault (const AtParamEntry* pentry);
AI_API AI_PURE  AtEnum              AiParamGetEnum    (const AtParamEntry* pentry);
AI_API AI_PURE  const char*         AiParamGetTypeName(uint8_t type);
AI_API AI_DEVICE AI_CONST int       AiParamGetTypeSize(uint8_t type);
/* \}*/

/**
 * This represents a user-declared parameter in Arnold (user-data).
 *
 * This holds details like name, type, and category.  The actual
 * contents of this struct are private.
 */
struct AtUserParamEntry;

/**
 * \name AtUserParamEntry Methods
 * \{
 */
AI_API AI_DEVICE AI_PURE  const char* AiUserParamGetName     (const AtUserParamEntry* upentry);
AI_API AI_DEVICE AI_PURE  uint8_t     AiUserParamGetType     (const AtUserParamEntry* upentry);
AI_API AI_DEVICE AI_PURE  uint8_t     AiUserParamGetArrayType(const AtUserParamEntry* upentry);
AI_API AI_DEVICE AI_PURE  uint8_t     AiUserParamGetCategory (const AtUserParamEntry* upentry);
/* \}*/

/**
 * Returns whether an AtParamValue of type src_type can be converted to
 * dst_type.
 *
 * For instance, \c AiParamTypeConvertible(AI_TYPE_FLOAT, AI_TYPE_INT)
 * would return true since an AtParamValue containing an int can be converted
 * into an AtParamValue containing a float.
 *
 * \param  dst_type  type of the destination value
 * \param  src_type  type of the source value
 */
AI_API AI_CONST bool AiParamTypeConvertible(uint8_t dst_type, uint8_t src_type);

/**
 * \name Parameter Installers
 * These macros are to be called from a node's \c node_parameters method only.
 *
 * There is a different macro for each supported parameter data type. For example,
 * a shader node that implemented a typical fractal noise would declare three
 * parameters like this:
 * \code
 * node_parameters
 * {
 *    AiParameterInt("octaves", 3);
 *    AiParameterFlt("lacunarity", 1.92f);
 *    AiParameterBool("turbulence", false);
 * }
 * \endcode 
 *
 * Please refer to ai_params.h for a description of the functions called by
 * these macros. 
 *
 * \param n         the name of the parameter that will be installed 
 * \param default   the default value of the new parameter (the actual number
 *                  of arguments passed in depends on the parameter's data type,
 *                  for example three floats for a RGB type)
 * \{
 */
#define AiParameterByte(n,c)       AiNodeParamByte   (params,-1,n,c);
#define AiParameterInt(n,c)        AiNodeParamInt    (params,-1,n,c);
#define AiParameterUInt(n,c)       AiNodeParamUInt   (params,-1,n,c);
#define AiParameterBool(n,c)       AiNodeParamBool   (params,-1,n,c);
#define AiParameterFlt(n,c)        AiNodeParamFlt    (params,-1,n,c);
#define AiParameterRGB(n,r,g,b)    AiNodeParamRGB    (params,-1,n,r,g,b);
#define AiParameterRGBA(n,r,g,b,a) AiNodeParamRGBA   (params,-1,n,r,g,b,a);
#define AiParameterVec(n,x,y,z)    AiNodeParamVec    (params,-1,n,x,y,z);
#define AiParameterVec2(n,x,y)     AiNodeParamVec2   (params,-1,n,x,y);
#define AiParameterStr(n,c)        AiNodeParamStr    (params,-1,n,c);
#define AiParameterPtr(n,c)        AiNodeParamPtr    (params,-1,n,c);
#define AiParameterNode(n,c)       AiNodeParamNode   (params,-1,n,c);
#define AiParameterArray(n,c)      AiNodeParamArray  (params,-1,n,c);
#define AiParameterMtx(n,c)        AiNodeParamMtx    (params,-1,n,c);
#define AiParameterEnum(n,c,e)     AiNodeParamEnum   (params,-1,n,c,e);
#define AiParameterClosure(n)      AiNodeParamClosure(params,-1,n);

#define AiOutputByte(n)            AiNodeOutputByte   (params,n);
#define AiOutputInt(n)             AiNodeOutputInt    (params,n);
#define AiOutputUInt(n)            AiNodeOutputUInt   (params,n);
#define AiOutputBool(n)            AiNodeOutputBool   (params,n);
#define AiOutputFlt(n)             AiNodeOutputFlt    (params,n);
#define AiOutputRGB(n)             AiNodeOutputRGB    (params,n);
#define AiOutputRGBA(n)            AiNodeOutputRGBA   (params,n);
#define AiOutputVec(n)             AiNodeOutputVec    (params,n);
#define AiOutputVec2(n)            AiNodeOutputVec2   (params,n);
#define AiOutputStr(n)             AiNodeOutputStr    (params,n);
#define AiOutputPtr(n)             AiNodeOutputPtr    (params,n);
#define AiOutputNode(n)            AiNodeOutputNode   (params,n);
#define AiOutputArray(n,t)         AiNodeOutputArray  (params,n,t);
#define AiOutputMtx(n)             AiNodeOutputMtx    (params,n);
#define AiOutputEnum(n,t)          AiNodeOutputEnum   (params,n,t);
#define AiOutputClosure(n)         AiNodeOutputClosure(params,n);
/* \}*/

/*\}*/

/* for convenience, the macros above call these functions */
AI_API void  AiNodeParamByte   (AtList* params, int varoffset, const char* pname, uint8_t pdefault);
AI_API void  AiNodeParamInt    (AtList* params, int varoffset, const char* pname, int pdefault);
AI_API void  AiNodeParamUInt   (AtList* params, int varoffset, const char* pname, unsigned int pdefault);
AI_API void  AiNodeParamBool   (AtList* params, int varoffset, const char* pname, bool pdefault);
AI_API void  AiNodeParamFlt    (AtList* params, int varoffset, const char* pname, float pdefault);
AI_API void  AiNodeParamRGB    (AtList* params, int varoffset, const char* pname, float r, float g, float b);
AI_API void  AiNodeParamRGBA   (AtList* params, int varoffset, const char* pname, float r, float g, float b, float a);
AI_API void  AiNodeParamVec    (AtList* params, int varoffset, const char* pname, float x, float y, float z);
AI_API void  AiNodeParamVec2   (AtList* params, int varoffset, const char* pname, float x, float y);
AI_API void  AiNodeParamStr    (AtList* params, int varoffset, const char* pname, const char* pdefault);
AI_API void  AiNodeParamPtr    (AtList* params, int varoffset, const char* pname, void* pdefault);
AI_API void  AiNodeParamNode   (AtList* params, int varoffset, const char* pname, AtNode* pdefault);
AI_API void  AiNodeParamArray  (AtList* params, int varoffset, const char* pname, AtArray* pdefault);
AI_API void  AiNodeParamMtx    (AtList* params, int varoffset, const char* pname, AtMatrix matrix);
AI_API void  AiNodeParamEnum   (AtList* params, int varoffset, const char* pname, int pdefault, AtEnum enum_type);
AI_API void  AiNodeParamClosure(AtList* params, int varoffset, const char* pname);

AI_API void  AiNodeOutputByte   (AtList* params, const char* pname);
AI_API void  AiNodeOutputInt    (AtList* params, const char* pname);
AI_API void  AiNodeOutputUInt   (AtList* params, const char* pname);
AI_API void  AiNodeOutputBool   (AtList* params, const char* pname);
AI_API void  AiNodeOutputFlt    (AtList* params, const char* pname);
AI_API void  AiNodeOutputRGB    (AtList* params, const char* pname);
AI_API void  AiNodeOutputRGBA   (AtList* params, const char* pname);
AI_API void  AiNodeOutputVec    (AtList* params, const char* pname);
AI_API void  AiNodeOutputVec2   (AtList* params, const char* pname);
AI_API void  AiNodeOutputStr    (AtList* params, const char* pname);
AI_API void  AiNodeOutputPtr    (AtList* params, const char* pname);
AI_API void  AiNodeOutputNode   (AtList* params, const char* pname);
AI_API void  AiNodeOutputArray  (AtList* params, const char* pname, int array_type);
AI_API void  AiNodeOutputMtx    (AtList* params, const char* pname);
AI_API void  AiNodeOutputEnum   (AtList* params, const char* pname, AtEnum enum_type);
AI_API void  AiNodeOutputClosure(AtList* params, const char* pname);
