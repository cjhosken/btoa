// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Global entry point to the scene graph elements (options, camera, lights, etc)
 */

#pragma once
#include "ai_bbox.h"
#include "ai_api.h"
#include "ai_node_entry.h"
#include "ai_string.h"
#include <stdint.h> // uint32_t etc

// forward declares
struct AtNode;
struct AtNodeIterator;
struct AtNodeEntry;
struct AtNodeEntryIterator;
struct AtAOVIterator;
struct AtParamValueMap;
class AtRenderSession;

/**
 * \struct AtAOVEntry
 * 
 * This helper struct is used to return information from the AOV iterator.
 */
struct AtAOVEntry
{
   AtString name;        /**< AOV name                       */
   uint8_t  type;        /**< Data type                      */
   int      blend_mode;  /**< Blend mode                     */
   AtString expression;  /**< Optional light path expression */
};

/** \defgroup ai_universe AtUniverse API
 *
 * Construction and manipulation of \ref AtUniverse objects.
 * 
 * \details
 * There is always a default universe, created on \ref AiBegin() and destroyed on \ref
 * AiEnd(). This universe cannot be manually destroyed. As a shortcut, universe API calls
 * can use a null universe pointer to refer to this default universe.
 * 
 * There can also be a number of secondary universes created using \ref AiUniverse(), which 
 * can be used for scene import, export and rendering independently from other universes
 * and the default universe.
 * 
 * Note that universes are totally independent, so a node can only belong to a single
 * universe, and it cannot link to or reference nodes in a different universe.
 * \{                                                                              
 */       

/**
 * \struct AtUniverse
 * 
 * This represents a universe in Arnold.
 * 
 * \see AiUniverse
 */
class AtUniverse;

/** \name Methods
 * \{
 */
#ifdef AI_CPU_COMPILER
AI_API         AtUniverse*          AiUniverse();
AI_API         void                 AiUniverseDestroy(AtUniverse* universe);
AI_API         bool                 AiUniverseCacheFlush(AtUniverse* universe, int cache_flags);
AI_API AI_PURE AtNode*              AiUniverseGetOptions(const AtUniverse* universe);
#endif // AI_CPU_COMPILER
AI_API AI_DEVICE AI_PURE AtNode*    AiUniverseGetCamera(const AtUniverse* universe);
#ifdef AI_CPU_COMPILER
AI_API AI_PURE AtBBox               AiUniverseGetSceneBounds(const AtUniverse* universe);
AI_API         AtNodeIterator*      AiUniverseGetNodeIterator(const AtUniverse* universe, unsigned int node_mask);
AI_API         AtNodeEntryIterator* AiUniverseGetNodeEntryIterator(unsigned int node_mask);
AI_API         AtAOVIterator*       AiUniverseGetAOVIterator(const AtUniverse* universe);
AI_API         void                 AiUniverseAddDefaultNodes(AtUniverse* universe, const AtParamValueMap* params);
AI_API         AtRenderSession*     AiUniverseGetRenderSession(const AtUniverse* universe);
AI_API         bool                 AiUniverseCompare(const AtUniverse* universe1, const AtUniverse* universe2, unsigned int node_mask = AI_NODE_ALL, AtParamValueMap* diffs = NULL);
AI_API         uint32_t             AiUniverseGetId(const AtUniverse* universe);
AI_API         AtUniverse*          AiUniverseGetFromId(uint32_t universe_id);

/** \name Node Iterator API
 * \{
 */
AI_API         void    AiNodeIteratorDestroy(AtNodeIterator* iter);
AI_API         AtNode* AiNodeIteratorGetNext(AtNodeIterator* iter);
AI_API AI_PURE bool    AiNodeIteratorFinished(const AtNodeIterator* iter);
/*\}*/

/** \name Node Entry Iterator API
 * \{
 */
AI_API         void         AiNodeEntryIteratorDestroy(AtNodeEntryIterator* iter);
AI_API         AtNodeEntry* AiNodeEntryIteratorGetNext(AtNodeEntryIterator* iter);
AI_API AI_PURE bool         AiNodeEntryIteratorFinished(const AtNodeEntryIterator* iter);
/*\}*/

/** \name AOV Iterator API
 * \{
 */
AI_API         void              AiAOVIteratorDestroy(AtAOVIterator* iter);
AI_API         const AtAOVEntry* AiAOVIteratorGetNext(AtAOVIterator* iter);
AI_API AI_PURE bool              AiAOVIteratorFinished(const AtAOVIterator* iter);
#endif // AI_CPU_COMPILER
/*\}*/

/** \name Cache Types
 * \{
 */
#define AI_CACHE_TEXTURE        0x0001  /**< Flushes all texturemaps */
#define AI_CACHE_BACKGROUND     0x0002  /**< Flushes all skydome importance tables for background */
#define AI_CACHE_QUAD           0x0004  /**< Flushes all quad lights importance tables */
#define AI_CACHE_VOLUME_DISPLAY 0x0008  /**< Flushes all volume viewport display data */
#define AI_CACHE_ALL            (AI_CACHE_TEXTURE | AI_CACHE_BACKGROUND | AI_CACHE_QUAD | AI_CACHE_VOLUME_DISPLAY)  /**< Flushes all cache types simultaneously */
/*\}*/

/*\}*/
