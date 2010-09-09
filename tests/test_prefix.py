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

from fudge.prefix import FieldPrefix  

class FieldPrefixTests(unittest.TestCase):
    def setUp(self):
        pass
     
    def testCreate(self):
        p = FieldPrefix(0x98)  # fixed, ordinal, name
        self.assertTrue(p.fixedwidth)
        self.assertTrue(p.has_ordinal)
        self.assertTrue(p.has_name)
        self.assertEquals(0, p.variablewidth) 
        
        byte = p.encode()                                   
        self.assertEquals(0x98, byte)
     
    def testVariableWidth(self): 
        """There are 4 varwidth options"""
        ZERO = 0x00 # 0000 0000
        ONE = 0x20  # 0010 0000
        TWO = 0x40  # 0100 0000
        FOUR = 0x60 # 0110 0000      
        
        p = FieldPrefix(ZERO)
        self.assertFalse(p.fixedwidth) 
        self.assertEquals(0, p.variablewidth) 
        byte = p.encode()                                   
        self.assertEquals(ZERO, byte)
                           
        p = FieldPrefix(ONE)
        self.assertFalse(p.fixedwidth) 
        self.assertEquals(1, p.variablewidth)
        byte = p.encode()                                   
        self.assertEquals(ONE, byte)

        p = FieldPrefix(TWO)
        self.assertFalse(p.fixedwidth) 
        self.assertEquals(2, p.variablewidth)
        byte = p.encode()                                   
        self.assertEquals(TWO, byte)

        p = FieldPrefix(FOUR)
        self.assertFalse(p.fixedwidth) 
        self.assertEquals(4, p.variablewidth) 
        byte = p.encode()                                   
        self.assertEquals(FOUR, byte) 
         
if __name__ == '__main__':
    unittest.main()