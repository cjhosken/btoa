# pxrConfig.cmake - Configuration file for the pxr project

# Determine the directory where this config file is located
get_filename_component(_PXR_CONFIG_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

# Define version numbers
set(PXR_MAJOR_VERSION "0")
set(PXR_MINOR_VERSION "25")
set(PXR_PATCH_VERSION "02")
set(PXR_VERSION "${PXR_MAJOR_VERSION}.${PXR_MINOR_VERSION}.${PXR_PATCH_VERSION}")

# Define root directory of the USD install (assumed relative to config file)
set(PXR_ROOT "${_PXR_CONFIG_DIR}")

# Set include and library paths
set(PXR_INCLUDE_DIRS "${PXR_ROOT}/include")
set(PXR_LIBRARY_DIR "${PXR_ROOT}/lib")
set(PXR_usd_ms_LIBRARY "${PXR_LIBRARY_DIR}/libusd_ms.so")

# Preprocessor define for static linking, if needed
add_definitions(-DPXR_STATIC)

# Macro to simplify interface library creation
function(pxr_import_library libname)
    add_library(${libname} INTERFACE IMPORTED)
    set_target_properties(${libname} PROPERTIES
        IMPORTED_LOCATION "${PXR_usd_ms_LIBRARY}"
        INTERFACE_INCLUDE_DIRECTORIES "${PXR_INCLUDE_DIRS}"
    )
endfunction()

# List of USD component libraries
set(_pxr_components
    arch tf gf vt ndr sdr sdf usd ar plug trace work
    hf hd usdGeom usdImaging usdLux usdShade pxOsd
    cameraUtil pcp usdUtils usdVol usdSkel usdRender
)

# Create imported interface libraries for all components
foreach(lib ${_pxr_components})
    pxr_import_library(${lib})
endforeach()

# Define list of all available PXR libraries
set(PXR_LIBRARIES ${_pxr_components})

# Exported variables
set(PXR_INCLUDE_DIRS ${PXR_INCLUDE_DIRS})
set(PXR_LIBRARIES ${PXR_LIBRARIES})
set(PXR_VERSION ${PXR_VERSION})

# Optional messages for debugging
message(STATUS "Found PXR version: ${PXR_VERSION}")
message(STATUS "PXR include dirs: ${PXR_INCLUDE_DIRS}")
message(STATUS "PXR monolithic lib: ${PXR_usd_ms_LIBRARY}")
