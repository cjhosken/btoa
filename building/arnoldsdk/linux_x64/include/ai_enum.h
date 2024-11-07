// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Enum data type and utility functions
 */

#pragma once
#include "ai_api.h"

/** \defgroup ai_enum  AtEnum API
 * 
 * Arnold \ref AtEnum type.
 * 
 * \{
 */

/** String-based enumerated data type
 *
 * \ref AtNode parameters of type \c AI_TYPE_ENUM are stored as \ref AtEnum.
 * The \ref AtEnum data type is just an array of strings that ends with
 * a NULL string (not an empty string, but a NULL pointer).
 *
 * Note that, in order to keep backwards compatibility, any value strings
 * beginning with a digit will be interpreted as a number.
 */
typedef const char** AtEnum;

AI_API AI_PURE int         AiEnumGetValue(AtEnum enum_type, const char* string);
AI_API AI_PURE const char* AiEnumGetString(AtEnum enum_type, int index);

/*\}*/
