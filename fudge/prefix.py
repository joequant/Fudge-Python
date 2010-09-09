# encoding: utf-8
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

def decode(byte):
   fixedwidth = (byte & 0x80) != 0
   name = (byte & 0x08) != 0
   ordinal = (byte & 0x10) != 0
   variablewidth = (byte & 0x60) >>5
   if variablewidth == 3:
       variablewidth = 4
   return (fixedwidth, variablewidth, ordinal, name) 
 
   
def encode(fixedwidth, variablewidth, ordinal, name):
   byte = 0x00
   if fixedwidth:
       byte = byte | 0x80
   if name:
       byte = byte | 0x08
   if ordinal:
       byte = byte | 0x10
   if variablewidth > 0:
       if variablewidth == 4:
           varwidth = 3
       else:
           varwidth = variablewidth
       byte = byte | varwidth << 5
   return byte

class FieldPrefix:
    def __init__(self, byte):
        (self.fixedwidth, self.variablewidth, self.ordinal, self.name) = \
            decode(byte)
    
    def _repr__(self):
        return "Prefix(%r, %r, %r, %r)"% \
          (self.fixedwidth, self.variablewidth, self.ordinal, self.name)
    
    def encode(self):
        return encode(self.fixedwidth, self.variablewidth, self.ordinal, self.name)

       