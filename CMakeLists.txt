cmake_minimum_required(VERSION 3.27)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
find_package(pybind11 CONFIG REQUIRED)
add_subdirectory(extern/RESPONDSimulationv2)

# file(GLOB_RECURSE RESPOND_FILES "extern/RESPONDSimulationv2/include/*.hpp")
file(GLOB RESPONDPY_SRC CONFIGURE_DEPENDS "src/*.cpp")

pybind11_add_module(_core MODULE ${RESPONDPY_SRC})

# Set up the libraries and header search paths for this target
target_link_libraries(_core
PRIVATE
    respond
)

install(TARGETS _core LIBRARY DESTINATION .)
