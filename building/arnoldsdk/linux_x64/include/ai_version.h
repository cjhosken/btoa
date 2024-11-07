// Copyright 2022 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Version number information and checking of backwards-compatibility
 */

#pragma once
#include "ai_api.h"

#define ARNOLD_XSTR(s) ARNOLD_STR(s)
#define ARNOLD_STR(s)  #s

#define AI_MAXSIZE_VERSION 32

/*
 * AI_VERSION_FIX *MUST* be a string!
 * (something like "0.test" is acceptable, too!)
 */
#define AI_VERSION_ARCH_NUM    7
#define AI_VERSION_MAJOR_NUM   3
#define AI_VERSION_MINOR_NUM   4
#define AI_VERSION_FIX         "1"

#define AI_VERSION_ARCH   ARNOLD_XSTR(AI_VERSION_ARCH_NUM)
#define AI_VERSION_MAJOR  ARNOLD_XSTR(AI_VERSION_MAJOR_NUM)
#define AI_VERSION_MINOR  ARNOLD_XSTR(AI_VERSION_MINOR_NUM)

/*
 * Expose Arnold version as a single integer number than can be easily used for direct comparison. E.g.:
 * 
 * #if ARNOLD_VERSION_NUM >= 60002
 */
#define ARNOLD_VERSION_NUM (AI_VERSION_ARCH_NUM*10000)+(AI_VERSION_MAJOR_NUM*100)+AI_VERSION_MINOR_NUM

/*
 * Minimum NVML major version we will allow Arnold GPU to run with
 */
#define AI_MIN_NVML_VERSION 7

/*
 * Minimum CUDA Compute Capability version we will allow Arnold GPU to run with
 */
#define AI_MIN_CUDA_COMPUTE_CAPABILITY 5.0f

/** \defgroup ai_version Versioning API
 * 
 * Arnold version information.
 * 
 * \{
 */

/** Full Arnold version as string */
#define AI_VERSION   AI_VERSION_ARCH "." AI_VERSION_MAJOR "." AI_VERSION_MINOR "." AI_VERSION_FIX

AI_API const char* AiGetVersion(char* arch, char* major, char* minor, char* fix);
AI_API const char* AiGetVersionInfo();
AI_API const char* AiGetCompileOptions();
AI_API bool        AiCheckAPIVersion(const char* arch, const char* major, const char* minor);
AI_API void        AiSetAppString(const char* appstr);

/**
 * Copyright Notice types
 */
enum AtCopyrightNoticeType
{
  AI_COPYRIGHT_NOTICES_CORE,
  AI_COPYRIGHT_NOTICES_PLUGINS
};

AI_API const char* AiGetCopyrightNotices(AtCopyrightNoticeType copyright_notice_type);

/*\}*/
