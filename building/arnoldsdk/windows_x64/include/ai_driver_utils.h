// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Basic utility functions for output drivers
 */

#pragma once
#include "ai_api.h"
#include <stdint.h> // uint32_t etc

/** \addtogroup ai_drivers
 * \{
 */

/** \name Quantization and Dithering
 * \{
 */
AI_API AI_CONST uint8_t  AiQuantize8bit (int x, int y, int i, float value, bool dither);
AI_API AI_CONST uint16_t AiQuantize16bit(int x, int y, int i, float value, bool dither);
/*\}*/

/*\}*/
