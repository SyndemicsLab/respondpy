cmake_minimum_required(VERSION 3.27)
project(respondpy VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
find_package(pybind11 CONFIG REQUIRED)
add_subdirectory(extern/RESPONDSimulationv2)

# file(GLOB_RECURSE RESPOND_FILES "extern/RESPONDSimulationv2/include/*.hpp")
# file(GLOB_RECURSE RESPONDPY_HEADERS "include/respondpy/*.hpp")
# file(GLOB RESPONDPY_SRC CONFIGURE_DEPENDS "src/*.cpp")

pybind11_add_module(respondpy src/respondpy.cpp)

target_include_directories(respondpy 
PRIVATE 
    ${CMAKE_CURRENT_SOURCE_DIR}/include
PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/extern/RESPONDSimulationv2/include
)

# Set up the libraries and header search paths for this target
target_link_libraries(respondpy
PRIVATE
    respond
)

install(TARGETS respondpy LIBRARY DESTINATION .)
