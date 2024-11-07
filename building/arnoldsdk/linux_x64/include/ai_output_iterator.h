// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * AtOutputIterator type and methods
 */

#pragma once
#include "ai_string.h"

// forward declarations
struct AtNode;

/** \defgroup ai_output_iterator AtOutputIterator API
 *
 *  \ref AtOutputIterator methods.
 *
 *  \details
 *  Arnold \ref AtOutputIterator structure is used to iterate over a group of output
 *  and provide information regarding each output.
 * \{
 */

/**
 * \struct AtOutputIterator
 *
 * This represents an iterator that is used to iterate over group of ouputs in Arnold.
 */
struct AtOutputIterator;

/**
 * \name AtOutputIterator Methods
 * \{
 */
AI_API bool         AiOutputIteratorGetNext(struct AtOutputIterator* iter, AtString* output_name, int* pixel_type, const void** bucket_data);
AI_API void         AiOutputIteratorReset(struct AtOutputIterator* iter);
AI_API AtNode*      AiOutputIteratorGetFilter(struct AtOutputIterator* iter);
AI_API bool         AiOutputIteratorIsHalf(struct AtOutputIterator* iter);
AI_API AtString     AiOutputIteratorGetLayerName(struct AtOutputIterator* iter);
AI_API AtNode*      AiOutputIteratorGetCamera(struct AtOutputIterator* iter);
/* \}*/
/*\}*/
