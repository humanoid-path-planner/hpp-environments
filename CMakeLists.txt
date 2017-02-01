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

SET(PROJECT_NAME hpp_environments)
SET(PROJECT_DESCRIPTION "Environments for the humanoid path planner platform.")
SET(PROJECT_URL "")

SETUP_PROJECT()

FINDPYTHON(2.7 EXACT REQUIRED)

FIND_PACKAGE(catkin REQUIRED)
catkin_package()

SET(TEXTURE_FILES
  texture/logo_romeo.jpg
)

INSTALL(DIRECTORY urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

INSTALL(DIRECTORY srdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

INSTALL(DIRECTORY meshes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

INSTALL(FILES ${TEXTURE_FILES}
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/texture
)

INSTALL(FILES package.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

ADD_SUBDIRECTORY(src)

SETUP_PROJECT_FINALIZE()
