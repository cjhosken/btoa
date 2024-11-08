// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Key/Value storage
 */

#pragma once
#include "ai_node_entry.h"
#include "ai_vector.h"
#include "ai_color.h"
#include "ai_api.h"
#include "ai_string.h"
#ifdef AI_CPU_COMPILER

struct AtParamValueMap;
struct AtParamValueMapIterator;

/** \defgroup ai_map AtParamValueMap API
 * \{
 */

/**
 * \name AtParamValueMap Methods
 * \{
 */
AI_API AtParamValueMap*         AiParamValueMap();
AI_API void                     AiParamValueMapDestroy(AtParamValueMap* map);
AI_API AtParamValueMapIterator* AiParamValueMapGetIterator(const AtParamValueMap* map);
AI_API void                     AiParamValueMapMerge(AtParamValueMap* target_map, const AtParamValueMap* src_map);
AI_API AtParamValueMap*         AiParamValueMapClone(const AtParamValueMap* src_map);
/* \}*/

/** \name Value Writing
 *
 * \details
 * These functions allow inserting  key/value pairs into a map.
 *
 * Here is an example:
 * \code
 * AiParamValueMapSetStr(map, AtString("author"), AtString("William Shakespeare"));
 * AiParamValueMapSetFlt(map, AtString("temperature"), 21.0f);
 * \endcode
 *
 *
 * \param map    the map to operate with
 * \param name   the key you want to insert
 * \param value  the value you want to insert
 *
 * \{
 */
#define AiCreateFuncs(_name, _type) \
AI_API void AiParamValueMapSet##_name(AtParamValueMap* map, const AtString name, _type value);

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
AiCreateFuncs(Array,AtArray*)
AiCreateFuncs(Ptr,  void*)
#undef AiCreateFuncs

/*\}*/

/** \name Value Retrieval
 *
 * \details
 * These functions allow client code to retrieve values from a map
 *
 * Following on the example above:
 * \code
 * AtString author;
 * bool success = AiParamValueMapGetStr(map, AtString("author"), &author)
 * if (success)
 *    printf("\nAuthor: %s", author.c_str());
 * \endcode
 *
 * \param map         the map to read from
 * \param name        the key attached to the value you want to get
 * \param[out] value  if the read succeeds, the variable pointed to by \e value
 *                    will be overwritten with the value
 * \return            true when the lookup is succesful
 * \{
 */
#define AiCreateFuncs(_name, _type) \
AI_API bool AiParamValueMapGet##_name(const AtParamValueMap* map, const AtString name, _type* value);

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
AiCreateFuncs(Array,AtArray*)
AiCreateFuncs(Ptr,  void*)
#undef AiCreateFuncs
/*\}*/

struct AtParamValueMapEntry
{
   AtString     name;
   uint8_t      type;
   AtParamValue value;
};

/**
 * \name AtParamValueMap Methods
 * \{
 */
AI_API void                        AiParamValueMapIteratorDestroy(AtParamValueMapIterator* iter);
AI_API const AtParamValueMapEntry* AiParamValueMapIteratorGetNext(AtParamValueMapIterator* iter);
AI_API bool                        AiParamValueMapIteratorFinished(const AtParamValueMapIterator* iter);
/* \}*/

/*\}*/
#endif // AI_CPU_COMPILER
