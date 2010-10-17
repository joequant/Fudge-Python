#!/usr/bin/env python
#
# Copyrigh CERN, 2010.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import unittest
import cStringIO

from fudge import message
from fudge.field import *

from nose.plugins.skip import SkipTest

from fudge import registry
REGISTRY = registry.DEFAULT_REGISTRY
FUDGEMSG_FIELD = REGISTRY.type_by_id(types.FUDGEMSG_TYPE_ID)

BYTES = ''.join([ chr(x%256) for x in range(512)])

class testField(unittest.TestCase):
    def setUp(self):
        pass

    def test_fixedlen_bytearrays(self):
        """Test we can decode a field"""
        # byte[4] '00010203'
        # byte[8] '0001020304050607'
        encoded = '8011' + BYTES[:4].encode('hex')+ \
                  '8012' + BYTES[:8].encode('hex')

        (f, num_bytes) = Field.decode(encoded.decode('hex'))

        self.assertEquals(6, num_bytes)
        self.assertEquals(None, f.name)
        self.assertEquals(None, f.ordinal)
        self.assertEquals(4, len(f.value))
        self.assertEquals(BYTES[:4], f.value)

        (f, num_bytes) = Field.decode(encoded.decode('hex')[num_bytes:])
        self.assertEquals(10, num_bytes)
        self.assertEquals(None, f.name)
        self.assertEquals(None, f.ordinal)
        self.assertEquals(8, len(f.value))
        self.assertEquals(BYTES[:8], f.value)

    def test_fixedlen_bytearrays_submsg(self):
        """Test we decode fixed length byte arrays"""

        # Message
        #   byte[4] '00010203'
        #   byte[8] '0001020304050607'
        encoded = '200f10' + '8011' + BYTES[:4].encode('hex')+ \
                             '8012' + BYTES[:8].encode('hex')

        (f, num_bytes) = Field.decode(encoded.decode('hex'))
        self.assertEquals(19, num_bytes)
        self.assertEquals(None, f.name)
        self.assertEquals(None, f.ordinal)
        self.assertEquals(16, len(f.value))

        m = f.value
        self.assertEquals(2, len(m.fields))

        f1 = m.fields[0]
        self.assertEquals(None, f1.name)
        self.assertEquals(None, f1.ordinal)
        self.assertEquals(4, len(f1.value))
        self.assertEquals(BYTES[:4], f1.value)

        f2 = m.fields[1]
        self.assertEquals(None, f2.name)
        self.assertEquals(None, f2.ordinal)
        self.assertEquals(8, len(f2.value))
        self.assertEquals(BYTES[:8], f2.value)

    def test_string_submsg(self):
        """Test we decode strings correctly"""
        encoded = '200f12' + '200e03' + u'foo'.encode('hex') \
                           + '200e03' + u'bar'.encode('hex') \
                           + '200e03' + u'baz'.encode('hex')

        (f, num_bytes) = Field.decode(encoded.decode('hex'))
        self.assertEquals(21, num_bytes)
        self.assertEquals(None, f.name)
        self.assertEquals(None, f.ordinal)
        self.assertEquals(18, len(f.value))

    def test_string_submsg_ordinals(self):
        """Decode strings with ordinals"""
        encoded = '200f18' + '300e000103' + u'foo'.encode('hex') \
                           + '300e000203' + u'bar'.encode('hex') \
                           + '300e000303' + u'baz'.encode('hex')

        (f, num_bytes) = Field.decode(encoded.decode('hex'))
        self.assertEquals(27, num_bytes)
        self.assertEquals(None, f.name)
        self.assertEquals(None, f.ordinal)
        self.assertEquals(24, len(f.value))

        m = f.value
        self.assertEquals(3, len(m.fields))
