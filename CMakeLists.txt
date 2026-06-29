cmake_minimum_required(VERSION 3.27)

project(RESPONDPY LANGUAGES CXX)

include(FetchContent)

set(CMAKE_CXX_STANDARD 20 CACHE STRING "The C++ standard to compile with, 20")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

if($ENV{FORCE_COLOR})
    if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        add_compile_options(-fdiagnostics-color=always)
    elseif("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
        add_compile_options(-fcolor-diagnostics)
    endif()
endif()

# This is a standard recipe for setting a default build type
set(_default_build_type "Debug")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to '${_default_build_type}' as none was specified.")
    set(CMAKE_BUILD_TYPE
        "${_default_build_type}"
        CACHE STRING "Choose the type of build." FORCE)
    # Set the possible values of build type for cmake-gui
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# If no Python venv set, and .venv exists, use it.
if(NOT DEFINED ENV{VIRTUALENV}
   AND NOT DEFINED Python_ROOT_DIR
   AND NOT DEFINED Python_EXECUTABLE
   AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.venv")
  set(Python_ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/.venv")
endif()

# Adding pybind11 and setting up Python
# Will display pybind11 version
set(PYBIND11_FINDPYTHON TRUE)
set(Python_ARTIFACTS_INTERACTIVE TRUE)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG d03662f0984f652b60e7ddce53d3868002275197 # v3.0.4
    FIND_PACKAGE_ARGS NAMES pybind11)

FetchContent_Declare(
    spdlog
    GIT_REPOSITORY  https://github.com/gabime/spdlog.git
    GIT_TAG         v1.x
    GIT_PROGRESS    TRUE
    FIND_PACKAGE_ARGS NAMES spdlog
)
set(SPDLOG_BUILD_SHARED OFF)
set(SPDLOG_BUILD_PIC ON)
set(SPDLOG_INSTALL ON)

FetchContent_Declare(
    respond
    GIT_REPOSITORY https://github.com/SyndemicsLab/respond.git
    GIT_TAG e9a452e7082b785978e66907b17af4db8b9bed53 # v2.4.1
    OVERRIDE_FIND_PACKAGE
)
set(RESPOND_BUILD_DOCS OFF)
set(BUILD_SHARED_LIBS OFF)
set(RESPOND_BUILD_PIC ON)
set(RESPOND_INSTALL ON)
FetchContent_MakeAvailable(pybind11 spdlog respond)

# Display versions
message(STATUS "CMake ${CMAKE_VERSION}")
message(STATUS "Python ${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}")
if(DEFINED pybind11_VERSION)
    message(STATUS "pybind11 ${pybind11_VERSION}")
endif()

#-------------------------------------------------------------------------------
# Target Control
#-------------------------------------------------------------------------------
file(GLOB_RECURSE RESPONDPY_HEADERS "include/respondpy/*.hpp")
file(GLOB RESPONDPY_SRC CONFIGURE_DEPENDS src/*.cpp)

pybind11_add_module(_core MODULE ${RESPONDPY_HEADERS} ${RESPONDPY_SRC})
target_include_directories(_core PRIVATE include)

set_target_properties(_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

 
# Set up the libraries and header search paths for this target
target_link_libraries(_core
    PUBLIC
        respond::respond_model
    PRIVATE
        spdlog::spdlog
)

# Better error messages
target_compile_definitions(_core PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)

source_group(
    TREE ${CMAKE_CURRENT_SOURCE_DIR}/include
    PREFIX "Header Files"
    FILES ${RESPONDPY_HEADERS}
)
source_group(
    TREE ${CMAKE_CURRENT_SOURCE_DIR}/src
    PREFIX "Source Files"
    FILES ${RESPONDPY_SRC}
)

# Make the output library be in respondpy/_core...
# This is a generator expression to avoid Debug/Release subdirectories in IDEs,
# which confuses Python.
set_property(TARGET _core PROPERTY LIBRARY_OUTPUT_DIRECTORY "$<1:respondpy>")

# Collect all the python files and symlink them into the build directory
# Protects from in-source builds (don't do this, please)
if(
    NOT "${CMAKE_CURRENT_SOURCE_DIR}" STREQUAL "${CMAKE_CURRENT_BINARY_DIR}" 
    AND NOT DEFINED SKBUILD
)
    file(
        GLOB_RECURSE RESPONDPY_FILES
        LIST_DIRECTORIES false
        RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/src"
        CONFIGURE_DEPENDS "src/respondpy/*.py")
    foreach(F IN LISTS RESPONDPY_FILES)
        file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/${F}")
        file(CREATE_LINK "${CMAKE_CURRENT_SOURCE_DIR}/src/${F}" "${CMAKE_CURRENT_BINARY_DIR}/${F}"
            COPY_ON_ERROR SYMBOLIC)
    endforeach()
endif()

# Support installing
install(TARGETS _core DESTINATION "respondpy")

if(NOT DEFINED SKBUILD)
  install(DIRECTORY "src/respondpy" DESTINATION ".")
  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/respondpy/version.py"
          DESTINATION "respondpy")

  # Tests (Requires pytest to be available to run)
  include(CTest)
endif()

if(DEFINED SKBUILD)
  # Don't worry about the version
elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/respondpy/version.py")
    set(VERSION_REGEX [=[version[ \t]*=[ \t]*["']([0-9]+\.[0-9]+\.[0-9]+)]=])

    # Read in the line containing the version
    file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/src/respondpy/version.py" VERSION_STRING
        REGEX [=[version[ \t]*=]=])

    # Pick out just the version
    string(REGEX MATCH [=[[0-9]+\.[0-9]+\.[0-9]+]=] VERSION_STRING "${VERSION_STRING}")
else()
    set(VERSION_STRING "0.0.0")
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/respondpy/version.py"
        "version = ${VERSION_STRING}")
    message(STATUS "Not built with scikit-build-core, defaulting version to 0.0.0")
endif()

if(NOT DEFINED SKBUILD)
    project(RESPONDPY LANGUAGES CXX VERSION ${VERSION_STRING})
    message(STATUS "respondpy ${RESPOND_VERSION}")

    if(BUILD_TESTING)
        add_subdirectory(tests)
    endif()
endif()
