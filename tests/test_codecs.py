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
 
from fudge.codecs import *
from fudge import utils

class codecsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_bool(self):
        self.assertEquals('\x00', enc_bool(False))
        self.assertEquals('\x01', enc_bool(True))
        
        self.assertEquals(False, dec_bool('\x00'))
        self.assertEquals(True, dec_bool('\x01'))

    def test_byte(self):
        self.assertEquals('\x01', enc_byte(0x01)) 
        self.assertEquals(0x01, dec_byte('\x01'))
        
        self.assertEquals('\xff', enc_byte(255))
        self.assertEquals(' ', enc_byte(32)) 
    
    def test_short(self):
        self.assertEquals('\x80\x00', enc_short(utils.MIN_SHORT))
        self.assertEquals('\x7f\xff', enc_short(utils.MAX_SHORT))
   
        self.assertEquals(utils.MIN_SHORT, dec_short(enc_short(utils.MIN_SHORT)))
        self.assertEquals(utils.MAX_SHORT, dec_short(enc_short(utils.MAX_SHORT)))         
        
    def test_int(self):
        self.assertEquals('\x80\x00\x00\x00', enc_int(utils.MIN_INT))
        self.assertEquals('\x7f\xff\xff\xff', enc_int(utils.MAX_INT))
        
        self.assertEquals(utils.MIN_INT, dec_int(enc_int(utils.MIN_INT)))
        self.assertEquals(utils.MAX_INT, dec_int(enc_int(utils.MAX_INT)))
        
    def test_long(self):
        self.assertEquals('\x80\x00\x00\x00\x00\x00\x00\x00', enc_long(utils.MIN_LONG))
        self.assertEquals('\x7f\xff\xff\xff\xff\xff\xff\xff', enc_long(utils.MAX_LONG))

        self.assertEquals(utils.MIN_LONG, dec_long(enc_long(utils.MIN_LONG)))
        self.assertEquals(utils.MAX_LONG, dec_long(enc_long(utils.MAX_LONG)))
 
    def test_name(self):  
        self.assertEquals('\x00', enc_name(''))
        self.assertEquals('', dec_name('\x00'))
        
        self.assertEquals('\x07abcdefg', enc_name('abcdefg'))
        self.assertEquals('abcdefg', dec_name(enc_name('abcdefg'))) 
        