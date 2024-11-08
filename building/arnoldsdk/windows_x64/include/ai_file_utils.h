// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for file path processing
 */

#pragma once

#include <ai_string.h>

/** \defgroup ai_file_utils File Utils API
 *
 *  File path processing and resolution.
 * 
 * \{
 */

enum class AtFileType
{
   Custom,
   Texture,
   OSL,
   Procedural,
   Plugin
};

/**
*  Processes a file path and resolves it against search paths
*
*  This function will first expand any environment variable references in the file path, and
*  apply any existing path remapping to it. After that, if the custom_path string containes one or
*  more paths, it will search for the file in those paths. If not found, and file_type is not "Custom",
*  if will continue searching on the corresponding default path(s) for that type.
*
*  \param file_path    Initial file path to be processed and resolved
*  \param file_type    Used to select one of the default search paths (or Custom for none of them)
*  \param custom_path  A custom search path or paths can be given here
*
*/
AI_API AtString AiResolveFilePath(const char* file_path, AtFileType file_type, const char* custom_path = NULL);

/*\}*/
