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

from fudge.message import Message, Envelope
from fudge import registry
from fudge import types

from fudge import utils

from nose.plugins.skip import SkipTest

class TestDeeperMsg(unittest.TestCase):
    def test_deeper_submsg(self):
        # comparison arrays
        bytes = ''.join([chr(x%256) for x in range(512)] )
        empty = [0] * 128
        shorts = range(16)
        doubles  = [x/10.0 for x in range(16)]

        m = Message()
        m.add(types.INDICATOR, name=u"Indicator")
        m.add(True, name=u"Boolean")

        m.add(128, name=u"Byte")  # Huh - in the C code it's -128 which isn't a byte!
        m.add(-32768, name=u"Short")
        m.add(2147483647, name=u"Int")
        m.add(9223372036854775807L, name=u"Long")
        m.add(1.23456, name=u"Float")
        m.add(1.2345678, name=u"Double", type_=registry.DEFAULT_REGISTRY.type_by_id(types.DOUBLE_TYPE_ID))

        byte_message= Message()
        for size in (4, 8, 16, 20, 32, 64, 128, 256, 512):
            byte_message.add(bytes[:size], ordinal=size)
        m.add(byte_message, name=u'ByteArrays')

        m.add(u'', name=u'Empty String')
        m.add(u'This is a string.', name=u'String')

        fp_message = Message()
        fp_message.add(doubles[:0], name=u'Float[0]', \
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.FLOATARRAY_TYPE_ID))
        fp_message.add(empty[:15], name=u'Float[15]', \
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.FLOATARRAY_TYPE_ID))
        fp_message.add(doubles[:0], name=u'Double[0]', \
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.DOUBLEARRAY_TYPE_ID))
        fp_message.add(doubles[:15], name=u'Double[15]', \
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.DOUBLEARRAY_TYPE_ID))

        array_message = Message()
        array_message.add(bytes[:0], name=u'Byte[0]')
        array_message.add(bytes[:15], name=u'Byte[15]')
        array_message.add(fp_message, name=u'FP Arrays')
        array_message.add(empty[:0], name=u'Short[0]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.SHORTARRAY_TYPE_ID))
        array_message.add(shorts[:15], name=u'Short[15]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.SHORTARRAY_TYPE_ID))
        array_message.add(empty[:0], name=u'Int[0]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.INTARRAY_TYPE_ID))
        array_message.add(empty[:15], name=u'Int[15]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.INTARRAY_TYPE_ID))
        array_message.add(empty[:0], name=u'Long[0]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.LONGARRAY_TYPE_ID))
        array_message.add(empty[:15], name=u'Long[15]',
                type_=registry.DEFAULT_REGISTRY.type_by_id(types.LONGARRAY_TYPE_ID))
        m.add(array_message, name=u'Arrays')

        empty_message = Message()
        m.add(empty_message, name=u'Null Message')

        e = Envelope(m)
        writer = cStringIO.StringIO()
        e.encode(writer)
        bytes = writer.getvalue()

        foo = open('tests/data/deeper_fudge_msg.dat', 'r')
        expected = foo.read()
        foo.close()
        self.assertEquals(len(expected), len(bytes))
        self.assertEquals(expected, bytes)

    def test_decode_encode_deeper(self):
        """decode then encode the deeper_fudge_msg.

        Check they are the same.
        """

        foo = open('tests/data/deeper_fudge_msg.dat', 'r')
        expected = foo.read()
        foo.close()
        e = Envelope.decode(expected)

        writer = cStringIO.StringIO()
        e.encode(writer)
        bytes = writer.getvalue()

        self.assertEquals(len(expected), len(bytes))
        self.assertEquals(expected, bytes)
