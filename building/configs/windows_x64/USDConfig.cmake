# - Configuration file for the pxr project
# Defines the following variables:
# PXR_MAJOR_VERSION - Major version number.
# PXR_MINOR_VERSION - Minor version number.
# PXR_PATCH_VERSION - Patch version number.
# PXR_VERSION       - Complete pxr version string.
# PXR_INCLUDE_DIRS  - Root include directory for the installed project.
# PXR_LIBRARIES     - List of all libraries, by target name.
# PXR_foo_LIBRARY   - Absolute path to individual libraries.
# The preprocessor definition PXR_STATIC will be defined if appropriate

get_filename_component(PXR_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

set(USD_MAJOR_VERSION "0")
set(USD_MINOR_VERSION "24")
set(USD_PATCH_VERSION "05")
set(USD_VERSION "2405")

# Set the root directory for USD
if(WIN32)
    set(USD_ROOT "$ENV{USERPROFILE}\\.btoa\\dependencies\\usd")
else()
    set(USD_ROOT "$ENV{HOME}/.btoa/dependencies/usd")
endif()

# Path to the USD monolithic library
set(PXR_usd_ms_LIBRARY "${USD_ROOT}/lib/libusd_ms.so")  # This will be used for non-Windows platforms

# On Windows, the library file extension will be .lib for static or .dll for dynamic
if(WIN32)
    set(PXR_usd_ms_LIBRARY "${USD_ROOT}\\lib\\usd_ms.lib")  # .lib for static linking
endif()

# Set include directories
set(PXR_INCLUDE_DIRS "${USD_ROOT}/include" CACHE PATH "Path to the pxr include directory")

# Define interface targets for each library
add_library(arch INTERFACE IMPORTED)
set_target_properties(arch PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(tf INTERFACE IMPORTED)
set_target_properties(tf PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(gf INTERFACE IMPORTED)
set_target_properties(gf PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(vt INTERFACE IMPORTED)
set_target_properties(vt PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(ndr INTERFACE IMPORTED)
set_target_properties(ndr PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(sdr INTERFACE IMPORTED)
set_target_properties(sdr PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(sdf INTERFACE IMPORTED)
set_target_properties(sdf PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usd INTERFACE IMPORTED)
set_target_properties(usd PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(ar INTERFACE IMPORTED)
set_target_properties(ar PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(plug INTERFACE IMPORTED)
set_target_properties(plug PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(trace INTERFACE IMPORTED)
set_target_properties(trace PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(work INTERFACE IMPORTED)
set_target_properties(work PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(hf INTERFACE IMPORTED)
set_target_properties(hf PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(hd INTERFACE IMPORTED)
set_target_properties(hd PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdGeom INTERFACE IMPORTED)
set_target_properties(usdGeom PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdImaging INTERFACE IMPORTED)
set_target_properties(usdImaging PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdLux INTERFACE IMPORTED)
set_target_properties(usdLux PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdShade INTERFACE IMPORTED)
set_target_properties(usdShade PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(pxOsd INTERFACE IMPORTED)
set_target_properties(pxOsd PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(cameraUtil INTERFACE IMPORTED)
set_target_properties(cameraUtil PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(pcp INTERFACE IMPORTED)
set_target_properties(pcp PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdUtils INTERFACE IMPORTED)
set_target_properties(usdUtils PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdVol INTERFACE IMPORTED)
set_target_properties(usdVol PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdSkel INTERFACE IMPORTED)
set_target_properties(usdSkel PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

add_library(usdRender INTERFACE IMPORTED)
set_target_properties(usdRender PROPERTIES IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}")

# Initialize PXR_LIBRARIES with the path to the monolithic library
set(PXR_LIBRARIES "${PXR_usd_ms_LIBRARY}")

# If PXR_STATIC is defined, include Windows-specific libraries
if(NOT ON)
    if(WIN32)
        list(APPEND PXR_LIBRARIES Shlwapi.lib)
        list(APPEND PXR_LIBRARIES Dbghelp.lib)
    endif()
    add_definitions(-DPXR_STATIC)
endif()

# Provide useful information for debugging
message(STATUS "PXR_INCLUDE_DIRS: ${PXR_INCLUDE_DIRS}")
message(STATUS "PXR_LIBRARIES: ${PXR_LIBRARIES}")

# Set include directories and link libraries
include_directories(${PXR_INCLUDE_DIRS})
link_libraries(${PXR_LIBRARIES})
