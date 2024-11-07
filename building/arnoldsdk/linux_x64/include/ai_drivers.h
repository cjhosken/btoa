// Copyright 2022 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing AOV driver nodes
 */

#pragma once
#include "ai_nodes.h"
#include "ai_api.h"
#include "ai_bbox.h"
#include "ai_output_iterator.h"
#include <stdint.h> // uint32_t etc

// forward declaration
struct AtOutputIterator;
struct AtAOVSampleIterator;

/** \defgroup ai_drivers Output Driver Nodes
 *
 *  Construction and manipulation of driver nodes.
 * 
 *  \details
 *  Arnold supports pluggable output-file writers called "drivers".
 *  This output driver mechanism provides a pluggable architecture for
 *  writing output image files using Arnold's built-in AOV pipeline.
 *  It is also possible to write to arbitrary devices, such as a window
 *  display.
 *
 *  AOVs (Arbitrary Output Values) are organized into "layers", with each
 *  layer having a particular type (such as FLOAT or RGBA).
 *
 *  Drivers receive AOVs one bucket at a time which is perfectly
 *  suited to image-formats that are tiled.  An iterator allows the
 *  driver to iterate through all the AOV layers contained in the
 *  bucket.
 *
 * \{
 */

/** Driver Node methods structure */
struct AtDriverNodeMethods {
   bool         (*DriverSupportsPixelType)(const AtNode*, uint8_t);
   const char** (*DriverExtension)();
   void         (*DriverOpen)(AtNode*, struct AtOutputIterator*, AtBBox2, AtBBox2, int);
   bool         (*DriverNeedsBucket)(AtNode*, int, int, int, int, uint16_t);
   void         (*DriverPrepareBucket)(AtNode*, int, int, int, int, uint16_t);
   void         (*DriverProcessBucket)(AtNode*, struct AtOutputIterator*, struct AtAOVSampleIterator*, int, int, int, int, uint16_t);
   void         (*DriverWriteBucket)(AtNode*, struct AtOutputIterator*, struct AtAOVSampleIterator*, int, int, int, int);
   void         (*DriverClose)(AtNode*, struct AtOutputIterator*);
};

/** Output Driver node methods exporter */
#define AI_DRIVER_NODE_EXPORT_METHODS(tag)         \
AI_INSTANCE_COMMON_METHODS                         \
driver_supports_pixel_type;                        \
driver_extension;                                  \
driver_open;                                       \
driver_needs_bucket;                               \
driver_prepare_bucket;                             \
driver_process_bucket;                             \
driver_write_bucket;                               \
driver_close;                                      \
static AtDriverNodeMethods ai_driver_mtds = {      \
   DriverSupportsPixelType,                        \
   DriverExtension,                                \
   DriverOpen,                                     \
   DriverNeedsBucket,                              \
   DriverPrepareBucket,                            \
   DriverProcessBucket,                            \
   DriverWriteBucket,                              \
   DriverClose,                                    \
};                                                 \
static AtNodeMethods ai_node_mtds = {              \
   &ai_common_mtds,                                \
   &ai_driver_mtds                                 \
};                                                 \
const AtNodeMethods *tag = &ai_node_mtds;

/**
 * \name Node Method Declarations
 * \{
 */

/** Driver's driver_supports_pixel_type declaration
 *
 *  Can the driver handle buckets of pixels of the specified type? This function
 *  is not called for raw mode drivers.
 *
 *  \return true if the driver can write pixels of the given type
 */
#define driver_supports_pixel_type \
static bool DriverSupportsPixelType(const AtNode* node, uint8_t pixel_type)

/** Driver's driver_extension method declaration
 *
 * If the extension is empty (returned array is {NULL} then arnold will assume
 * the driver could be a "view" type driver as opposed to just a file writing
 * driver. Both view and file drivers will apply imagers at the end of the
 * render, but view drivers will also apply imagers during rendering so that
 * there is a quicker preview of what the final image will look like. This
 * extra imager processing can slow the render, so view drivers have the option
 * of returning an arbitrary extension so that the faster code path is used.
 *
 *  \return  a NULL-terminated array of filename extensions which this driver
 *           is capable of writing.  For example, a 'jpeg' driver might return
 *           the following array:  { "jpeg", "jpg", NULL }
 */
#define driver_extension \
static const char** DriverExtension()

/** Driver's driver_open method declaration
 *
 * This function is called before rendering starts and can make any preparations
 * the driver needs, like opening a file or allocating memory. The list of connected
 * outputs is passed in using an output iterator.
 *
 * \param node             pointer to the driver node itself
 * \param iterator         output iterator for outputs connected to this driver
 * \param display_window   this is a 2D bounding box for the actual resolution
 * \param data_window      this is the actual region of pixels that will be rendered
 * \param bucket_size      maximum width in pixels of a bucket
 */
#define driver_open \
static void DriverOpen(AtNode* node, struct AtOutputIterator* iterator, AtBBox2 display_window, AtBBox2 data_window, int bucket_size)

/** Driver's driver_needs_bucket method declaration
 *
 * This function is called to determine if a bucket will be rendered. It can be used
 * to continue work on partial images without re-rendering already present buckets.
 *
 * \param node             pointer to the driver node itself
 * \param bucket_xo        x coordinate of the bucket (upper-left)
 * \param bucket_yo        y coordinate of the bucket (upper-left)
 * \param bucket_size_x    width of the bucket in pixels
 * \param bucket_size_y    height of the bucket in pixels
 * \param tid              thread ID that will render this bucket
 *
 *  \return                true if the bucket needs to be rendered,
 *                         false if the bucket can be skipped
 */
#define driver_needs_bucket \
static bool DriverNeedsBucket(AtNode* node, int bucket_xo, int bucket_yo, int bucket_size_x, int bucket_size_y, uint16_t tid)

/** Driver's driver_prepare_bucket method declaration
 *
 * This function is called before a bucket is rendered. It can be used to display
 * bucket corners for interactive rendering drivers to show which buckets are being
 * processed, for example. The renderer locks around this function so the contained
 * code is not required to be thread safe. The bucket size may be smaller than what
 * was given to \c driver_open because buckets are clamped to the edge of the render
 * region.
 *
 * \param node             pointer to the driver node itself
 * \param bucket_xo        x coordinate of the bucket (upper-left)
 * \param bucket_yo        y coordinate of the bucket (upper-left)
 * \param bucket_size_x    width of the bucket in pixels
 * \param bucket_size_y    height of the bucket in pixels
 * \param tid              thread ID that will render this bucket
 */
#define driver_prepare_bucket \
static void DriverPrepareBucket(AtNode* node, int bucket_xo, int bucket_yo, int bucket_size_x, int bucket_size_y, uint16_t tid)

/** Driver's driver_process_bucket method declaration
 *
 * This function is called after a bucket has been rendered, but before it is written out.
 * It provides the rendered pixels of each output to the driver, or the raw AOV samples if
 * this is a raw driver. The renderer does not lock around this function, to allow for
 * lengthy bucket preprocessing to happen in parallel. The contained code should not require
 * any thread synchornization. The bucket size may be smaller than what was given to
 * \c driver_open because buckets are clamped to the edge of the render region.
 *
 * \param node             pointer to the driver node itself
 * \param iterator         output iterator (loops over connected outputs for regular drivers)
 * \param sample_iterator  raw AOV sample iterator (loops over connected AOVs for raw drivers)
 * \param bucket_xo        x coordinate of the bucket (upper-left)
 * \param bucket_yo        y coordinate of the bucket (upper-left)
 * \param bucket_size_x    width of the bucket in pixels
 * \param bucket_size_y    height of the bucket in pixels
 * \param tid              thread ID that rendered this bucket
 */
#define driver_process_bucket \
static void DriverProcessBucket(AtNode* node, struct AtOutputIterator* iterator, struct AtAOVSampleIterator* sample_iterator, int bucket_xo, int bucket_yo, int bucket_size_x, int bucket_size_y, uint16_t tid)

/** Driver's driver_write_bucket method declaration
 *
 * This function is called after a bucket has been rendered. It provides the rendered
 * pixels of each output to the driver, or the raw AOV samples if this is a raw driver.
 * The renderer locks around this function so the contained code is not required to
 * be thread safe. The bucket size may be smaller than what was given to \c driver_open
 * because buckets are clamped to the edge of the render region.
 *
 * \param node             pointer to the driver node itself
 * \param iterator         output iterator (loops over connected outputs for regular drivers)
 * \param sample_iterator  raw AOV sample iterator (loops over connected AOVs for raw drivers)
 * \param bucket_xo        x coordinate of the bucket (upper-left)
 * \param bucket_yo        y coordinate of the bucket (upper-left)
 * \param bucket_size_x    width of the bucket in pixels
 * \param bucket_size_y    height of the bucket in pixels
 */
#define driver_write_bucket \
static void DriverWriteBucket(AtNode* node, struct AtOutputIterator* iterator, struct AtAOVSampleIterator* sample_iterator, int bucket_xo, int bucket_yo, int bucket_size_x, int bucket_size_y)

/** Driver's driver_close method declaration
 *
 * This function is called after the image has finished rendering. It is responsible
 * for any final tasks such as flushing or closing open files.
 *
 * \param node             pointer to the driver node itself
 * \param iterator         output iterator (loops over connected outputs for regular drivers)
 */
#define driver_close \
static void DriverClose(AtNode* node, struct AtOutputIterator* iterator)
/* \}*/

/**
 * \name API for Driver Writers
 * \{
 */

AI_API void         AiDriverInitialize(AtNode* node, bool supports_multiple_outputs);
AI_API void         AiRawDriverInitialize(AtNode* node, const char** required_aovs, bool requires_depth);
AI_API void         AiDriverGetMatrices(AtMatrix& world_to_camera, AtMatrix& world_to_screen);
AI_API const char** AiDriverExtension(const AtNodeEntry* node_entry);

AI_API const AtNodeEntry* AiFindDriverType(const char* extension);

/* \}*/

/*\}*/
