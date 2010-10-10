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


"""Equiv to tests/data/subMsg.dat"""

import unittest
import cStringIO

from fudge.message import Message, Envelope
from fudge import registry
from fudge import types

from fudge import utils

from nose.plugins.skip import SkipTest

class TestSubMsg(unittest.TestCase):

    def test_submsg(self):
        sub1 = Message()
        sub2 = Message()

        m = Message()
        sub1.add(u"fibble", name=u"bibble")
        sub1.add(u"Blibble", ordinal=827)

        sub2.add(9837438, name=u"bibble9")
        sub2.add(82.769997, ordinal=828)

        m.add(sub1, name="sub1")
        m.add(sub2, name="sub2")

        e = Envelope(m)
        writer = cStringIO.StringIO()
        e.encode(writer)
        bytes = writer.getvalue()

        foo = open('tests/data/subMsg.dat', 'r')
        expected = foo.read()
        foo.close()
        self.assertEquals(len(expected), len(bytes))
        self.assertEquals(expected, bytes)

    def test_decode_submsg(self):
        file = open('tests/data/subMsg.dat', 'r')
        bytes = file.read()

        e = Envelope.decode(bytes)
        m = e.message
        self.assertEquals(2, len(m.fields))
        self.assertTrue(m.fields[0].is_type(types.FUDGEMSG_TYPE_ID))
        self.assertEquals(u'sub1', m.fields[0].name)
        self.assertTrue(m.fields[1].is_type(types.FUDGEMSG_TYPE_ID))
        self.assertEquals(u'sub2', m.fields[1].name)
        sub1 = m.fields[0].value
        sub2 = m.fields[1].value

        self.assertEquals(2, len(sub1.fields))
        self.assertTrue(sub1.fields[0].is_type(types.STRING_TYPE_ID))
        self.assertEquals(u'bibble', sub1.fields[0].name)
        self.assertEquals(None, sub1.fields[0].ordinal)
        self.assertEquals(u'fibble', sub1.fields[0].value)

        self.assertTrue(sub1.fields[1].is_type(types.STRING_TYPE_ID))
        self.assertEquals(None, sub1.fields[1].name)
        self.assertEquals(827, sub1.fields[1].ordinal)
        self.assertEquals(u'Blibble', sub1.fields[1].value)

        self.assertEquals(2, len(sub2.fields))
        self.assertTrue(sub2.fields[0].is_type(types.INT_TYPE_ID))
        self.assertEquals(u'bibble9', sub2.fields[0].name)
        self.assertEquals(None, sub2.fields[0].ordinal)
        self.assertEquals(9837438, sub2.fields[0].value)

        self.assertTrue(sub2.fields[1].is_type(types.FLOAT_TYPE_ID))
        self.assertEquals(None, sub2.fields[1].name)
        self.assertEquals(828, sub2.fields[1].ordinal)
        self.assertAlmostEquals(82.769997, sub2.fields[1].value, 6)

    def test_deeper_submsg(self):

        m = Message()
        m.add(types.INDICATOR, name=u"Indicator")
        m.add(True, name=u"Boolean")

        m.add(255, name=u"Byte")  # Huh - in the C code it's -128 which isn't a byte!
        m.add(-32768, name=u"Short")
        m.add(2147483647, name=u"Int")
        m.add(9223372036854775807L, name=u"Long")
        m.add(1.23456, name=u"Float")


        #TEST_EQUALS_INT( fields [  8 ].type, FUDGE_TYPE_FUDGE_MSG );
        #TEST_EQUALS_MEMORY( FudgeString_getData ( fields [  8 ].name ), 10, "ByteArrays", 10 );
        #TEST_EQUALS_TRUE( ( bytemessage = fields [ 8 ].data.message ) != 0 );

        m.add(1.2345678, name=u"Double", type_=registry.DEFAULT_REGISTRY.type_by_id(types.DOUBLE_TYPE_ID))
        m.add(u'', name=u"Empty String")
        m.add(u'This is a string.', name="String")


        #TEST_EQUALS_INT( fields [ 11 ].type, FUDGE_TYPE_FUDGE_MSG );
        #TEST_EQUALS_MEMORY( FudgeString_getData ( fields [ 11 ].name ), 6, "Arrays", 6 );
        #TEST_EQUALS_TRUE( ( arraysmessage = fields [ 11 ].data.message ) != 0 );

        empty_message = Message()
        m.add(empty_message, name=u'Null Message')

        #TEST_EQUALS_INT( fields [ 12 ].type, FUDGE_TYPE_FUDGE_MSG );
        #TEST_EQUALS_MEMORY( FudgeString_getData ( fields [ 12 ].name ), 12, "Null Message", 12 );
        #TEST_EQUALS_TRUE( ( emptymessage = fields [ 12 ].data.message ) != 0 );

        e = Envelope(m)
        foo = open('foo', 'w')
        e.encode(foo)
        foo.close()