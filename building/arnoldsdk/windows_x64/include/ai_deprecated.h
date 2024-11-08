// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Macros for backwards compatibility only - do not include this in new code
 * 
 * IMPORTANT: Only include this file from .c or .cpp. Never include this in a
 *            .h file. Also, make this the _last_ thing you include to avoid
 *            problems with system or 3rd party header files.
 */

#pragma once

struct AtCameraInput;
struct AtCameraOutput;
struct AtNode;

AI_API void AiCameraCreateRayDeprecated(const AtNode* node, const AtCameraInput& input,
                                        AtCameraOutput& output, uint16_t tid);

AI_DEPRECATED typedef AtVector  AtPoint;  // eventually we will remove AtPoint.
AI_DEPRECATED typedef AtVector2 AtPoint2; // eventually we will remove AtPoint2.
AI_DEPRECATED typedef AtRGB     AtColor;  // eventually we will remove AtColor.
