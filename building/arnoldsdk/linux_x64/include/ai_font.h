// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for managing fonts
 */

#pragma once

#include <ai_array.h>
#include <ai_string.h>

/** \defgroup ai_font Font API
 *
 *  Font utilities.
 * 
 * \{
 */ 

/**
*  Return available font families
*
*  Fonts are loaded from the following places:
*   - any directories named in the OPENIMAGEIO_FONTS environment variable
*   - system font directories (e.g. /Library/Fonts, /System/Library/Fonts, C:\Windows\Fonts)
*   - user font directories (e.g. /usr/fonts, /usr/share/fonts, %LOCALAPPDATA%\Microsoft\Windows\Fonts)
* 
*  \return             list of available font families
*/
AI_API const AtArray* AiFontGetFamilies();

/**
*  Return available font styles of a given font family
*
*  \param family       font family name (e.g. Arial)
*  \return             list of available font styles
*/
AI_API const AtArray* AiFontGetStyles(const AtString family);

/**
*  Filename of a given font family and style
*
*  This function returns the filename of a given font family name and style.
*  For instance the filename of the "Courier New Italic" font is "couri.ttf".
*  If style is an empty string, it returns the regular style font, if exists.
*
*  \param family       font family name (e.g. Arial)
*  \param style        font style (e.g. Regular, Italic, etc.)
*  \return             font filename
*/
AI_API AtString AiFontGetFilename(const AtString family, const AtString style);

/*\}*/
