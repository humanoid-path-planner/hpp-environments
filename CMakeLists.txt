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

SET(URDF_FILES
  urdf/buggy.urdf
  urdf/scene.urdf
)
SET(URDF_UR_BENCHMARK_FILES
  urdf/ur_benchmark/obstacle_sphere.urdf
  urdf/ur_benchmark/obstacles.urdf
  urdf/ur_benchmark/table.urdf
  urdf/ur_benchmark/wall.urdf
  urdf/ur_benchmark/box.urdf
  urdf/ur_benchmark/pokeball.urdf
  )

SET(SRDF_UR_BENCHMARK_FILES
  srdf/ur_benchmark/box.srdf
  srdf/ur_benchmark/pokeball.srdf
  )

SET(SRDF_FILES
    srdf/buggy.srdf
    srdf/scene.srdf
  )

INSTALL(FILES ${URDF_FILES}
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf)

INSTALL(FILES ${URDF_UR_BENCHMARK_FILES}
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf/ur_benchmark)

INSTALL(FILES ${SRDF_UR_BENCHMARK_FILES}
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/srdf/ur_benchmark)

INSTALL(FILES ${SRDF_FILES}
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/srdf)

INSTALL(FILES package.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

ADD_SUBDIRECTORY(meshes)
ADD_SUBDIRECTORY(src)

SETUP_PROJECT_FINALIZE()
