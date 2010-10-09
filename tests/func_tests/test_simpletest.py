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


"""Equivalent to the examples/simpletest"""

import unittest
import cStringIO

from fudge.message import Message, Envelope
from fudge import registry
from fudge import types

from fudge import utils

from nose.plugins.skip import SkipTest

MY_NAME = u"Random Person"

ADDRESS = [u"123 Fake Street", u"Some City",
           u"P0S T4L", u"Country"]

class TestSimpleTest(unittest.TestCase):

    def test_simpletest(self):
        """Equivalent to the examples/simpletest"""

        raise SkipTest()

        MSG_TYPE = registry.DEFAULT_REGISTRY[types.FUDGEMSG_TYPE_ID]
        message = Message()

        message.add(MY_NAME, name=u"name")
        message.add(19801231L, ordinal=4, name=u"dob" )

        submsg = Message()
        for line, ordinal in zip(ADDRESS, range(len(ADDRESS))):
            submsg.add(line, ordinal=ordinal)
        message.add(submsg, name=u"address")
        e = Envelope(message)

        writer = cStringIO.StringIO()
        e.encode(writer)
        bytes = writer.getvalue()

        self.assertEquals(108, len(bytes))

        returned = Envelope.decode(bytes)

        self.assertEquals(0, returned.schema_version)
        self.assertEquals(0, returned.directives)

        returned_message = returned.message
        assertEquals(3, len(returned_message.fields))


