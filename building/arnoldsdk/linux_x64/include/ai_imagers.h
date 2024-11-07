// Copyright 2022 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing imager nodes
 */

#pragma once
#include "ai_nodes.h"
#include "ai_api.h"
#include "ai_output_iterator.h"
#include <stdint.h> // uint32_t etc

// forward declaration
struct AtOutputIterator;

/** \defgroup ai_imagers Imager Nodes
 *
 *  Construction and manipulation of imager nodes.
 *
 *  \details
 *  Post-processing nodes called imagers operate on pixels before the output
 *  driver. Imagers can be chained together and used to create a variety
 *  of effects on rendered images. Examples include but are not limited to
 *  color management, camera effects such as vignetting or bloom and denoising.
 *
 * \{
 */

enum class AtImagerSchedule { ANY = 0, BUCKET = 1, FULL_FRAME = 2 };

/** Imager Node methods structure */
struct AtImagerNodeMethods {
   void (*ImagerEvaluate)(AtRenderSession*, AtNode*, struct AtOutputIterator*, int, int, int, int, uint16_t);
   void (*ImagerPrepare)(AtRenderSession*, AtNode*, const AtNode*, struct AtOutputIterator*, AtImagerSchedule&);
};

/** Imager node methods exporter */
#define AI_IMAGER_NODE_EXPORT_METHODS(tag)         \
AI_INSTANCE_COMMON_METHODS                         \
imager_evaluate;                                   \
static AtImagerNodeMethods ai_imager_mtds = {      \
   ImagerEvaluate,                                 \
   NULL,                                           \
};                                                 \
static AtNodeMethods ai_node_mtds = {              \
   &ai_common_mtds,                                \
   &ai_imager_mtds                                 \
};                                                 \
const AtNodeMethods *tag = &ai_node_mtds;

/**
 * \name Node Method Declarations
 * \{
 */

/** Imager's imager_prepare method declaration
 *
 * The imager_prepare function will allow the imager to query the outputs that
 * it will process and give the imager an opportunity to request any additional
 * AOVs that may need to be rendered or additional outputs to be written to the
 * driver.
 *
 * \param render_session  render session where this node will be used for rendering
 * \param node            pointer to the imager node
 * \param driver          pointer to the driver node connected to imager stack
 * \param iterator        output iterator (loops over connected outputs)
 * \param schedule        schedule type of the imager (ANY/BUCKET/FULL_FRAME). Default value is ANY.
 */
#define imager_prepare                                                                                                                                         \
static void ImagerPrepare(AtRenderSession* render_session, AtNode* node, const AtNode* driver, struct AtOutputIterator* iterator, AtImagerSchedule& schedule); \
AI_OPTIONAL_METHOD_INSTALL(ai_imager_mtds, ImagerPrepare)                                                                                                      \
static void ImagerPrepare(AtRenderSession* render_session, AtNode* node, const AtNode* driver, struct AtOutputIterator* iterator, AtImagerSchedule& schedule)

/** Imager's imager_evaluate method declaration
 *
 * This function is called after a bucket has been rendered, but before it is
 * passed to the driver. It provides the rendered pixels of each output to the
 * driver. The imager may use this function to make many modification to pixels.
 * The renderer does not lock around this function, to allow for lengthy imager
 * processing to happen in parallel. The contained code should not require any
 * thread synchronization.
 *
 * \param render_session   render session where this node will be used for rendering
 * \param node             pointer to the driver node itself
 * \param iterator         output iterator (loops over connected outputs)
 * \param bucket_xo        x coordinate of the bucket (upper-left)
 * \param bucket_yo        y coordinate of the bucket (upper-left)
 * \param bucket_size_x    width of the bucket in pixels
 * \param bucket_size_y    height of the bucket in pixels
 * \param tid              thread ID that rendered this bucket
 */
#define imager_evaluate \
static void ImagerEvaluate(AtRenderSession* render_session, AtNode* node, struct AtOutputIterator* iterator, int bucket_xo, int bucket_yo, int bucket_size_x, int bucket_size_y, uint16_t tid)
/* \}*/

/**
 * \name API for Imager Writers
 * \{
 */
AI_API bool AiImagerAddInput(AtRenderSession* render_session, const AtNode* imager, const AtNode* driver, int aov_type, AtString aov_name, AtNode* filter);
AI_API bool AiImagerAddOutput(AtRenderSession* render_session, const AtNode* imager, const AtNode* driver, int output_type, AtString output_name);
/* \}*/

/*\}*/
