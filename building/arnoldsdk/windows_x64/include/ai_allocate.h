// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Memory allocation routines
 */

#pragma once
#include "ai_msg.h"
#include "ai_api.h"
#include "ai_string.h"
#include <cstddef> // size_t

/** \defgroup ai_allocate Memory Allocation API
 * 
 * Memory allocation and deallocation.
 * 
 * \{                                                                              
 */       

AI_API void* AiMalloc(size_t size);
AI_API void* AiRealloc(void* addr, size_t size);
AI_API void  AiFree(void* addr);

AI_API void AiAddMemUsage(int64_t size, const AtString category);
AI_API size_t AiMallocUsableSize(const void* addr);

/*\}*/
