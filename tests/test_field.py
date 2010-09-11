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

from fudge import registry
REGISTRY = registry.DEFAULT_REGISTRY

from fudge.field import *

BYTE_FIELD = REGISTRY.type_by_id(registry.BYTE_TYPE_ID)  
INT_FIELD = REGISTRY.type_by_id(registry.INT_TYPE_ID) 
STRING_FIELD = REGISTRY.type_by_id(registry.STRING_TYPE_ID)

class testField(unittest.TestCase):
    def setUp(self):
        pass   
       
    def test_size_no_opts_fixed(self):
        """Test the simplest case""" 
        f = Field(BYTE_FIELD, None, None, 0x01)
        self.assertEquals(3, f.size())  
        
        f = Field(INT_FIELD, None, None, 0x80000000)
        self.assertEquals(6, f.size())
        
    def test_size_no_opts_variable(self):  
        f = Field(STRING_FIELD, None, None, u'')
        self.assertEquals(3, f.size()) 
        
        f= Field(STRING_FIELD, None, None, u'foo')
        self.assertEquals(6, f.size())
        
    def test_size_ordinal(self):
        f = Field(BYTE_FIELD, 0x01, None, 0x01)
        self.assertEquals(5, f.size())
        
        f = Field(INT_FIELD, 0x02, None, 0x80000001)
        self.assertEquals(8, f.size())   
        
    def test_size_name(self):
        f = Field(BYTE_FIELD, None, u'foo', 0x01)
        self.assertEquals(7, f.size())
        f = Field(BYTE_FIELD, None, u'foobarbaz', 0x02)
        self.assertEquals(13, f.size())
        
    def test_both(self):
        f = Field(BYTE_FIELD, 0x01, u'foo', 0x01)
        self.assertEquals(9, f.size())  
        
        f = Field(BYTE_FIELD, 0x02, u'foobarbaz', 0x02)
        self.assertEquals(15, f.size())
        