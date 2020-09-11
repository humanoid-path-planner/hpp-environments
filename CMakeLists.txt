# Copyright (c) 2016, 2020 CNRS
# Author: Joseph Mirabel, Guilhem Saurel
#
# this file is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# this file is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# this file.  If not, see
# <http://www.gnu.org/licenses/>.

CMAKE_MINIMUM_REQUIRED(VERSION 3.1)

SET(PROJECT_NAME hpp-environments)
SET(PROJECT_DESCRIPTION "Environments for the humanoid path planner platform.")
STRING(REPLACE "-" "_" ROS_PROJECT_NAME ${PROJECT_NAME})

OPTION(BUILD_PYTHON_INTERFACE "Build the python bindings" ON)
OPTION(INSTALL_PYTHON_INTERFACE_ONLY "Install *ONLY* the python bindings" OFF)

IF(NOT INSTALL_PYTHON_INTERFACE_ONLY)
  SET(PROJECT_USE_CMAKE_EXPORT TRUE)
ENDIF(NOT INSTALL_PYTHON_INTERFACE_ONLY)

INCLUDE(cmake/hpp.cmake)
INCLUDE(cmake/python.cmake)

COMPUTE_PROJECT_ARGS(PROJECT_ARGS LANGUAGES CXX)
PROJECT(${PROJECT_NAME} ${PROJECT_ARGS})

IF(BUILD_PYTHON_INTERFACE)
  FINDPYTHON(REQUIRED)
ENDIF(BUILD_PYTHON_INTERFACE)

SET(TEXTURE_FILES
  texture/logo_romeo.jpg
)

IF(NOT INSTALL_PYTHON_INTERFACE_ONLY)
  INSTALL(DIRECTORY urdf
    DESTINATION "share/${ROS_PROJECT_NAME}")

  INSTALL(DIRECTORY srdf
    DESTINATION "share/${ROS_PROJECT_NAME}")

  INSTALL(DIRECTORY meshes
    DESTINATION "share/${ROS_PROJECT_NAME}")

  INSTALL(FILES ${TEXTURE_FILES}
    DESTINATION "share//${ROS_PROJECT_NAME}/texture")

  INSTALL(FILES package.xml
    DESTINATION "share/${ROS_PROJECT_NAME}")

  ADD_LIBRARY(${PROJECT_NAME} INTERFACE)
  INSTALL(TARGETS ${PROJECT_NAME} EXPORT ${TARGETS_EXPORT_NAME} DESTINATION lib)
ENDIF(NOT INSTALL_PYTHON_INTERFACE_ONLY)

IF(BUILD_PYTHON_INTERFACE)
  ADD_SUBDIRECTORY(src)
ENDIF(BUILD_PYTHON_INTERFACE)
