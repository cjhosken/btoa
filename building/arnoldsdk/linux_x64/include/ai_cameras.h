// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing camera nodes
 */

#pragma once
#include "ai_nodes.h"
#include "ai_vector.h"

/** \defgroup ai_cameras  Camera Nodes
 * 
 * Camera initialization and update, and custom camera node implementation.
 * 
 * \{
 */

/** Camera ray creation inputs */
struct AtCameraInput {
   float sx, sy;                     /**< screen-space coordinates will range between
                                          (screen_window_min.x, screen_window_min.y/frame_aspect_ratio) and
                                          (screen_window_max.x, screen_window_max.y/frame_aspect_ratio) */
   float dsx, dsy;                   /**< derivatives of the screen-space coordinates with respect to pixel coordinates */
   float lensx, lensy;               /**< lens sampling coordinates in [0,1)^2                */
   float relative_time;              /**< time relative to this camera (in [0,1))             */
};

/** Camera ray creation outputs
 *
 *  If the d*d* derivatives are left to their default value of zero,
 *  an accurate numerical estimate will be automatically computed for
 *  them to prevent catastrophic degradation of texture IO performance.
 *  Note that this estimate might not be as good as analytically computed
 *  derivatives but will often be good enough.
 */
struct AtCameraOutput {
   AtVector origin;                  /**< ray origin in camera space (required)    */
   AtVector dir;                     /**< ray direction in camera space (required) */
   AtVector dOdx, dOdy;              /**< derivative of the ray origin with respect to the pixel coordinates (optional - defaults to 0)    */
   AtVector dDdx, dDdy;              /**< derivative of the ray direction with respect to the pixel coordinates (optional - defaults to 0) */
   AtRGB    weight;                  /**< weight of this ray (used for vignetting) (optional - defaults to AI_RGB_WHITE) */
};

/** Camera node methods structure */
struct AtCameraNodeMethods {
   void (*CreateRay)(const AtNode*, const AtCameraInput&, AtCameraOutput&, uint16_t tid);
   bool (*ReverseRay)(const AtNode* node, const AtVector &Po, float relative_time, AtVector2 &Ps);
};

/** Camera node methods exporter */
#define AI_CAMERA_NODE_EXPORT_METHODS(tag)   \
AI_INSTANCE_COMMON_METHODS                   \
camera_create_ray;                           \
camera_reverse_ray;                          \
static AtCameraNodeMethods ai_cam_mtds = {   \
   CameraCreateRay,                          \
   CameraReverseRay                          \
};                                           \
static AtNodeMethods ai_node_mtds = {        \
   &ai_common_mtds,                          \
   &ai_cam_mtds                              \
};                                           \
const AtNodeMethods* tag = &ai_node_mtds;


/**
 * \name API Methods for Camera Writers
 * \{
 */
AI_API void AiCameraInitialize(AtNode* node);
AI_API void AiCameraUpdate(AtNode* node, bool plane_distance);
/*\}*/

/**
 * \name Node Method Declarations
 * \{
 */

/** Camera's camera_create_ray method declaration
 *
 * This function is called for the camera to return a ray origin and direction given
 * a point in 2d screen coordinates.
 *
 * \param node             pointer to the camera node itself
 * \param input            AtCameraInput data required to generate a new ray (screen position,
 *                         derivatives, etc...)
 * \param[out] output      Camera ray origin, direction and weight. Derivatives are set to zero
 *                         by default. Estimates will be computed if they are not set.
 * \param tid              thread ID that will cast this ray
 */
#define camera_create_ray \
static void CameraCreateRay(const AtNode* node, const AtCameraInput& input, AtCameraOutput& output, uint16_t tid)

/** Camera's camera_reverse_ray method declaration
 *
 * This function is the reverse of camera_create_ray: given a point in camera space 3d coordinates
 * return the corresponding 2d screen coordinates.
 *
 * \param node             pointer to the camera node itself
 * \param Po               Point in camera space
 * \param relative_time    Relative time to compute the projection in
 * \param[out] Ps          Output point in screen space
 *
 * \return                 True if a screen space projection exists and False otherwise. Points that
 *                         fall outside the frame should return True and compute the corresponding
 *                         screen coordinates, only points with no projection at all should return
 *                         False. False can also be returned if there's no implementation available.
 */
#define camera_reverse_ray \
static bool CameraReverseRay(const AtNode* node, const AtVector &Po, float relative_time, AtVector2 &Ps)

/* \}*/

/*\}*/
