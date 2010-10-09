#
# Copyright CERN, 2010.
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

from fudge.message import Envelope, Message
from fudge.types import INDICATOR

class messageTests(unittest.TestCase):
    def setUp(self):
        self._output = cStringIO.StringIO()

    def assertOutput(self, encoded):
        self.assertEquals(encoded, self._output.getvalue())

    def test_empty_envelope(self):
         empty = Envelope(Message())
         empty.encode(self._output)
         self.assertOutput('\x00\x00\x00\x00\x00\x00\x00\x08')

    def test_simple_message(self):
        """A Very simple message - a single indicator field"""
        message = Message()
        message.encode(self._output)
        self.assertOutput('')

        self._output.reset()
        message.add(INDICATOR)
        message.encode(self._output)
        self.assertOutput('\x80\x00')

        m = Message.decode('\x80\x00')
        self.assertEquals(1, len(m.fields))
        f = m.fields[0]
        self.assertEquals(INDICATOR, f.value)

    def test_message_with_multi_fields(self):
        """Check the encoding of a message with a few fields as
        a message .

        """
        encoded_mess = '\x80\x00\x90\x00\x00\x02\x80\x01\x01'
        encoded_env =  '\x00\x00\x00\x00\x00\x00\x00\x11' + encoded_mess

        message = Message()
        message.add(INDICATOR)
        message.add(INDICATOR, ordinal=2)
        message.add(True, classname='bool')
        message.encode(self._output)
        self.assertOutput(encoded_mess)

        m = Message.decode(encoded_mess)
        self.assertEquals(3, len(m.fields))

    def test_envelope_with_multi_fields(self):
        """Check the encoding of a message with a few fields both as
        an envelope.

        """

        encoded_mess = '\x80\x00\x90\x00\x00\x02\x80\x01\x01'
        encoded_env =  '\x00\x00\x00\x00\x00\x00\x00\x11' + encoded_mess

        message = Message()
        message.add(INDICATOR)
        message.add(INDICATOR, ordinal=2)
        message.add(True, classname='bool')

        e = Envelope(message)
        e.encode(self._output)
        self.assertOutput(encoded_env)