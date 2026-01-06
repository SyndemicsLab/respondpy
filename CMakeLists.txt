cmake_minimum_required(VERSION 3.27)

#-------------------------------------------------------------------------------
# Handle building from CMake instead of scikitbuild-core
#-------------------------------------------------------------------------------
if(NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME "respondpy")
    set(SKBUILD_PROJECT_VERSION "0.0.1")
endif()

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

message(STATUS "Building ${SKBUILD_PROJECT_NAME} version ${SKBUILD_PROJECT_VERSION}")

#-------------------------------------------------------------------------------
# Set Compile Flags
#-------------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#-------------------------------------------------------------------------------
# Python Binding Details
#-------------------------------------------------------------------------------
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

#-------------------------------------------------------------------------------
# Target Control
#-------------------------------------------------------------------------------
pybind11_add_module(${SKBUILD_PROJECT_NAME} MODULE)

target_sources(${SKBUILD_PROJECT_NAME}
    PRIVATE
        src/register_respond.cpp
)

#-------------------------------------------------------------------------------
# Include RESPOND Library Repository
#-------------------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    respond
    GIT_REPOSITORY https://github.com/SyndemicsLab/respond.git
    GIT_TAG b5848bf63e7b5cd5eb7f8b8f0c73231be1d423ac
    OVERRIDE_FIND_PACKAGE
)
set(RESPOND_INSTALL ON)
find_package(respond REQUIRED)

# Set up the libraries and header search paths for this target
target_link_libraries(${SKBUILD_PROJECT_NAME}
    PRIVATE
        respond::respond_model
)

pybind11_extension(${SKBUILD_PROJECT_NAME})
if(NOT MSVC AND NOT ${CMAKE_BUILD_TYPE} MATCHES Debug|RelWithDebInfo)
    # Strip unnecessary sections of the binary on Linux/macOS
    pybind11_strip(${SKBUILD_PROJECT_NAME})
endif()
