// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Various utility functions for shader writers
 */

#pragma once
#include "ai_bbox.h"
#include "ai_color.h"
#include "ai_vector.h"
#include "ai_api.h"
#include "ai_shaderglobals.h"

// forward declaration
struct AtSampler;
struct AtNode;

/** \defgroup ai_shader_util  Shader Utility API
 * 
 * Various utility functions for shader writers.
 * 
 * \{
 */

/** \name Coordinate Transformations
 * \{
 */
#define AI_WORLD_TO_OBJECT  1 /**< World-to-object coordinate transformation */
#define AI_OBJECT_TO_WORLD  2 /**< Object-to-world coordinate transformation */
/* \}*/

/** \name Wireframe Types
 * \{
 */
#define AI_WIREFRAME_TRIANGLES            0   /**< Tessellated triangles      */
#define AI_WIREFRAME_POLYGONS             1   /**< Tessellated polygons       */
#define AI_WIREFRAME_PATCHES              2   /**< Patches before subdivision */
/* \}*/

/** \name Lighting Functions
 * \{
 */
AI_API AI_DEVICE AI_GPU_FORCE_INLINE AtRGB      AiOcclusion(const AtVector& N, const AtVector& Ng, AtShaderGlobals* sg, float mint, float maxt, float spread, float falloff, const AtSampler* sampler, AtVector* Nbent);
AI_API AI_DEVICE AI_GPU_FORCE_INLINE AtRGB      AiSelfOcclusion(const AtVector& N, const AtVector& Ng, AtShaderGlobals* sg, float mint, float maxt, float spread, float falloff, const AtSampler* sampler, AtVector* Nbent);
AI_API                               AtRGB      AiDirectDiffuse(const AtVector& N, AtShaderGlobals* sg);
AI_API                               AtRGB      AiIndirectDiffuse(const AtVector& N, AtShaderGlobals* sg, const AtRGB& weight);
/* \} */

/** \name BSDF Utility Functions
 * \{
 */
AI_API AI_DEVICE AtVector   AiReflect(const AtVector& I, const AtVector& N);
AI_API           AtVectorDv AiReflectWithDerivs(const AtVectorDv& I, const AtVectorDv& N);
AI_API AI_DEVICE AtVector   AiReflectSafe(const AtVector& I, const AtVector& N, const AtVector& Ng);
AI_API AI_DEVICE bool       AiRefract(const AtVector& I, const AtVector& N, AtVector& T, float n1, float n2);
AI_API           bool       AiRefractWithDerivs(const AtVectorDv& I, const AtVectorDv& N, AtVectorDv& T, float n1, float n2);

AI_API AI_DEVICE AI_CONST float AiSchlickFresnel(const AtVector& N, const AtVector& Rd, float Krn);
AI_API AI_CONST AtRGB      AiSchlickFresnelRGB(const AtVector& N, const AtVector& Rd, const AtRGB& Krn);
AI_API AI_CONST AtRGB      AiConductorFresnel(const AtVector& N, const AtVector& Rd, const AtRGB& n, const AtRGB& k);
AI_API AI_CONST float      AiDielectricFresnel(const AtVector& N, const AtVector& Rd, float eta);
AI_API AI_DEVICE void      AiArtisticToConductorFresnel(const AtRGB& reflectivity, const AtRGB& edgetint, AtRGB& n, AtRGB& k);

AI_API AI_DEVICE void      AiFaceForward(AtVector& N, const AtVector& I);
/* \}*/

/** \name Utility Helper Types
 * \{
 */

/** This function pointer points to float-based bump-mapping function for
 * use by AiShaderGlobalsEvaluateBump().
 *
 * This function would return the displacement height for the given shading context.
 * This function would be called three times (on three different shading contexts).
 * The returned displacements would be used to generate a triangle from which a
 * normal is calculated.
 *
 * \param sg    the current shading context
 * \param data  user-defined data pointer
 * \return bump/displacement height for the current shading context
 */
#ifdef AI_CPU_COMPILER
typedef float (*AtFloatBumpEvaluator)(AtShaderGlobals* sg, void* data);
#endif // AI_CPU_COMPILER
/* \}*/

/** \name Utility Functions
 * \{
 */
AI_API AI_DEVICE bool    AiShaderGlobalsGetTriangle(const AtShaderGlobals* sg, int key, AtVector p[3]);
AI_API         bool      AiShaderGlobalsGetVertexNormals(const AtShaderGlobals* sg, int key, AtVector n[3]);
AI_API         bool      AiShaderGlobalsGetVertexUVs(const AtShaderGlobals* sg, const AtString uvset, AtVector2 uv[3]);
AI_API AI_DEVICE uint32_t  AiShaderGlobalsGetPolygon(const AtShaderGlobals* sg, int key, AtVector* p);
AI_API AI_DEVICE uint32_t  AiShaderGlobalsGetUniformID(const AtShaderGlobals* sg);
AI_API AI_DEVICE void      AiShaderGlobalsGetPositionAtTime(const AtShaderGlobals* sg, float time, AtVector& P, AtVector* N, AtVector* Ng, AtVector* Ns);
AI_API AI_DEVICE AI_PURE AtVector2 AiShaderGlobalsGetPixelMotionVector(const AtShaderGlobals* sg, float time0, float time1);
AI_API AI_PURE AtBBox    AiShaderGlobalsGetBBoxLocal(const AtShaderGlobals* sg);
AI_API AI_PURE AtBBox    AiShaderGlobalsGetBBoxWorld(const AtShaderGlobals* sg);
AI_API         AtNode*   AiShaderGlobalsGetShader(const AtShaderGlobals* sg);
AI_API AI_DEVICE int32_t   AiShaderGlobalsGetSelectedOutput(const AtShaderGlobals* sg);
AI_API AI_DEVICE AI_PURE AtVector  AiShaderGlobalsTransformNormal(const AtShaderGlobals* sg, AtVector N, int space);
AI_API AI_DEVICE AI_PURE AtVector  AiShaderGlobalsTransformPoint(const AtShaderGlobals* sg, AtVector P, int space);
AI_API AI_DEVICE AI_PURE AtVector  AiShaderGlobalsTransformVector(const AtShaderGlobals* sg, AtVector V, int space);
AI_API         void      AiShaderGlobalsSetTraceSet(AtShaderGlobals* sg, const AtString set, bool inclusive);
AI_API         void      AiShaderGlobalsUnsetTraceSet(AtShaderGlobals* sg);
AI_API         void*     AiShaderGlobalsQuickAlloc(const AtShaderGlobals* sg, uint32_t size);
#ifdef AI_CPU_COMPILER
AI_API AI_PURE AtVector  AiShaderGlobalsEvaluateBump(AtShaderGlobals* sg, AtFloatBumpEvaluator bump_func, void* data);
#endif // AI_CPU_COMPILER
AI_API AI_DEVICE AtRGB   AiShaderGlobalsStochasticOpacity(AtShaderGlobals *sg, const AtRGB& opacity);
AI_API AI_DEVICE AI_PURE float AiShaderGlobalsArea(const AtShaderGlobals* sg);
AI_API AI_DEVICE AI_PURE float AiShaderGlobalsEdgeLength(const AtShaderGlobals* sg);
AI_API AI_DEVICE AI_PURE float     AiWireframe(const AtShaderGlobals* sg, float line_width, bool raster_space, int edge_type);
AI_API AI_PURE bool      AiShaderGlobalsIsObjectMatte(const AtShaderGlobals *sg);
AI_API AI_PURE bool      AiShaderGlobalsIsObjectOpaque(const AtShaderGlobals *sg);

/**
 * Make the surface normal face the viewer
 *
 * Returns a reversed vector sg->N if needed, in order to make it face forward
 * with respect to viewing vector sg->Rd (not necessarily a camera ray).
 *
 * \param sg      the current shading context
 * \return        viewer-facing normal vector
 */
AI_DEVICE inline AtVector AiFaceViewer(const AtShaderGlobals* sg)
{
   return (AiV3Dot(sg->Ng, sg->Rd) > 0.0f) ? -sg->N : sg->N;
}

/* \}*/

/** \name Camera Information
 * \{
 */
AI_API AI_PURE float AiCameraGetShutterStart();
AI_API AI_PURE float AiCameraGetShutterEnd();
AI_API AI_DEVICE void  AiCameraToWorldMatrix(const AtNode* node, float time, AtMatrix& out);
AI_API AI_DEVICE void  AiWorldToCameraMatrix(const AtNode* node, float time, AtMatrix& out);
AI_API AI_DEVICE void  AiWorldToScreenMatrix(const AtNode* node, float time, AtMatrix& out);
/* \}*/

/** \name Environment Mappings
 * \{
 */
AI_API void AiMappingMirroredBall(const AtVector& dir, float& u, float& v);
AI_API void AiMappingAngularMap  (const AtVector& dir, float& u, float& v);
AI_API void AiMappingLatLong     (const AtVector& dir, float& u, float& v);
/* \}*/

/** \name Derivatives for Environment Mappings
 * \{
 */
AI_API AI_DEVICE void AiMappingMirroredBallDerivs(const AtVector &dir, const AtVector &dDdx, const AtVector &dDdy, float &u, float &v, float &dudx, float &dudy, float &dvdx, float &dvdy);
AI_API AI_DEVICE void AiMappingAngularMapDerivs  (const AtVector &dir, const AtVector &dDdx, const AtVector &dDdy, float &u, float &v, float &dudx, float &dudy, float &dvdx, float &dvdy);
AI_API AI_DEVICE void AiMappingLatLongDerivs     (const AtVector &dir, const AtVector &dDdx, const AtVector &dDdy, float &u, float &v, float &dudx, float &dudy, float &dvdx, float &dvdy);

/* \}*/

/*\}*/
