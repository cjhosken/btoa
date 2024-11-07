// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for writing operator nodes
 */

#pragma once

#include "ai_nodes.h"
#include "ai_version.h"
#include "ai_matrix.h"
#include "ai_api.h"

// Forward declarations
struct AtNode;
struct AtCookContext;

/** \defgroup ai_operator Operator API
 * 
 * Operator node creation and operation.
 * 
 * \details
 * This API is used to create graphs of operator nodes which can procedurally perform scene
 * inspection, creation, and late binding modifications at render time.
 * 
 * The operator graph defines a non-destructive set of operations, where the graph is
 * evaluated from a given node in the graph, denoted as target operator. The target operator
 * is defined in the options and can be set using \ref AiOpSetTarget. Any graphs not connected
 * to the target operator will be ignored. 
 * 
 * An operator that is connected to the target will be initialized and cooked if it needs 
 * to do any work. That is determined based on the presence of a selection parameter and
 * if the operator is enabled. 
 * An enabled operator without a selection will always be initialized and cooked at least 
 * once, otherwise it's only initialized and cooked if the selection expression matches one 
 * or more nodes in the scene.
 * 
 * Operators can recursively create other operator nodes and optionally pass child data
 * to them (see \ref AiOpSetChildData. Operators can also declare their own user data,
 * where it is initialized/used in \ref AtOpInit, used in \ref AtOpCook, and deleted in 
 * \ref AtOpCleanup. 
 * Note that no information flows through the graph.
 *
 * Operators are evaluated during the pre-render initialization process which is done in parallel.
 * It is therefore important that the code in an operator node is designed to be re-entrant.
 *
 * \{
 */

typedef bool (*AtOpCleanupChildData)(void* child_data);

AI_API bool     AiOpSetTarget(AtUniverse* universe, AtNode* node);
AI_API AtNode*  AiOpGetTarget(const AtUniverse* universe);

AI_API AtArray* AiOpGetInputs(AtNode* op);
AI_API bool     AiOpLink(AtNode* from, AtNode* to, int index = -1);
AI_API bool     AiOpUnlinkInputByIndex(AtNode* to, unsigned int index);
AI_API bool     AiOpUnlink(AtNode* from, AtNode* to);

AI_API void     AiOpSetChildData(AtNode* op, void* child_data = NULL, AtOpCleanupChildData cleanup = NULL);

AI_API bool     AiOpMatchNodeSelection(AtNode* node, AtString selection, bool relative = true, AtNode* target = NULL);

AI_API AtNode*  AiOpCookContextGetCookScope(AtCookContext* cook_context);

/**
 * Operator init method.
 * 
 * This method will be called first if the operator needs to do any work to perform any
 * initialization required by the operator.
 * 
 * The operator is only initialized once in a batch session but in an IPR session this
 * method is called every time the operator is dirtied. This method may be called 
 * concurrently with other uses of the same operator plugin.
 * 
 * @param op         operator node (itself)
 * @param user_data  general-purpose, user-supplied data pointer that Arnold
 *                   will pass along to the other operator methods
 * @return           true if successful, false otherwise
 */

typedef bool (*AtOpInit)(AtNode* op, void** user_data);

/**
 * Operator cleanup method.
 * 
 * This method is called if the operator node is deleted or if the render session
 * has finished, where it should perform any cleanup required by the operator.
 * Make sure to release any memory you allocated that is no longer needed by Arnold.
 * 
 * @param op         operator node (itself)
 * @param user_data  general-purpose, user-supplied data pointer as returned from
 *                   \ref AtOpInit.
 * @return           true if successful, false otherwise
 */
typedef bool (*AtOpCleanup)(AtNode* op, void* user_data);

/**
 * Operator cook method which operates on the cooked node. The cooked node is either
 * the operator itself (no selection parameter), or any node in the scene which matches
 * the selection expression.
 * 
 * Therefore, this method is called one or more times if the operator needs to do any
 * work, depending on how many nodes it has to operate on. The operator may cook multiple 
 * nodes concurrently.
 * 
 * This method may have access to user data and child data when cooking. The user data
 * is a general-purpose pointer that is used by this operator and is initialized and
 * cleaned up as part of the operator's life cycle. The child data is a general-purpose
 * pointer that can be passed to an operator after creating it, where the cleanup method
 * provided is called when the child data is cleaned up (see \ref AtOpCleanupChildData).
 * 
 * Selection expressions support wildcards when matching parameter names and selections
 * can match multiple parameters. The matched parameter names are accessible to allow
 * customizing the operator's behavior based on the matched parameters.
 * 
 * @param node             node being cooked
 * @param op               operator node (itself)
 * @param child_data       general-purpose data pointer that may be passed here by the
 *                         operator's creator
 * @param user_data        general-purpose, user-supplied data pointer as returned from
 *                         \ref AtOpInit.
 * @param matching_params  names of parameters that matched the selection expression
 * @param cook_context     context specific information about the cook (see e.g.
 *                         \ref AtOpCookContextGetCookReference)
 * @return                 true if successful, false otherwise
 */
typedef bool (*AtOpCook)(AtNode* node, AtNode* op, void* child_data, void* user_data, const AtArray* matching_params, AtCookContext* cook_context);

/**
 * Operator post cook method which is called once per operator instance after all the
 * cook calls for all operators are finished. The method is only called if an operator
 * was cooked by being part of a graph that was connected to the options or a procedural.
 * 
 * @param op         operator node (itself)
 * @param user_data  general-purpose, user-supplied data pointer as returned from
 *                   \ref AtOpInit.
 * @return           true if successful, false otherwise
 */
typedef bool (*AtOpPostCook)(AtNode* op, void* user_data);

/**
 * Cleanup method for child data which is passed to other operators. The lifetime of
 * the child data may differ from the operator that created it so we need to provide
 * this function to perform the cleanup when calling \ref AiOpSetChildData.
 * 
 * @param child_data  general-purpose data pointer that is passed to an operator
 * @return            true if successful, false otherwise
 */

struct AtOperatorNodeMethods
{
   AtOpInit       Init;
   AtOpCleanup    Cleanup;
   AtOpCook       Cook;
   AtOpPostCook   PostCook;
};

/**
 * Operator function pointer entry-point symbol
 *
 * \param[out] methods  List of operator methods
 * \return              true upon success
 */
typedef int (*AtOpFuncPtr)(AtOperatorNodeMethods* methods);

/** Exporter for the methods shared with the standard node interface */
#define AI_OPERATOR_COMMON_NODE_METHODS         \
node_parameters;                                \
static AtCommonMethods ai_common_mtds = {       \
   NULL,                                        \
   NULL,                                        \
   Parameters,                                  \
   NULL,                                        \
   NULL,                                        \
   NULL                                         \
};

#define AI_OPERATOR_NODE_EXPORT_METHODS(tag)    \
AI_OPERATOR_COMMON_NODE_METHODS                 \
operator_init;                                  \
operator_cleanup;                               \
operator_cook;                                  \
operator_post_cook;                             \
static AtOperatorNodeMethods ai_op_mtds = {     \
   OperatorInit,                                \
   OperatorCleanup,                             \
   OperatorCook,                                \
   OperatorPostCook                             \
};                                              \
static AtNodeMethods ai_node_mtds = {           \
   &ai_common_mtds,                             \
   &ai_op_mtds                                  \
};                                              \
const AtNodeMethods* tag = &ai_node_mtds;

#define AI_OPERATOR_NODE_INTERNAL_METHODS(tag)  \
AI_INSTANCE_COMMON_METHODS                      \
static AtNodeMethods ai_node_internal_mtds = {  \
   &ai_common_mtds,                             \
   NULL                                         \
};                                              \
const AtNodeMethods* tag = &ai_node_internal_mtds;

#define operator_init \
static bool OperatorInit(AtNode* op, void** user_data)

#define operator_cleanup \
static bool OperatorCleanup(AtNode* op, void* user_data)

#define operator_cook \
static bool OperatorCook(AtNode* node, AtNode* op, void* child_data, void* user_data, const AtArray* matching_params, AtCookContext* cook_context)

#define operator_post_cook \
static bool OperatorPostCook(AtNode* op, void* user_data)

/*\}*/
