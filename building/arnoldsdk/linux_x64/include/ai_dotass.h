// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for reading and writing the .ass scene file format
 */

#pragma once
#include "ai_node_entry.h"
#include "ai_scene.h"

struct AtMetadataStore;
class AtUniverse;

/** \defgroup ai_dotass ASS File API
 *
 *  Loading and writing of .ass (Arnold Scene Source) scene files.
 *
 *  This is deprecated in favor of ai_scene.h and its AiScene* methods.
 * 
 *  \details
 *  Arnold has built-in support for writing scene data to a file and later
 *  reading the file in. Although not required, the extension for these files
 *  is usually .ass, which stands for <b>A</b>rnold <b>S</b>cene <b>S</b>ource.
 *  The file format is a straightforward mapping from Arnold \ref AtNode's 
 *  to human-readable ASCII. For example, a sphere node is written as:
 *  \code
 *  sphere          // this is the node class
 *  {               // any number of param/value pairs enclosed in curly braces
 *   center 0 0 0   //  parameter "center" of type AtVector is set to value (0,0,0)
 *   radius 2.0     //  parameter "radius" of type float is set to value 2.0
 *  }               // end of node block
 *  \endcode
 *
 * \{
 */

// This is the new API, supporting multiple universes.
AI_API AI_DEPRECATED int AiASSWrite(AtUniverse* universe, const char* filename, int mask = AI_NODE_ALL, bool open_procs = false, bool binary = true);
AI_API AI_DEPRECATED int AiASSWriteWithMetadata(AtUniverse* universe, const char* filename, int mask = AI_NODE_ALL, bool open_procs = false, bool binary = true, const AtMetadataStore* mds = NULL);
AI_API AI_DEPRECATED int AiASSLoad(AtUniverse* universe, const char* filename, int mask = AI_NODE_ALL);

/*\}*/
