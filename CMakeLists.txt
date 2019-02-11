# Copyright (c) 2016 CNRS
# Author: Joseph Mirabel
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

CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
INCLUDE(cmake/base.cmake)
INCLUDE(cmake/python.cmake)
INCLUDE(cmake/hpp.cmake)

SET(PROJECT_NAME hpp-environments)
SET(PROJECT_DESCRIPTION "Environments for the humanoid path planner platform.")
STRING(REPLACE "-" "_" ROS_PROJECT_NAME ${PROJECT_NAME})

SETUP_HPP_PROJECT()

FINDPYTHON(2.7 EXACT REQUIRED)

SET(TEXTURE_FILES
  texture/logo_romeo.jpg
)

INSTALL(DIRECTORY urdf
  DESTINATION "share/${ROS_PROJECT_NAME}")

INSTALL(DIRECTORY srdf
  DESTINATION "share/${ROS_PROJECT_NAME}")

INSTALL(DIRECTORY meshes
  DESTINATION "share/${ROS_PROJECT_NAME}")

INSTALL(FILES ${TEXTURE_FILES}
  DESTINATION "share//${ROS_PROJECT_NAME}/texture"
)

INSTALL(FILES package.xml
  DESTINATION "share/${ROS_PROJECT_NAME}")

ADD_SUBDIRECTORY(src)

SETUP_PROJECT_FINALIZE()
