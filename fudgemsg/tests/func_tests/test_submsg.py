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


"""Equiv to fudgemsg/tests/data/subMsg.dat"""

import unittest
import cStringIO

from fudgemsg.message import Message, Envelope
from fudgemsg import registry
from fudgemsg import types

from fudgemsg import utils

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

        foo = open('fudgemsg/tests/data/subMsg.dat', 'r')
        expected = foo.read()
        foo.close()
        self.assertEquals(len(expected), len(bytes))
        self.assertEquals(expected, bytes)

    def test_decode_submsg(self):
        file = open('fudgemsg/tests/data/subMsg.dat', 'r')
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
