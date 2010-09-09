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

def decode_prefix(byte):
   fixedwidth = (byte & 0x80) != 0
   has_name = (byte & 0x08) != 0
   has_ordinal = (byte & 0x10) != 0
   variablewidth = (byte & 0x60) >>5
   if variablewidth == 3:
       variablewidth = 4
   return (fixedwidth, variablewidth, has_ordinal, has_name) 
 
   
def encode_prefix(fixedwidth, variablewidth, has_ordinal, has_name):
   byte = 0x00
   if fixedwidth:
       byte = byte | 0x80
   if has_name:
       byte = byte | 0x08
   if has_ordinal:
       byte = byte | 0x10
   if variablewidth > 0:
       if variablewidth == 4:
           varwidth = 3
       else:
           varwidth = variablewidth
       byte = byte | varwidth << 5
   return byte

def calculate_variable_width(length):
    if length <= 255:
        return 1
    elif length < 2**15 -1 :
        return 2
    else:
        return 4
    
class FieldPrefix:
    def __init__(self, byte):
        (self.fixedwidth, self.variablewidth, self.has_ordinal, self.has_name) = \
            decode_prefix(byte)
    
    def _repr__(self):
        return "Prefix[fixedwidth=%r, variable=%r, has_ordinal=%r, has_name=%r]"% \
          (self.fixedwidth, self.variablewidth, self.has_ordinal, self.has_name)
    
    def encode(self):
        return encode_prefix(self.fixedwidth, self.variablewidth, self.has_ordinal, self.has_name)

       