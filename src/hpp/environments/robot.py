#!/usr/bin/env python
# Copyright (c) 2015 CNRS
# Author: Joseph Mirabel
#
# This file is part of hpp_environments.
# hpp_environments is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp_environments is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp_environments.  If not, see
# <http://www.gnu.org/licenses/>.

from hpp.corbaserver.robot import Robot

##
#  Control of robot Buggy in hpp
class Buggy (Robot):
    ##
    #  Information to retrieve urdf and srdf files.
    packageName = "hpp_environments"
    meshPackageName = "hpp_environments"
    rootJointType = "planar"

    urdfName = "buggy"
    urdfSuffix = ""
    srdfSuffix = ""

    def __init__ (self, robotName, load = True):
        Robot.__init__ (self, robotName, self.rootJointType, load)
