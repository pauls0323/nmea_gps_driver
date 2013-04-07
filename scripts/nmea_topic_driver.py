#! /usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Eric Perko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the names of the authors nor the names of their
#    affiliated organizations may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
# Remove scripts directory from module path
# Until nmea_gps_driver.py is removed, it conflicts with
# importing any modules under the nmea_gps_driver name, such as msg
sys.path.pop(0)

import rospy

from nmea_gps_driver.msg import NMEASentence

import libnmea_gps_driver.driver

def nmea_sentence_callback(nmea_sentence, driver):
    try:
        driver.add_sentence(nmea_sentence.sentence, timestamp=nmea_sentence.header.stamp)
    except ValueError as e:
        rospy.logwarn("Value error, likely due to missing fields in the NMEA message. Error was: %s" % e)

if __name__ == '__main__':
    rospy.init_node('nmea_topic_driver')

    driver = libnmea_gps_driver.driver.RosNMEADriver()

    rospy.Subscriber("nmea_sentence", NMEASentence, nmea_sentence_callback,
            driver)

    rospy.spin()
