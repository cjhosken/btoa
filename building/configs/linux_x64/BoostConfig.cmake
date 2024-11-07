get_filename_component(PXR_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

# Find and configure Boost
set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)

set(Boost_LIBRARIES "$ENV{HOME}/.btoa/dependencies/boost/lib")
set(Boost_INCLUDE_DIRS "$ENV{HOME}/.btoa/dependencies/boost/include")

message(STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")

include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARIES})

