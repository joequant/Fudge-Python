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

from fudge.registry import *
from fudge import types
from fudge import utils

import uuid

class TestClass(object):
    """Used for testing `fudge.registry.fullname`"""
    pass

class testRegistry(unittest.TestCase):

    def setUp(self):
        self.reg = Registry()
        self.BYTE_TYPE = self.reg[types.BYTE_TYPE_ID]
        self.SHORT_TYPE = self.reg.type_by_id(types.SHORT_TYPE_ID)
        self.INT_TYPE = self.reg.type_by_id(types.INT_TYPE_ID)
        self.LONG_TYPE = self.reg.type_by_id(types.LONG_TYPE_ID)

        self.STRING_TYPE = self.reg.type_by_id(types.STRING_TYPE_ID)

    def test_type_by_id(self):
        self.assertEquals(self.BYTE_TYPE, self.reg.type_by_id(types.BYTE_TYPE_ID))
        self.assertRaises(UnknownTypeError, self.reg.type_by_id, 254)

    def test_type_by_class(self):
        s = u'foo'
        self.assertTrue(s.__class__.__name__, 'unicode')
        self.assertEquals(self.STRING_TYPE, self.reg.type_by_class(s))

        u = uuid.uuid1()
        self.assertRaises(UnknownTypeError, self.reg.type_by_class, u)

    def test_type_by_class_with_class(self):
        n = int(0)
        self.assertEquals(n.__class__.__name__,'int')
        self.assertEquals(self.LONG_TYPE, self.reg.type_by_class(n, classname='long'))

        s = str('foo')
        self.assertEquals(s.__class__.__name__, 'str')
        self.assertEquals(self.STRING_TYPE, self.reg.type_by_class(s, classname='unicode'))

        s = uuid.uuid1()
        self.assertRaises(UnknownTypeError, self.reg.type_by_class, s)

    def test_type_by_class_names(self):
        s =str('foo')
        self.assertEquals(s.__class__.__name__, 'str')

        self.assertEquals(self.STRING_TYPE, self.reg.type_by_class(s, classname='unicode'))

    def test_type_by_class_numbers(self):
        """All numbers map to INT or LONG (and then are narrowed)"""
        self.assertEquals(self.INT_TYPE, self.reg.type_by_class(0))

        self.assertEquals(self.INT_TYPE, self.reg.type_by_class(utils.MAX_BYTE))
        self.assertEquals(self.INT_TYPE, self.reg.type_by_class(utils.MAX_SHORT))
        self.assertEquals(self.INT_TYPE, self.reg.type_by_class(utils.MAX_INT))
        self.assertEquals(self.LONG_TYPE, self.reg.type_by_class(utils.MAX_INT+1))

    def test_narrow_int_byte(self):
        self.assertEquals(self.BYTE_TYPE, self.reg._narrow_int(0))
        self.assertEquals(self.BYTE_TYPE, self.reg._narrow_int(255))
        self.assertEquals(self.SHORT_TYPE, self.reg._narrow_int(-1))
        self.assertEquals(self.SHORT_TYPE, self.reg._narrow_int(256))

    def test_narrow_int_short(self):
        self.assertEquals(self.SHORT_TYPE, self.reg._narrow_int(utils.MIN_SHORT))
        self.assertEquals(self.SHORT_TYPE, self.reg._narrow_int(utils.MAX_SHORT))
        self.assertEquals(self.INT_TYPE, self.reg._narrow_int(utils.MIN_SHORT - 1))
        self.assertEquals(self.INT_TYPE, self.reg._narrow_int(utils.MAX_SHORT + 1))

    def test_narrow_int_int(self):
        self.assertEquals(self.INT_TYPE, self.reg._narrow_int(utils.MIN_INT))
        self.assertEquals(self.INT_TYPE, self.reg._narrow_int(utils.MAX_INT))
        self.assertEquals(self.LONG_TYPE, self.reg._narrow_int(utils.MIN_INT - 1))
        self.assertEquals(self.LONG_TYPE, self.reg._narrow_int(utils.MAX_INT + 1))

    def test_narrow_int_long(self):
        # TODO(jamesc) - should decide what to do for <LONG_MIN, >LONG_MAX
        self.assertEquals(self.LONG_TYPE, self.reg._narrow_int(utils.MIN_LONG))
        self.assertEquals(self.LONG_TYPE, self.reg._narrow_int(utils.MAX_LONG))

    def test_narrow_non_narrowable(self):
        self.assertEquals(self.STRING_TYPE, self.reg.narrow(self.STRING_TYPE,'foo'))

    def test_narrow_byte(self):
        self.assertEquals(self.BYTE_TYPE, self.reg.narrow(self.BYTE_TYPE,0))
        self.assertEquals(self.BYTE_TYPE, self.reg.narrow(self.SHORT_TYPE,0))
        self.assertEquals(self.BYTE_TYPE, self.reg.narrow(self.INT_TYPE,0))
        self.assertEquals(self.BYTE_TYPE, self.reg.narrow(self.LONG_TYPE,0))

    def test_narrow_short(self):
        self.assertEquals(self.SHORT_TYPE, self.reg.narrow(self.SHORT_TYPE, utils.MAX_SHORT))
        self.assertEquals(self.SHORT_TYPE, self.reg.narrow(self.INT_TYPE, utils.MAX_SHORT))
        self.assertEquals(self.SHORT_TYPE, self.reg.narrow(self.LONG_TYPE, utils.MAX_SHORT))

    def test_narrow_int(self):
        self.assertEquals(self.INT_TYPE, self.reg.narrow(self.INT_TYPE, utils.MAX_INT))
        self.assertEquals(self.INT_TYPE, self.reg.narrow(self.LONG_TYPE, utils.MAX_INT))

    def test_narrow_int(self):
        self.assertEquals(self.LONG_TYPE, self.reg.narrow(self.LONG_TYPE, utils.MAX_LONG))

    def test_narrow_str(self):
        array = 'x'*4
        self.assertEquals(self.reg[types.BYTEARRAY4_TYPE_ID], self.reg.narrow(self.reg[types.BYTEARRAY_TYPE_ID], array))

        array = 'x'*20
        self.assertEquals(self.reg[types.BYTEARRAY20_TYPE_ID], self.reg.narrow(self.reg[types.BYTEARRAY_TYPE_ID], array))

        array = 'x'*27
        self.assertEquals(self.reg[types.BYTEARRAY_TYPE_ID], self.reg.narrow(self.reg[types.BYTEARRAY_TYPE_ID], array))

    def test_type_repr(self):
        f = FieldType(1, int, False, 2)
        self.assertEquals("FieldType[id=1, classname='int']", "%r"%f)

    def test_fullname_builtin(self):
        """Check that the fullname stuff works for builtins"""
        self.assertEquals('str', fullname(str))
        self.assertEquals('long', fullname(long))

    def test_fullname_custom(self):
         """Check that the fullname stuff works for builtins"""
         self.assertEquals('str', fullname(str))
         self.assertEquals('long', fullname(long))
         self.assertEquals('tests.test_registry.TestClass', fullname(TestClass))