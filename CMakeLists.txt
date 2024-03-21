# Copyright (c) 2016, 2020 CNRS Author: Joseph Mirabel, Guilhem Saurel
#
# this file is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# this file is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Lesser Public License for more
# details.  You should have received a copy of the GNU Lesser General Public
# License along with this file.  If not, see <http://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 3.10)

set(PROJECT_NAME hpp-environments)
set(PROJECT_DESCRIPTION "Environments for the humanoid path planner platform.")
string(REPLACE "-" "_" ROS_PROJECT_NAME ${PROJECT_NAME})

option(BUILD_PYTHON_INTERFACE "Build the python bindings" ON)
option(INSTALL_PYTHON_INTERFACE_ONLY "Install *ONLY* the python bindings" OFF)

if(NOT INSTALL_PYTHON_INTERFACE_ONLY)
  set(PROJECT_USE_CMAKE_EXPORT TRUE)
endif(NOT INSTALL_PYTHON_INTERFACE_ONLY)

# Check if the submodule cmake have been initialized
set(JRL_CMAKE_MODULES "${CMAKE_CURRENT_LIST_DIR}/cmake")
if(EXISTS "${JRL_CMAKE_MODULES}/base.cmake")
  message(STATUS "JRL cmakemodules found in 'cmake/' git submodule")
else()
  find_package(jrl-cmakemodules QUIET CONFIG)
  if(jrl-cmakemodules_FOUND)
    get_property(
      JRL_CMAKE_MODULES
      TARGET jrl-cmakemodules::jrl-cmakemodules
      PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS "JRL cmakemodules found on system at ${JRL_CMAKE_MODULES}")
  elseif(${CMAKE_VERSION} VERSION_LESS "3.14.0")
    message(
      FATAL_ERROR
        "\nCan't find jrl-cmakemodules. Please either:\n"
        "  - use git submodule: 'git submodule update --init'\n"
        "  - or install https://github.com/jrl-umi3218/jrl-cmakemodules\n"
        "  - or upgrade your CMake version to >= 3.14 to allow automatic fetching\n"
    )
  else()
    message(STATUS "JRL cmakemodules not found. Let's fetch it.")
    include(FetchContent)
    FetchContent_Declare(
      "jrl-cmakemodules"
      GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
    FetchContent_MakeAvailable("jrl-cmakemodules")
    FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
  endif()
endif()

include("${JRL_CMAKE_MODULES}/hpp.cmake")
include("${JRL_CMAKE_MODULES}/python.cmake")

compute_project_args(PROJECT_ARGS LANGUAGES CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})

if(BUILD_PYTHON_INTERFACE)
  findpython(REQUIRED)
endif(BUILD_PYTHON_INTERFACE)

set(TEXTURE_FILES texture/logo_romeo.jpg)

if(NOT INSTALL_PYTHON_INTERFACE_ONLY)
  add_project_dependency(example-robot-data 3.9.1 REQUIRED)

  install(DIRECTORY urdf DESTINATION "share/${ROS_PROJECT_NAME}")

  install(DIRECTORY srdf DESTINATION "share/${ROS_PROJECT_NAME}")

  install(DIRECTORY meshes DESTINATION "share/${ROS_PROJECT_NAME}")

  install(FILES ${TEXTURE_FILES}
          DESTINATION "share//${ROS_PROJECT_NAME}/texture")

  install(FILES package.xml DESTINATION "share/${ROS_PROJECT_NAME}")

  add_library(${PROJECT_NAME} INTERFACE)
  install(
    TARGETS ${PROJECT_NAME}
    EXPORT ${TARGETS_EXPORT_NAME}
    DESTINATION lib)
endif(NOT INSTALL_PYTHON_INTERFACE_ONLY)

if(BUILD_PYTHON_INTERFACE)
  add_subdirectory(src)
endif(BUILD_PYTHON_INTERFACE)
