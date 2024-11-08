// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing pixel-filtering nodes
 */

#pragma once
#include "ai_nodes.h"
#include "ai_vector.h"
#include <stdint.h> // uint32_t etc

// forward declaration
struct AtAOVSampleIterator;

/** \defgroup ai_filters Pixel Sample Filter Nodes
 *
 *  Sample filters creation and operation.
 * 
 *  \details
 *  Arnold has support for pluggable sample filters. The filter will process a
 *  bucket of AOV subsamples and filter them down to a single AOV sample per
 *  pixel.
 *
 *  Filters operate on a "primary" AOV;  this is the AOV which is specified on
 *  the same "outputs" line as where the filter is specified.    However,
 *  filters can also query supporting, or auxiliary, AOVs which can assist in
 *  filtering.  These  are specified when a filter is initialized (see
 *  AiFilterInitialize()).
 *
 * \{
 */

/** Filter Node methods structure */
struct AtFilterNodeMethods {
   uint8_t (*FilterOutputType)(const AtNode*, uint8_t);
   void    (*FilterPixel)(AtNode*, AtAOVSampleIterator*, void*, uint8_t);
};

/** Filter Node methods exporter */
#define AI_FILTER_NODE_EXPORT_METHODS(tag)      \
AI_INSTANCE_COMMON_METHODS                      \
filter_output_type;                             \
filter_pixel;                                   \
static AtFilterNodeMethods ai_filter_mtds = {   \
   FilterOutputType,                            \
   FilterPixel                                  \
};                                              \
static AtNodeMethods ai_node_mtds = {           \
   &ai_common_mtds,                             \
   &ai_filter_mtds                              \
};                                              \
const AtNodeMethods *tag = &ai_node_mtds;

/**
 * \name Node Method Declarations
 * \{
 */

/** Filter's filter_output_type method declaration
 *
 *  This function describes how a pixel sample filter will map a particular
 *  input type to an output type.  For example, if a filter is asked to 
 *  filter an integer AOV, then the filter might decide to convert the 
 *  integers to floats first and then output a float containing the filtered
 *  values.  Most filters' "output" type will match their "input" type.  The
 *  system will use this information to ensure that a filter is only connected
 *  to an output driver which can write the filter's output type.
 * 
 * \param node        The filter node
 * \param input_type  A particular input type (e.g. \c AI_TYPE_RGB, \c AI_TYPE_FLOAT, etc)
 * \return            Returns the output type of this filter for a given input type
 */
#define filter_output_type \
static uint8_t FilterOutputType(const AtNode* node, uint8_t input_type)

/** Filter's filter_pixel method declaration
 * 
 *  This function peforms pixel filtering.  Generally, this function will contain a
 *  loop which iterates over all the samples of the primary AOV which are contained in
 *  this pixel.
 *
 *  \param node      The filter node
 *  \param iterator  An iterator which the filter uses to iterate over all the samples of the
 *                   primary AOV for the current pixel.  The user advances to the next sample
 *                   by calling AiAOVSampleIteratorGetNext().
 *  \param data_out  A pointer to where the filter writes the filtered pixel output.
 *  \param data_type This contains the data-type of the primary AOV.
 */
#define filter_pixel \
static void FilterPixel(AtNode* node, AtAOVSampleIterator* iterator, void* data_out, uint8_t data_type)

/* \}*/

/**
 * \name API Methods for Filter Writers
 * \{
 */
AI_API void AiFilterInitialize(AtNode* node, bool requires_depth, const char** required_aovs);
AI_API void AiFilterUpdate(AtNode* node, float width);
/* \}*/

/**
 * \name API Methods to Loop over Samples
 * \{
 */
AI_API         void      AiAOVSampleIteratorInitPixel(AtAOVSampleIterator* iter, int x, int y);
AI_API         void      AiAOVSampleIteratorGetPixel(AtAOVSampleIterator* iter, int &x, int &y);
AI_API         void      AiAOVSampleIteratorReset(AtAOVSampleIterator* iter);
AI_API         bool      AiAOVSampleIteratorGetNext(AtAOVSampleIterator* iter);
AI_API         bool      AiAOVSampleIteratorGetNextDepth(AtAOVSampleIterator* iter);
AI_API AI_PURE AtVector2 AiAOVSampleIteratorGetOffset(const AtAOVSampleIterator* iter);
AI_API AI_PURE float     AiAOVSampleIteratorGetInvDensity(const AtAOVSampleIterator* iter);
AI_API AI_PURE int       AiAOVSampleIteratorGetDepth(const AtAOVSampleIterator* iter);
AI_API AI_PURE bool      AiAOVSampleIteratorHasValue(const AtAOVSampleIterator* iter);
AI_API AI_PURE bool      AiAOVSampleIteratorHasAOVValue(const AtAOVSampleIterator* iter, AtString name, uint8_t type);
AI_API AI_PURE AtString  AiAOVSampleIteratorGetAOVName(const AtAOVSampleIterator* iter);
/* \}*/

/**
 * \name API Methods to Get Sample Value from Iterator
 * \{
 */
AI_API AI_PURE bool         AiAOVSampleIteratorGetBool  (const AtAOVSampleIterator* iter);
AI_API AI_PURE int          AiAOVSampleIteratorGetInt   (const AtAOVSampleIterator* iter);
AI_API AI_PURE unsigned int AiAOVSampleIteratorGetUInt  (const AtAOVSampleIterator* iter);
AI_API AI_PURE float        AiAOVSampleIteratorGetFlt   (const AtAOVSampleIterator* iter);
AI_API AI_PURE AtRGB        AiAOVSampleIteratorGetRGB   (const AtAOVSampleIterator* iter);
AI_API AI_PURE AtRGBA       AiAOVSampleIteratorGetRGBA  (const AtAOVSampleIterator* iter);
AI_API AI_PURE AtVector     AiAOVSampleIteratorGetVec   (const AtAOVSampleIterator* iter);
AI_API AI_PURE AtVector2    AiAOVSampleIteratorGetVec2  (const AtAOVSampleIterator* iter);
AI_API AI_PURE AtMatrix     AiAOVSampleIteratorGetMatrix(const AtAOVSampleIterator* iter);
AI_API AI_PURE const void*  AiAOVSampleIteratorGetPtr   (const AtAOVSampleIterator* iter);
/* \}*/

/**
 * \name API Methods to Get Sample Value from Iterator for an Arbitrary AOV
 * \{
 */
AI_API AI_PURE bool         AiAOVSampleIteratorGetAOVBool  (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE int          AiAOVSampleIteratorGetAOVInt   (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE unsigned int AiAOVSampleIteratorGetAOVUInt  (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE float        AiAOVSampleIteratorGetAOVFlt   (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE AtRGB        AiAOVSampleIteratorGetAOVRGB   (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE AtRGBA       AiAOVSampleIteratorGetAOVRGBA  (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE AtVector     AiAOVSampleIteratorGetAOVVec   (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE AtVector2    AiAOVSampleIteratorGetAOVVec2  (const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE AtMatrix     AiAOVSampleIteratorGetAOVMatrix(const AtAOVSampleIterator* iter, const AtString name);
AI_API AI_PURE const void*  AiAOVSampleIteratorGetAOVPtr   (const AtAOVSampleIterator* iter, const AtString name);
/* \}*/

/*\}*/
