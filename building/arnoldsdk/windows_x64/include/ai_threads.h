// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Multi-platform API for the creation and management of CPU threads
 */

#pragma once
#include "ai_api.h"

/** \defgroup ai_threads Thread Management API
 * 
 * Implementation of platform-agnostic CPU threads.
 * 
 * \{
 */

AI_API void* AiThreadCreate(unsigned int (*fn)(void*), void* data, int priority);
AI_API void  AiThreadClose(void* thread);
AI_API void  AiThreadWait(void* thread);
AI_API AI_CONST void* AiThreadSelf();

typedef void (*AtParallelForFunc)(size_t array_index, void* data, void* payload);

AI_API void AiParallelFor(void* array_of_data, size_t data_size, size_t num_data, void* payload, AtParallelForFunc job);

typedef void* AtParallelJobsID;
typedef void (*AtParallelJobsFunc)(void* payload);

AI_API AtParallelJobsID AiParallelJobsCreateID();
AI_API void AiParallelJobsDestroy(AtParallelJobsID jobsID);

AI_API void AiParallelJobsDispatch(AtParallelJobsID jobsID, void* payload, AtParallelJobsFunc job);
AI_API void AiParallelJobsWait(AtParallelJobsID jobsID);

/**
*   Work scheduler structure that can run jobs in parallel. This has more overhead than
*   AiParallelFor(), but is more flexible as it allows for dispatching jobs without needing
*   to place all the jobs in an array.
*   For example:
*   \code
*   AtParallelJobs jobs;
*   for (size_t i = 0; i < job_count; ++i)
*   {      
*      jobs.add(payload, &callback);
*   }  
*   jobs.wait();
*   \endcode
*/
struct AtParallelJobs
{
   AtParallelJobs() { m_jobs = AiParallelJobsCreateID(); }
   ~AtParallelJobs() { AiParallelJobsDestroy(m_jobs); }
   void add(void* payload, AtParallelJobsFunc job) { AiParallelJobsDispatch(m_jobs, payload, job); }
   void wait() { AiParallelJobsWait(m_jobs); }
   AtParallelJobsID m_jobs;
};

#define AI_MAX_THREADS 1024  /**< maximum number of threads */

/** \name Thread Priorities
 * \{
 */
#define AI_PRIORITY_LOWEST   0x00  /**< even lower priority than \c AI_PRIORITY_LOW */
#define AI_PRIORITY_LOW      0x01  /**< low thread priority */
#define AI_PRIORITY_NORMAL   0x02  /**< normal thread priority */
#define AI_PRIORITY_HIGH     0x03  /**< high thread priority */
/*\}*/

/*\}*/
