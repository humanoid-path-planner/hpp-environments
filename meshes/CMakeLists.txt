# Copyright (c) 2016 CNRS Author: Joseph Mirabel
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

set(BUGGY
    buggy/buggyBB.dae
    buggy/buggy.dae
    buggy/buggy_rearwheel.dae
    buggy/scene.dae
    buggy/scene.stl
    buggy/wheel_frontleft.dae
    buggy/wheel_frontright.dae)

install(FILES ${BUGGY}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes/buggy)

set(UR_BENCHMARK_MESHES ur_benchmark/pokeball.dae)

install(FILES ${UR_BENCHMARK_MESHES}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes/ur_benchmark)

set(HRP2_MESHES hrp2/floor.dae)

install(FILES ${HRP2_MESHES}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes/hrp2)

install(DIRECTORY tests DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes)
