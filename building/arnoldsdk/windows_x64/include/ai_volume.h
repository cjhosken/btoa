// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing volume and implicit surface plugins
 */

#pragma once

#include "ai_bbox.h"
#include "ai_color.h"
#include "ai_params.h"
#include "ai_string.h"
#include "ai_version.h"

// forward declaration
struct AtNode;
struct AtShaderGlobals;

/** \defgroup ai_volumes Volume Plugin API
 *
 * Interaction with custom volumes, implicit surfaces and formats at render time.
 *
 * \details
 * This is accomplished by providing the renderer some
 * callback functions which are called as needed (when the object is hit by a
 * ray).  The plugins are intended to provide tight ray intervals surrounding
 * actual volumetric or implicit surface data, as well as sampling methods for
 * sampling data channels from the volume or implicit surface.
 *
 * Note that the plugins have a thread-locked part: init and cleanup, while
 * the rest of the callbacks may be called concurrently from multiple threads.
 *
 * \{
 */

/** \name Volume interpolation quality
 * \{
 */
#define AI_VOLUME_INTERP_CLOSEST   0   /**< closest data from the volume */
#define AI_VOLUME_INTERP_TRILINEAR 1   /**< trilinearly sampled volume */
#define AI_VOLUME_INTERP_TRICUBIC  2   /**< tricubicly sampled volume */
/* \} */

/**
 * Volume data, as returned by \ref AtVolumeCreate
 */
struct AtVolumeData
{
   void*  private_info;    /**< Volume plugin private data, used how the plugin likes */
   AtBBox bbox;            /**< Bounding box for this volume, plugin is responsible for also including volume_padding from the node */
   float  auto_step_size;  /**< Recommended step size for ray marching through this data */
};

struct AtVolumeIntersectionInfo;

AI_API void AiVolumeAddIntersection(const AtVolumeIntersectionInfo* info, float t0, float t1);
AI_API void AiVolumeMergeIntersection(const AtVolumeIntersectionInfo* info, float t0, float t1, uint32_t prim_id);

/*
 * Volume file querying.
 */
AI_API AtArray* AiVolumeFileGetChannels(const char* filename);
AI_API AtBBox   AiVolumeFileGetBBox(const char* filename, const AtArray* channels);

/**
 * Volume plugin volume creation.
 *
 * This method will be called for each volume node before usage.
 *
 * \param      node         Owner node where the volume was requested
 * \param[out] data         Volume data with all fields to be set by the callback
 * \return                  true if volume creation succeeded
 */
typedef bool (*AtVolumeCreate)(const AtNode* node,
                               AtVolumeData* data);

/**
 * Volume plugin volume update.
 *
 * This method will be called for each volume node before each render
 * pass or scene change, so that the volume can be update accordingly. If not
 * provided, the volume will be destroyed and recreated.
 *
 * \param      node         Owner node where the volume was requested
 * \param[out] data         Volume data with all fields to be set by the callback
 * \return                  true if volume data was modified
 */
typedef bool (*AtVolumeUpdate)(const AtNode* node,
                               AtVolumeData* data);

/**
 * Volume plugin volume cleanup method.
 *
 * This method will be called once for each volume that was created by a call to
 * \ref AtVolumeCreate to allow a chance to clean up any private data.
 *
 * \param data      Volume data returned from \ref AtVolumeCreate
 * \return          true upon success
 */
typedef bool (*AtVolumeCleanup)(const AtNode* node,
                                AtVolumeData* data);

/**
 * Volume plugin sample method.
 *
 * This method will be called concurrently to sample data from a given channel
 * with the specified interpolation.  Implementors should use sg->Po as the
 * sampling position.
 *
 * \param      data      Volume data returned from \ref AtVolumeCreate
 * \param      channel   Data channel name from the volume or implicit surface
 * \param      sg        Shader globals for the sampling context
 * \param      interp    Volume interpolation quality, one of \c AI_VOLUME_INTERP_*
 * \param[out] value     Resulting sampled value, matching the type output in out_type
 * \param[out] type      Resulting value type, one of \c AI_TYPE_FLOAT, \c AI_TYPE_VECTOR2, \c AI_TYPE_RGB, \c AI_TYPE_RGBA, or \c AI_TYPE_VECTOR
 * \return               true upon success
 */
typedef bool (*AtVolumeSample)(const AtVolumeData* data,
                               const AtString channel,
                               const AtShaderGlobals* sg,
                               int interp,
                               AtParamValue *value,
                               uint8_t *type);

/**
 * Volume plugin gradient method.
 *
 * This method will be called concurrently to sample the gradient from a given
 * channel with the specified interpolation.  Implementors should use sg->Po as
 * the sampling position.  Note that this is generally only used for implicit
 * surfaces, so if the plugin is only outputting density volume data this
 * method can just return false and do no other work.  Also note that this will
 * also only make sense for scalar channels, such as signed distance fields.
 *
 * \param      data      Volume data returned from \ref AtVolumePluginCreateVolume
 * \param      channel   Data channel name from the volume or implicit surface
 * \param      sg        Shader globals for the sampling context
 * \param      interp    Volume interpolation quality, one of \c AI_VOLUME_INTERP_*
 * \param[out] gradient  Resulting sampled gradient
 * \return               true upon success
 */
typedef bool (*AtVolumeGradient)(const AtVolumeData* data,
                                 const AtString channel,
                                 const AtShaderGlobals* sg,
                                 int interp,
                                 AtVector* gradient);

/**
 * Volume plugin method for submitting extents along a ray where there is data.
 *
 * For each ray interval where there is volumetric data to be integrated this
 * callback should call \ref AiVolumeAddIntersection to submit the extent
 * along the ray.  Any extra distance from the node's volume_padding parameter
 * must be accounted for and added to each interval.  Note that for implicits,
 * the ray extents should encompass the interval where there is data such as
 * signed-distance field values, like in narrow-band level sets.  The implicit
 * solver will then find the true ray intersection with the surface.
 *
 * \warning
 * Any ray extents submitted that overlap will have the shaders run more than
 * once for each extent.  If shaders should only be run once, then those extents
 * should be merged and submitted just once to \ref AiVolumeAddIntersection instead.
 *
 * \param data      Volume data returned from \ref AtVolumeCreate
 * \param info      Opaque ptr to intersection info passed to \ref AiVolumeAddIntersection
 * \param tid       Current thread ID, use for thread-local access as needed
 * \param time      Time at which the volume is being sampled (for motion blur)
 * \param origin    Ray origin in object space
 * \param direction Ray direction, normalized and in object space
 * \param t0        Start of the source ray interval in which to check for extents
 * \param t1        End of the source ray interval in which to check for extents
 */
typedef void (*AtVolumeRayExtents)(const AtVolumeData* data,
                                   const AtVolumeIntersectionInfo* info,
                                   uint16_t tid,
                                   float time,
                                   const AtVector* origin,
                                   const AtVector* direction,
                                   float t0,
                                   float t1);

struct AtVolumeNodeMethods
{
   AtVolumeCreate        Create;        /**< This method is called to load/create a volume */
   AtVolumeUpdate        Update;        /**< This method is called to update a volume before render passes or on scene changes */
   AtVolumeCleanup       Cleanup;       /**< This method is called to clean up a volume when it's no longer needed */
   AtVolumeRayExtents    RayExtents;    /**< This method is called to get all tightly-bounded extents along a ray where the volume exists */
   AtVolumeSample        Sample;        /**< This method is called to sample a volume's named channel using a given point and interpolation */
   AtVolumeGradient      Gradient;      /**< This method is called to sample the gradient of a volume's named channel using a given point and interpolation */
};

/** Volume node methods exporter */
#define AI_VOLUME_NODE_EXPORT_METHODS(tag)   \
AI_INSTANCE_COMMON_SHAPE_METHODS             \
volume_create;                               \
volume_update;                               \
volume_cleanup;                              \
volume_ray_extents;                          \
volume_sample;                               \
volume_gradient;                             \
static AtVolumeNodeMethods ai_vol_mtds = {   \
   VolumeCreate,                             \
   VolumeUpdate,                             \
   VolumeCleanup,                            \
   VolumeRayExtents,                         \
   VolumeSample,                             \
   VolumeGradient                            \
};                                           \
static AtNodeMethods ai_node_mtds = {        \
   &ai_common_mtds,                          \
   &ai_vol_mtds                              \
};                                           \
const AtNodeMethods* tag = &ai_node_mtds;

#define volume_create                          \
static bool VolumeCreate(const AtNode* node,   \
                         AtVolumeData* data)

#define volume_update                          \
static bool VolumeUpdate(const AtNode* node,   \
                         AtVolumeData* data)

#define volume_cleanup                         \
static bool VolumeCleanup(const AtNode* node,  \
                          AtVolumeData* data)

#define volume_ray_extents                                         \
static void VolumeRayExtents(const AtVolumeData* data,             \
                             const AtVolumeIntersectionInfo* info, \
                             uint16_t tid,                         \
                             float time,                           \
                             const AtVector* origin,               \
                             const AtVector* direction,            \
                             float t0,                             \
                             float t1)

#define volume_sample                                \
static bool VolumeSample(const AtVolumeData* data,   \
                         const AtString channel,     \
                         const AtShaderGlobals* sg,  \
                         int interp,                 \
                         AtParamValue *value,        \
                         uint8_t *type)

#define volume_gradient                                \
static bool VolumeGradient(const AtVolumeData* data,   \
                           const AtString channel,     \
                           const AtShaderGlobals* sg,  \
                           int interp,                 \
                           AtVector* gradient)

/*\}*/
