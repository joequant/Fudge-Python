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

from fudge import registry
REGISTRY = registry.DEFAULT_REGISTRY

from fudge.field import *                               
from fudge.taxonomy.map import Taxonomy

INDICATOR_FIELD = REGISTRY.type_by_id(types.INDICATOR_TYPE_ID)  
BYTE_FIELD = REGISTRY.type_by_id(types.BYTE_TYPE_ID)  
INT_FIELD = REGISTRY.type_by_id(types.INT_TYPE_ID) 
STRING_FIELD = REGISTRY.type_by_id(types.STRING_TYPE_ID)

class testField(unittest.TestCase):
    def setUp(self):
        pass   
       
    def encodeEquals(self, expected, f, taxonomy=None):
        output = cStringIO.StringIO()
        f.encode(output, taxonomy)                  
        # Allow us to compare easily using \xDF etc..
        result = output.getvalue().encode('hex')
        self.assertEquals(expected, result)
        
    def test_size_no_opts_fixed(self):
        """Test the simplest case""" 
        f = Field(BYTE_FIELD, None, None, 0x01)
        self.assertEquals(3, f.size())  
        self.encodeEquals('800201', f)  
        
        f = Field(INT_FIELD, None, None, 0x80000000)
        self.assertEquals(6, f.size())
        self.encodeEquals('800480000000', f)
         
    def test_size_no_opts_variable(self):  
        f = Field(STRING_FIELD, None, None, u'')
        self.assertEquals(3, f.size()) 
        # TODO(jamesc) - Is this correct according to the spec, or 
        #   should it be '200e' ?
        self.encodeEquals('200e00', f)
        
        f= Field(STRING_FIELD, None, None, u'foo')
        self.assertEquals(6, f.size())
        self.encodeEquals('200e03'+u'foo'.encode('hex'), f)
        
    def test_size_ordinal(self):
        f = Field(BYTE_FIELD, 0x01, None, 0x01)
        self.assertEquals(5, f.size())
        self.encodeEquals('9002000101', f)
        
        f = Field(INT_FIELD, 0x02, None, 0x80000001)
        self.encodeEquals('9004000280000001', f)
        
        self.assertEquals(8, f.size())   
        
    def test_size_name(self):
        f = Field(BYTE_FIELD, None, u'foo', 0x01)
        self.assertEquals(7, f.size())  
        self.encodeEquals('880203'+u'foo'.encode('hex')+'01', f)
        
        f = Field(BYTE_FIELD, None, u'foobarbaz', 0x02)
        self.assertEquals(13, f.size())
        self.encodeEquals('880209'+u'foobarbaz'.encode('hex')+'02', f)
        
    def test_both(self):
        f = Field(BYTE_FIELD, 0x01, u'foo', 0x01)
        self.assertEquals(9, f.size())  
        self.encodeEquals('9802000103'+u'foo'.encode('hex')+'01', f)
        
        f = Field(BYTE_FIELD, 0x02, u'foobarbaz', 0x02)
        self.assertEquals(15, f.size())
        self.encodeEquals('9802000209'+u'foobarbaz'.encode('hex')+'02', f)
   
    def test_indicator(self):
        f = Field(INDICATOR_FIELD, None, None, None)
        self.assertEquals(2, f.size())
        self.encodeEquals('8000', f)
        
    def test_size_with_taxonomy(self):
        f = Field(BYTE_FIELD, None, u'foo', 0xff)
        t = Taxonomy({1 : u'foo', 2 : u'bar'})
        
        self.assertEquals(7, f.size())
        self.encodeEquals('880203'+u'foo'.encode('hex')+'ff', f)
        
        self.assertEquals(5, f.size(t))
        self.encodeEquals('90020001ff', f, t) 
        
    def test_bad_encoded(self):
        # incomplete headers
        self.assertRaises(AssertionError, Field.decode, '')
        self.assertRaises(AssertionError, Field.decode, '\x88')
        self.assertRaises(AssertionError, Field.decode, '\x88\x02')
                                                               
        # TODO(jamesc) better decode error handling
        # Field.decode('\x88\x02\x01')