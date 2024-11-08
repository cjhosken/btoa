// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for managing rendering sessions
 */

#pragma once
#include "ai_api.h"
#include "ai_array.h"
#include "ai_string.h"
#include <stddef.h> // NULL
#include <stdint.h> // uint32_t etc

/** \defgroup ai_render Rendering API
 * 
 *  Render process operation and querying.
 * 
 * \{
 */

// forward declares
struct AtNode;
class AtRenderSession;
class AtUniverse;

/**
 * Render modes
 */
enum AtRenderMode
{
   AI_RENDER_MODE_CAMERA,  /**< Render from a camera */
   AI_RENDER_MODE_FREE     /**< Process arbitrary ray-tracing requests, acting as a "ray server" */
};

/**
 * Render error codes
 */
enum AtRenderErrorCode
{
   AI_SUCCESS,                   /**< no error                    */
   AI_ABORT,                     /**< render aborted              */
   AI_ERROR_NO_CAMERA,           /**< camera not defined          */
   AI_ERROR_BAD_CAMERA,          /**< bad camera data             */
   AI_ERROR_VALIDATION,          /**< usage not validated         */
   AI_ERROR_RENDER_REGION,       /**< invalid render region       */
   AI_INTERRUPT,                 /**< render interrupted by user  */
   AI_ERROR_NO_OUTPUTS,          /**< no rendering outputs        */
   AI_ERROR_UNAVAILABLE_DEVICE,  /**< Cannot create GPU context   */
   AI_ERROR                      /**< generic error               */
};

/**
 * Session mode
 *
 * The session mode indicates to the renderer what the purpose of the session
 * is. When it is intended to set up the scene fully, render, and afterwards
 * end the session without modifying or reading parameters from existing nodes,
 * use AI_SESSION_BATCH mode.  If instead the nodes will be modified after render
 * or have their parameters accessed for some other reason, and then another
 * render invoked, use AI_SESSION_INTERACTIVE.
 */
enum AtSessionMode
{
   AI_SESSION_BATCH,       /**< batch mode, extra (possibly destructive) optimizations allowed */
   AI_SESSION_INTERACTIVE  /**< interactive mode, can read/write nodes after rendering         */
};

/**
 * Outputs ready for display
 *
 * This indicates which outputs are ready for display during interactive
 * rendering.  For faster interactive rendering, Arnold may only provide pixel
 * data on the main interactive output to improve responsiveness for the user.
 * If the render gets to keep going, then Arnold will switch over to providing
 * data for all AOVs/outputs.
 */
enum AtDisplayOutput
{
   AI_DISPLAY_OUTPUT_NONE,                 /**< no updates ready; check render status or error code                      */
   AI_DISPLAY_OUTPUT_INTERACTIVE,          /**< interactive output updated fully, display on screen                      */
   AI_DISPLAY_OUTPUT_PARTIAL_INTERACTIVE,  /**< interactive output updated but not the whole image; put on screen anyway */
   AI_DISPLAY_OUTPUT_ALL                   /**< all outputs are getting updated, any output can be displayed             */
};

/**
 * Status of the current render
 */
enum AtRenderStatus
{
   AI_RENDER_STATUS_NOT_STARTED,  /**< Before \ref AiRenderBegin(), or after \ref AiRenderEnd()                                     */
   AI_RENDER_STATUS_PAUSED,       /**< Update callback paused the render or \ref AiRenderInterrupt() called                         */
   AI_RENDER_STATUS_RESTARTING,   /**< Update callback is restarting the render                                                     */
   AI_RENDER_STATUS_RENDERING,    /**< Currently actively rendering passes                                                          */
   AI_RENDER_STATUS_FINISHED,     /**< Render done, but \ref AiRenderEnd() not called yet                                           */
   AI_RENDER_STATUS_FAILED        /**< Render failed, \ref AiRenderEnd() will return the actual error code (\ref AtRenderErrorCode) */
};

/**
 * Reason for invoking the render update callback
 */
enum AtRenderUpdateType
{
   AI_RENDER_UPDATE_INTERRUPT,    /**< Callback invoked after render is interrupted and paused, can change the scene */
   AI_RENDER_UPDATE_BEFORE_PASS,  /**< Callback invoked just before render pass is to begin, can change the scene    */
   AI_RENDER_UPDATE_DURING_PASS,  /**< Callback invoked during render pass after some pixel data is ready; not currently invoked, but may be in a future release */
   AI_RENDER_UPDATE_AFTER_PASS,   /**< Callback invoked after a non-final render pass is done, can change the scene  */
   AI_RENDER_UPDATE_FINISHED,     /**< Callback invoked after the final render pass is done, can change the scene    */
   AI_RENDER_UPDATE_ERROR,        /**< Callback invoked when an error or abort occurs, and the render has failed     */
   AI_RENDER_UPDATE_IMAGERS       /**< Callback invoked for an imager update                                         */
};

/**
 * System handler mask
 */
enum AtSystemHandlerMask 
{
   AI_SYSTEM_HANDLER_NONE      = 0x0,        /**< no handlers                    */
   AI_SYSTEM_HANDLER_ALL       = 0xFF        /**< all handlers                   */
};

/**
 * \brief Additional useful information about the render, received in the render callback
 *
 * This provides additional information for the render host to decide what to show
 * such as bucket corners, do special handling during fast interactive passes,
 * and so on.  It also reports the actual sample settings for a given pass, as
 * fast interactive passes may have degraded (lowered) the sample settings in
 * order to achieve higher interactivity.  The final pass will always use the
 * original sample settings, however.
 */
struct AtRenderUpdateInfo
{
   AtRenderSession* render_session;          /**< Pointer to the render session that is being executed (in case the callback is used for several render sessions)      */
   AtDisplayOutput outputs_to_display;       /**< Whether the outputs to be shown are none, partial, interactive, or all outputs                                       */
   uint32_t pass_index;                      /**< The pass number we're on out of the total number of passes, useful for indicating progress to the user               */
   uint32_t total_passes;                    /**< The total passes we expect to render, assuming no interruptions or errors                                            */
   int32_t current_AA_samples;               /**< The actual AA_samples for the current pass (options.AA_samples remains the original value)                           */
   int32_t current_AA_samples_max;           /**< The actual AA_samples_max for the current pass (options.AA_samples_max remains the original value)                   */
   int32_t current_GI_diffuse_samples;       /**< The actual GI_diffuse_samples for the current pass (options.GI_diffuse_samples remains the original value)           */
   int32_t current_GI_specular_samples;      /**< The actual GI_specular_samples for the current pass (options.GI_specular_samples remains the original value)         */
   int32_t current_GI_transmission_samples;  /**< The actual GI_transmission_samples for the current pass (options.GI_transmission_samples remains the original value) */
   int32_t current_GI_sss_samples;           /**< The actual GI_sss_samples for the current pass (options.GI_sss_samples remains the original value)                   */
   int32_t current_GI_volume_samples;        /**< The actual GI_volume_samples for the current pass (options.GI_volume_samples remains the original value)             */
};

/**
 * \brief Render update callback
 *
 * This is called in the following circumstances:
 *   - A render pass is about to start: update_type is
 *     \ref AI_RENDER_UPDATE_BEFORE_PASS, and update_info->outputs_to_display
 *     will not be \ref AI_DISPLAY_OUTPUT_NONE.  This is a chance to prepare for
 *     the outputs that will be displayed during this render pass. It is also
 *     safe to change the scene at this point.
 *   - The render is ongoing and some number of buckets are finished: status is
 *     update_type is \ref AI_RENDER_UPDATE_DURING_PASS, and
 *     update_info->outputs_to_display is \ref AI_DISPLAY_OUTPUT_PARTIAL_INTERACTIVE
 *     or \ref AI_DISPLAY_OUTPUT_ALL. It is NOT safe to change the scene at this
 *     point.  Note that the callback is not currently invoked with this update
 *     type, but may be in a future release.
 *   - A render pass is done: update_type is \ref AI_RENDER_UPDATE_AFTER_PASS,
 *     and update_info->outputs_to_display will not be \ref AI_DISPLAY_OUTPUT_NONE.
 *     It is safe to change the scene at this point.
 *   - Rendering is completed: update_type is \ref AI_RENDER_UPDATE_FINISHED,
 *     and update_info->outputs_to_display will not be \ref AI_DISPLAY_OUTPUT_NONE.
 *     It is safe to change the scene at this point.
 *   - Rendering was interrupted: update_type is \ref AI_RENDER_UPDATE_INTERRUPT,
 *     and update_info->outputs_to_display is \ref AI_DISPLAY_OUTPUT_NONE if the
 *     interrupt happened very early in the pass, otherwise it will be
 *     \ref AI_DISPLAY_OUTPUT_PARTIAL_INTERACTIVE. It is safe to change the scene
 *     at this point.
 *   - Rendering has failed: update_type is \ref AI_RENDER_UPDATE_ERROR, and
 *     update_info->outputs_to_display is \ref AI_DISPLAY_OUTPUT_NONE. The
 *     callback should return \ref AI_RENDER_STATUS_FAILED and host code call
 *     \ref AiRenderEnd() to get the error code.  It is NOT safe to change the
 *     scene at this point.
 * .
 * If you need the new render status within the callback, use the following
 * table which provides the equivalent status from the value of update_type:
 * <table>
 *  <caption id="render_update_type_to_status">Render status and render update type mapping</caption>
 *  <tr><th>AtRenderUpdateType</th><th>AtRenderStatus</th></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_INTERRUPT</td><td>\ref AI_RENDER_STATUS_PAUSED</td></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_BEFORE_PASS</td><td>\ref AI_RENDER_STATUS_RENDERING</td></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_DURING_PASS</td><td>\ref AI_RENDER_STATUS_RENDERING</td></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_AFTER_PASS</td><td>\ref AI_RENDER_STATUS_RENDERING</td></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_FINISHED</td><td>\ref AI_RENDER_STATUS_FINISHED</td></tr>
 *  <tr><td>\ref AI_RENDER_UPDATE_ERROR</td><td>\ref AI_RENDER_STATUS_FAILED</td></tr>
 * </table>
 *
 * The callback returns the next status desired, but should never return
 * \ref AI_RENDER_STATUS_NOT_STARTED as that is reserved.
 *
 * If you change the scene during the callback, it is recommended that you return
 * \ref AI_RENDER_STATUS_RESTARTING to go to the beginning of the pass sequence.
 * When the scene doesn't change you probably want to return the status as listed
 * above in the \ref render_update_type_to_status table.
 *
 * \note It is optional to have a render update callback, but is quite helpful
 * especially for interactive and progressive rendering (IPR). Aside from the
 * information in \ref AtRenderUpdateInfo all of the controlling of the render
 * can be done without a callback, usually by polling \ref AiRenderGetStatus()
 * for state changes.
 *
 * \param private_data  Pointer passed to \ref AiRenderBegin(), used for whatever the callback needs
 * \param update_type   Indicates when the callback is being called
 * \param update_info   Extra pass, sample, and output information
 * \return              The next \ref AtRenderStatus desired
 */
typedef AtRenderStatus (*AtRenderUpdateCallback)(void *private_data, AtRenderUpdateType update_type, const AtRenderUpdateInfo *update_info);

AI_API void AiBegin(AtSessionMode default_rs_mode = AI_SESSION_BATCH);
AI_API void AiEnd();
AI_API bool AiArnoldIsActive();
AI_API void AiSetSystemHandlers(AtSystemHandlerMask mask);

AI_API AtRenderSession* AiRenderSession(AtUniverse* universe, AtSessionMode mode = AI_SESSION_BATCH);
AI_API AtUniverse* AiRenderSessionGetUniverse(const AtRenderSession* render_session);
AI_API AI_PURE const AtNode* AiRenderSessionGetOptions(const AtRenderSession* render_session);
AI_API void AiRenderSessionDestroy(AtRenderSession* render_session);

AI_API AtSessionMode AiGetSessionMode(const AtRenderSession* render_session);

AI_API void AiRenderAddInteractiveOutput(AtRenderSession* render_session, uint32_t output_index);
AI_API bool AiRenderIsInteractiveOutput(AtRenderSession* render_session, uint32_t output_index);
AI_API bool AiRenderRemoveInteractiveOutput(AtRenderSession* render_session, uint32_t output_index);
AI_API void AiRenderRemoveAllInteractiveOutputs(AtRenderSession* render_session);

AI_API bool AiRenderSetHintBool(AtRenderSession* render_session, AtString hint, bool value);
AI_API bool AiRenderSetHintInt(AtRenderSession* render_session, AtString hint, int32_t value);
AI_API bool AiRenderSetHintFlt(AtRenderSession* render_session, AtString hint, float value);
AI_API bool AiRenderSetHintStr(AtRenderSession* render_session, AtString hint, AtString value);
AI_API bool AiRenderSetHintArray(AtRenderSession* render_session, AtString hint, AtArray *value);
AI_API bool AiRenderGetHintBool(const AtRenderSession* render_session, AtString hint, bool& value);
AI_API bool AiRenderGetHintInt(const AtRenderSession* render_session, AtString hint, int32_t& value);
AI_API bool AiRenderGetHintFlt(const AtRenderSession* render_session, AtString hint, float& value);
AI_API bool AiRenderGetHintStr(const AtRenderSession* render_session, AtString hint, AtString& value);
AI_API bool AiRenderGetHintArray(const AtRenderSession* render_session, AtString hint, const AtArray*& value);

AI_API AtRenderErrorCode AiRenderBegin(AtRenderSession* render_session, AtRenderMode mode = AI_RENDER_MODE_CAMERA, AtRenderUpdateCallback update_callback = NULL, void* callback_private_data = NULL);
AI_API AtRenderErrorCode AiRenderEnd(AtRenderSession* render_session);
AI_API AtRenderStatus    AiRenderGetStatus(const AtRenderSession* render_session);
AI_API void              AiRenderInterrupt(AtRenderSession* render_session, AtBlockingCall blocking = AI_NON_BLOCKING);
AI_API void              AiRenderAbort(AtRenderSession* render_session, AtBlockingCall blocking = AI_NON_BLOCKING);
AI_API void              AiRenderResume(AtRenderSession* render_session);
AI_API void              AiRenderRestart(AtRenderSession* render_session);
AI_API bool              AiRenderIsAnyActive();
AI_API AtRenderErrorCode AiRender(AtRenderSession* render_session, AtRenderMode mode = AI_RENDER_MODE_CAMERA);

/*\}*/
