// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for render statistics output
 */

#pragma once
#include "ai_api.h"
#include "ai_string.h"

#include <stddef.h> // NULL
#include <stdint.h>

/** \defgroup ai_stats Render Statistics API
 * 
 * Render statistics querying and operation.
 * 
 * \{
 */

/**
 * Output mode for structured statistics
 */
enum AtStatsMode
{
   AI_STATS_MODE_OVERWRITE,  /**< Overwrite the file if it exists         */
   AI_STATS_MODE_APPEND      /**< Append data to existing statistics file */
};

AI_API AtStatsMode AiStatsGetMode();
AI_API const char* AiStatsGetFileName();
AI_API void        AiStatsSetMode(AtStatsMode mode);
AI_API void        AiStatsSetFileName(const char* filename);

#ifdef AI_GPU_COMPILER
// profiling does not work on GPU
#define AiProfileBlock(...)
#else
/**
 * Macro to measure total time spent in a code block.  It can be given
 * either a descriptive string literal, an AtNode that should be associated
 * with this measurement, or both.
 *
 * Example usages:
 * \code
 * void foo(AtNode* node)
 * {
 *   AiProfileBlock(node);
 *   // ... do work
 *   while (some_expression)
 *   {
 *       AiProfileBlock("foo worker", node);
 *       // ... do work
 *   }
 * }
 *
 * void bar()
 * {
 *    AiProfileBlock(__func__);
 *    // ... do work
 * }
 * \endcode
 */
#define AiProfileBlock(...) AiProfileBlockRAII Ai_profile_block(__VA_ARGS__)
#endif

/**
 * JSON file to which profiling traces should be written to.  This is written
 * in the Trace Event format which is viewable in Google Chrome at
 * chrome://tracing/ . Setting to NULL will disable output.
 */
AI_API void AiProfileSetFileName(const char* filename);

/**
 * Get the JSON filename to which profiling traces will be written to.
 * \see AiProfileSetFileName()
 */
AI_API AtString AiProfileGetFileName();

/*\}*/


struct AtNode;

/** @private
 * Finalize profile entry
 *
 * \warning Please do not call AiProfileUpdate() directly.
 * \see AiProfileEnd()
 */
AI_API void AiProfileUpdate(uint64_t start_counter, uint64_t end_counter,
                            const char* name, const AtNode* node);

/** @private
 * Get profile counter
 *
 * \warning Please use AiProfileBlock() instead of directly using
 * AiProfileCounter() and AiProfileEnd().
 */
AI_API uint64_t AiProfileCounter();

/** @private
 * Stop profiling
 *
 * \warning Please use AiProfileBlock() instead of directly using
 * AiProfileCounter() and AiProfileEnd().
 */
ARNOLD_FORCEINLINE void AiProfileEnd(uint64_t start_counter, const char* name, const AtNode* node=NULL)
{
   const uint64_t end_counter = AiProfileCounter();
   if (Ai_unlikely(start_counter != end_counter))
      AiProfileUpdate(start_counter, end_counter, name, node);
}

/** @private */
struct AiProfileBlockRAII
{
   AiProfileBlockRAII(const char* name, const AtNode* node=NULL) :
      start_counter(AiProfileCounter()), name(name), node(node) { }

   AiProfileBlockRAII(const AtNode* node) :
      start_counter(AiProfileCounter()), name(NULL), node(node) { }

   ~AiProfileBlockRAII()
   {
      AiProfileEnd(start_counter, name, node);
   }

private:
   const uint64_t start_counter;
   const char* const name;
   const AtNode* const node;
};
