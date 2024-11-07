// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for MaterialX
 */

#pragma once

#include "ai_nodes.h"
#include "ai_api.h"
#include "ai_map.h"

/** \defgroup ai_materialx MaterialX API
 * 
 * MaterialX document processing
 * 
 * \details
 * This API acts as a bridge between the Arnold and MaterialX data models.
 * For instance, materials and looks in an Arnold universe can be written
 * to a MaterialX document, and vice versa.
 * 
 * Other utility functions can be used to introspect and query elements in
 * a MaterialX document such as look and material names.
 *
 * \{
 */

/**
 * MaterialX error codes
 */
enum AtMaterialxErrorCode
{
   AI_MATX_SUCCESS,              /**< no error                      */
   AI_MATX_ERROR_LOAD_DOCUMENT,  /**< error loading the document    */
   AI_MATX_ERROR_NO_MATERIALS    /**< no materials found            */
};

AI_API int AiMaterialxWrite(const AtUniverse* universe, const char* filename, const char* look_name, const char* properties = NULL, bool relative = true);
AI_API int AiMaterialxWriteMaterial(const char* filename, const char* material_name, const AtNode* surface = NULL, const AtNode* volume = NULL, const AtNode* displacement = NULL);

AI_API AtArray* AiMaterialxGetLookNames(const char* filename);
AI_API AtArray* AiMaterialxGetMaterialNames(const char* filename);

AI_API int AiMaterialxReadMaterials(AtUniverse* universe, const char* filename, const AtParamValueMap* params = NULL, AtArray* nodes = NULL);
AI_API const AtString AiMaterialxGetOslShaderCode(const char* node_definition, const char* shader_name, AtParamValueMap* connected_inputs = nullptr);
AI_API const AtNodeEntry* AiMaterialxGetNodeEntryFromDefinition(const char* node_definition, AtParamValueMap* optional_parameters = nullptr);

/*\}*/
