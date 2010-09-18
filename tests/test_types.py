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

from fudge.types import *

class testTypes(unittest.TestCase):
    def setUp(self):
       pass

    def test_unicode(self):
        self.assertEquals(0, size_unicode(''))
        
        unicode_val = u'Ma\xf1ana' 
        self.assertEquals(7, size_unicode(unicode_val)) 
        
        unicode_val = u'Ma\u00f1ana'
        self.assertEquals(7, size_unicode(unicode_val)) 
        
    def test_str(self):
        self.assertEquals(5, size_str('abcde')) 
        self.assertEquals(0, size_str(''))
    
    def test_name_for_type(self):
        self.assertEquals('byte', name_for_type(BYTE_TYPE_ID))
        self.assertEquals('string', name_for_type(STRING_TYPE_ID))
        
        self.assertEquals('indicator', name_for_type(0)) 
        self.assertEquals('unknown(200)', name_for_type(200))
            
