// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for writing procedural geometry nodes
 */

#pragma once
#include "ai_map.h"
#include "ai_version.h"
#ifdef AI_CPU_COMPILER

// forward declaration
struct AtBBox;
struct AtNode;
class AtUniverse;

/** \defgroup ai_procedurals Procedural API
 * 
 * Implementation of custom Arnold procedural nodes.
 * 
 *  \details
 * This API is used to create geometry procedurally at render time, rather than
 * upfront. This is accomplished by providing the renderer some callback functions
 * which are called during scene initialization, before rendering. Procedural nodes
 * should only contain geometry, shaders and lights.
 *
 * Note that procedurals can recursively create other procedural nodes.
 *
 * Procedurals are loaded during the pre-render initialization process. This process
 * runs single-threaded by default, but setting the metadata "parallel_init" to true will
 * allow multiple instances of the same procedural to be initialized in parallel when 
 * "options.parallel_node_init" is true (the default)
 * 
 * \code
 * node_parameters
 * {
 *  ...
 *    // Set procedural to run in parallel
 *    AiMetaDataSetBool(nentry, "", "parallel_init", true);
 *  ...
 * }
 * \endcode
 *
 * So, in order to benefit from this parallel initialization, it is necessary that
 * the code in a procedural node is properly designed to be re-entrant.
 *
 * \{
 */

/**
 * Procedural init method.
 * 
 * This method will be called first and should perform any initialization required
 * by your procedural. You probably want to create new nodes inside this method
 * but you should return them through \ref AtProcGetNode and correctly return
 * the number of created nodes from \ref AtProcNumNodes, otherwise the behavior
 * is undefined. Alternatively, if you know ahead of time exactly how many nodes
 * you are going to create, you can create them in \ref AtProcGetNode too.
 *
 * This method may be called concurrently with other uses of the same procedural
 * plugin, unless "options.enable_threaded_procedurals" is off.
 *
 * \param      node      This is the procedural node itself
 * \param[out] user_ptr  This is a general-purpose, user-supplied data pointer that
 *                       Arnold will pass along to the other procedural methods.
 * \return               true upon success
 */
typedef int (*AtProcInit)(AtNode* node, void** user_ptr);

/**
 * Procedural cleanup method.
 * 
 * This method will be called last and should perform any cleanup required
 * by your procedural. Make sure you release any memory you allocated that is no
 * longer needed by Arnold.
 *
 * This method may be called concurrently with other uses of the same procedural
 * plugin.
 *
 * \param node      This is the procedural node itself
 * \param user_ptr  User data pointer, as returned from \ref AtProcInit
 * \return          true upon success
 */
typedef int (*AtProcCleanup)(const AtNode* node, void* user_ptr);

/**
 * Procedural node count method.
 * 
 * This method will be called after initialization and should report the exact
 * number of nodes to be created. Alternatively, when the total number of nodes is
 * not known beforehand, it might return -1, and then Arnold will call the
 * \ref AtProcGetNode method until it returns NULL to indicate no more nodes are
 * available.
 *
 * This method may be called concurrently with other uses of the same procedural
 * plugin.
 *
 * \param node      This is the procedural node itself
 * \param user_ptr  User data pointer, as returned from \ref AtProcInit
 * \return          The number of nodes in the procedural
 */
typedef int (*AtProcNumNodes)(const AtNode* node, void* user_ptr);

/**
 * Procedural node fetching method.
 * 
 * This method will be called once for each node to be created (as determined by
 * \ref AtProcNumNodes). Note that if you created any node in \ref AtProcInit, they
 * also should be returned here, otherwise the behaviour would be undefined.
 *
 * If -1 was returned by \ref AtProcNumNodes, this method should return NULL when
 * all nodes have been returned and there are no more available.
 *
 * This method may be called concurrently with other uses of the same procedural
 * plugin.
 *
 * \param node      This is the procedural node itself
 * \param user_ptr  User data pointer, as returned from \ref AtProcInit
 * \param i         Node index, in the range 0 to \ref AtProcNumNodes - 1
 * \return          The i'th node in the procedural
 */
typedef AtNode* (*AtProcGetNode)(const AtNode* node, void* user_ptr, int i);

/**
 * Enum with the different modes available for a procedural viewport representation
 */
enum AtProcViewportMode
{
    AI_PROC_BOXES = 0,
    AI_PROC_POINTS,
    AI_PROC_POLYGONS,
};

/**
 * Procedural viewport representation method.
 * 
 * This method can be called to obtain a simplified representation of a procedural, made up of nodes that will be
 * created in the given universe.
 *
 * This is an example implementation for a simple custom procedural:
 * \code
 * procedural_viewport
 * {
 *    if (mode == AI_PROC_BOXES)
 *    {
 *       AtNode* bbox_node = AiNode(universe, "box", "bbox0");
 *       AiNodeSetVec(bbox_node, "min", -5, -5, -5);
 *       AiNodeSetVec(bbox_node, "max", 5, 5, 5);
 *    }
 *    return AI_SUCCESS;
 * }
 * \endcode
 * 
 * \param node              This is the procedural node itself
 * \param universe          The universe where the new nodes will be created
 * \param mode              The type of primitives used for the viewport representation
 * \param params            List of optional parameters to be interpreted by the procedurals
 * \return                  \c AI_SUCCESS if no error, an error value otherwise
 */
typedef int (*AtProcViewport)(const AtNode* node, AtUniverse* universe, AtProcViewportMode mode, const AtParamValueMap* params);

struct AtProceduralNodeMethods {
   AtProcInit          Init;                         /**< This is called before expanding the procedural */
   AtProcCleanup       Cleanup;                      /**< This is called last and should clean up any (temporary) memory used by the procedural */
   AtProcNumNodes      NumNodes;                     /**< This is called to find out how many nodes this procedural will generate */
   AtProcGetNode       GetNode;                      /**< This is called NumNodes times, once for each node the procedural creates */
   AtProcViewport      ProceduralViewport;           /**< This is called to get a viewport representation of the given procedural node */
};

/**
 * Procedural function pointer entry-point symbol
 *
 * A function pointer of this type can be set in the procedural funcptr parameter.
 *
 * \param[out] methods  List of procedural methods (some of which are optional) to be supplied by the user
 * \return              true upon success
 */
typedef int (*AtProcFuncPtr)(AtProceduralNodeMethods* methods);

/** Procedural node methods exporter */
#define AI_PROCEDURAL_NODE_EXPORT_METHODS(tag)  \
AI_INSTANCE_COMMON_SHAPE_METHODS                \
procedural_init;                                \
procedural_cleanup;                             \
procedural_num_nodes;                           \
procedural_get_node;                            \
static AtProceduralNodeMethods ai_proc_mtds = { \
   ProceduralInit,                              \
   ProceduralCleanup,                           \
   ProceduralNumNodes,                          \
   ProceduralGetNode,                           \
   NULL,                                        \
};                                              \
static AtNodeMethods ai_node_mtds = {           \
   &ai_common_mtds,                             \
   &ai_proc_mtds                                \
};                                              \
const AtNodeMethods* tag = &ai_node_mtds;

#define procedural_init \
static int ProceduralInit(AtNode* node, void** user_ptr)

#define procedural_cleanup \
static int ProceduralCleanup(const AtNode* node, void* user_ptr)

#define procedural_num_nodes \
static int ProceduralNumNodes(const AtNode* node, void* user_ptr)

#define procedural_get_node \
static AtNode* ProceduralGetNode(const AtNode* node, void* user_ptr, int i)

#define procedural_update                                          \
static void Update(AtRenderSession* render_session, AtNode* node); \
AI_OPTIONAL_METHOD_INSTALL(ai_common_mtds, Update)                 \
static void Update(AtRenderSession* render_session, AtNode* node)

#define procedural_finish                          \
static void Finish(AtNode* node);                  \
AI_OPTIONAL_METHOD_INSTALL(ai_common_mtds, Finish) \
static void Finish(AtNode* node)

#define procedural_viewport \
static int ProceduralViewport(const AtNode* node, AtUniverse* universe, AtProcViewportMode mode, const AtParamValueMap* params); \
AI_OPTIONAL_METHOD_INSTALL(ai_proc_mtds, ProceduralViewport) \
static int ProceduralViewport(const AtNode* node, AtUniverse* universe, AtProcViewportMode mode, const AtParamValueMap* params)

/**
 * Procedural viewport representation method.
 * 
 * Call this method to get a simplified representation of a procedural for a DCC viewport.
 * The nodes are created in the given universe, and mode determines the type of representation
 * (for example, bounding boxes, points, or polygons). The optional params allows you to pass in 
 * a variable number of paramater values to the method.
 *
 * This is an example of some code to get this representation from a procedural "proc":
 * \code
 * // Create new universe to store the procedural representation
 * AtUniverse* view_universe = AiUniverse();
 * 
 * // Obtain bounding-box representation (one box for each object in the procedural)
 * AtParamValueMap* params = AiParamValueMap();
 * AiParamValueMapSetInt(params, AtString("param"), 0);  // Example parameter
 * AiProceduralViewport(proc, view_universe, AI_PROC_BOXES, params);
 * AiParamValueMapDestroy(params);
 * 
 * // After that, we can iterate over those nodes and get any kind of information
 * AtNodeIterator* it = AiUniverseGetNodeIterator(view_universe, AI_NODE_SHAPE);
 * while (!AiNodeIteratorFinished(it))
 * {
 *    AtNode* node = AiNodeIteratorGetNext(it);
 *    printf("Node name: %s\n", AiNodeGetName(node));
 * }
 * AiNodeIteratorDestroy(it);
 * \endcode
 *
 * Optional parameters allow further configuration of the representation:
 * <table>
 * <tr><th>Supported optional parameters
 * <tr><td> *None yet*
 * </table>
 * 
 * \param node              This is the procedural node itself
 * \param universe          The universe where the new nodes will be created. A valid
 *                          universe pointer needs to be passed. If null, this function
 *                          will return with an error
 * \param mode              The type of primitives used for the viewport representation
 * \param params            List of optional parameters to be interpreted by the procedurals
 * \return                  AI_SUCCESS if no error, an error value otherwise
 */
AI_API int AiProceduralViewport(const AtNode* node, AtUniverse* universe, AtProcViewportMode mode = AI_PROC_BOXES, const AtParamValueMap* params = NULL);

/**
 * Method to expand a procedural node on demand.
 * 
 * Invoking this method before the render starts will initialize a procedural and 
 * generate its children nodes.
 * \param node      The procedural node to be expanded
 * \param params    Optional AtParamValueMap to pass custom arguments for the expansion
 * \return          true upon success
 */
AI_API bool AiProceduralExpand(AtNode *node, const AtParamValueMap* params = NULL);
/*\}*/
#endif // AI_CPU_COMPILER
