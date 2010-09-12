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
 
from fudge import codecs
from fudge import prefix  
from fudge import registry
from fudge import types
from fudge import utils

REGISTRY = registry.DEFAULT_REGISTRY

class Field:
    """A Concrete field suitable for including into Message""" 
    
    def __init__(self, type_, ordinal, name, value):
        self.type_ = type_
        self.ordinal = ordinal
        self.name = name
        self.value = value

    def size(self):
        """Calculate the size that the field will take up in the message"""
        size = 2 # prefix
        if self.ordinal:
            size = size + 2
        # TODO(jamesc) - deal with Taxonomy
        if self.name:
            # one for size prefix
            size = size + 1 + types.size_unicode(self.name)
            
        if self.type_.is_variable_sized: 
            # We store a variable sized length and then the value itself
            value_size = self.type_.calc_size(self.value)
            size = size + bytes_for_var_size(value_size) + value_size
        else:
            size = size + self.type_.fixed_size
        return size

    def __repr__(self):
        if self.name and not self.ordinal:
            return "Field[%s:%s-%s]"%(self.name, self.type_, self.value)
        elif self.name and self.ordinal:
            return "Field[%s,%d:%s-%s]"%(self.name, self.ordinal, self.type_, self.value)
        else:
            return "Field[%s-%s]"%(self.type_, self.value)

    def encode(self, writer):
        """Encode a Field.

        This encodes Field Prefix, Type, Ordinal, Name, Data
        """
        fixed_width = True
        variable_width = 0
        if self.type_.is_variable_sized:
            fixed_width = False 
            value_length = self.type_.calc_size(self.value)
            variable_width = bytes_for_var_size(value_length)
            

        writer.write(chr(prefix.encode_prefix(fixed_width, variable_width, \
            self.ordinal is not None, self.name is not None)))
        writer.write(codecs.enc_byte(self.type_.type_id))
        if self.ordinal:
            writer.write(codecs.enc_short(self.ordinal))
        if self.name:
            assert len(self.name) <= utils.MAX_BYTE 
            writer.write(codecs.enc_name(self.name)) 
        
        if not fixed_width:
            encode_value_length(value_length, writer)
            
        writer.write(self.type_.encoder(self.value))
       
    
    @classmethod
    def decode(cls, bytes):
        """Decode a field from a byte array.
        
        Returns:
          (field, num_read).
          
          field: the field read from the byte array
          num_read: number of bytes this field took up
          
        Raises:
          Error: if there is not enough bytes in the array for the field."""
        
        assert len(bytes) > 2
        
        # prefix
        fixedwidth, variablewidth, has_ordinal, has_name = prefix.decode_prefix(ord(bytes[0]))
        id = ord(bytes[1])
        field_type = REGISTRY[id]
        size = 2
        
        # ordinal
        ordinal = None
        if has_ordinal:
            ordinal = codecs.dec_short(bytes[size:])
            size = size + 2 
         
        # name   
        name = None
        if has_name:
            name_len = ord(bytes[size])  
            name = codecs.dec_unicode(bytes[size+1:size+name_len+1]) 
            size = size + name_len + 1 # length encoded as 1
            
        # value
        if fixedwidth:
            value = field_type.decoder(bytes[size:])
            size = size + field_type.fixed_size
        else:
            value_length = calc_length(bytes[size:], variablewidth) 
            value = field_type.decoder(bytes[size+1:size+value_length+1])
            size = size + value_length + bytes_for_var_size(value_length)
            
        field = Field(field_type, ordinal, name, value)
        return field, size

def bytes_for_var_size(var_size):
    if var_size <= utils.MAX_BYTE:
        return 1
    elif var_size <= utils.MAX_SHORT:
        return 2
    else:
        return 4

def encode_value_length(value_length, writer):
    if value_length <= utils.MAX_BYTE:
        writer.write(codecs.enc_byte(value_length)) 
    elif value_length <= utils.MAX_SHORT:
        writer.write(codecs.enc_short(value_length))
    else:
        writer.write(codecs.enc_int(value_length))
        
def calc_length(bytes, width):
    if width == 1:
        return codecs.dec_byte(bytes[0])
    elif width == 2:
        return codecs.dec_short(bytes[0:1])
    else:
        return codecs.dec_int(bytes[0:3])