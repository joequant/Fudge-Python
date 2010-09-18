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
      
"""A Registry, storing Fudge FieldTypes."""

from fudge import codecs
from fudge import types
from fudge import utils

INDICATOR_TYPE_ID = 0
BOOLEAN_TYPE_ID = 1
BYTE_TYPE_ID = 2
SHORT_TYPE_ID = 3
INT_TYPE_ID = 4
LONG_TYPE_ID = 5
BYTEARRAY_TYPE_ID = 6 
SHORTARRAY_TYPE_ID = 7
INTARRAY_TYPE_ID = 8
LONGARRAY_TYPE_ID = 9
FLOAT_TYPE_ID = 10
DOUBLE_TYPE_ID = 11 
FLOATARRAY_TYPE_ID = 12
DOUBLEARRAY_TYPE_ID = 13
STRING_TYPE_ID = 14
FUDGEMSG_TYPE_ID = 15
BYTEARRAY4_TYPE_ID = 17
BYTEARRAY8_TYPE_ID = 18
BYTEARRAY16_TYPE_ID = 19
BYTEARRAY20_TYPE_ID = 20
BYTEARRAY32_TYPE_ID = 21
BYTEARRAY64_TYPE_ID = 22
BYTEARRAY128_TYPE_ID = 23
BYTEARRAY256_TYPE_ID = 24
BYTEARRAY512_TYPE_ID = 25


class UnknownType(Exception): 
    pass
    
class FieldType(object):
    """"""
    def __init__(self, type_id, class_, is_variable_sized, fixed_size,
                 encoder=None, decoder=None, calc_size=None):         
        """Create a new Field type.  
    
        Arguments:
        type_id : the Fudge Type Identifier
        class : The python class this maps to
        is_variable_sized:  
        fixed_size : the fixed size of the type
         
        encoder : Convert from object to bytes 
            def encoder(obj) -> bytes
        decoder : Convert from bytes to object
            def decoder(bytes) -> object, bytes_read
            
        calc_size : if is_variable_sized is True, calculate the size needed
                to hold this object
            def size(object) -> num_bytes
        """
        self.type_id = type_id
        self.class_ = class_
        self.is_variable_sized = is_variable_sized
        self.fixed_size = fixed_size
        self.encoder = encoder 
        self.decoder = decoder
        self.calc_size = calc_size
         
        if self.is_variable_sized:
            assert self.calc_size
              
    def __repr__(self):
        return "FieldType[id=%r, class=%r]"%(self.type_id, self.class_)


class Registry(object):
    """A Fudge Type registry.
    
    """
    def __init__(self):
        self.types_by_id = {} 
        self.types_by_class = {}

        self._add(FieldType(INDICATOR_TYPE_ID, None, False, 0, \
                codecs.enc_indicator, codecs.dec_indicator, lambda x : 0))

        self._add(FieldType(BOOLEAN_TYPE_ID, bool, False, 1, \
                codecs.enc_bool, codecs.dec_bool))
        self._add(FieldType(BYTE_TYPE_ID, int, False, 1, \
                codecs.enc_byte, codecs.dec_byte))
        self._add(FieldType(SHORT_TYPE_ID, int, False, 2, \
                codecs.enc_short, codecs.dec_short))
        self._add(FieldType(INT_TYPE_ID, int, False, 4, \
                codecs.enc_int, codecs.dec_int))
        self._add(FieldType(LONG_TYPE_ID, long, False, 8, \
                codecs.enc_long, codecs.dec_long))

        self._add(FieldType(BYTEARRAY_TYPE_ID, str, True, 0, \
                codecs.enc_str, codecs.dec_str, types.size_str))
        self._add(FieldType(SHORTARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_short, x), \
                lambda x : codecs.dec_array(codecs.dec_short, 2, x), \
                lambda x : 2 * len(x)))
        self._add(FieldType(INTARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_int, x), \
                lambda x : codecs.dec_array(codecs.dec_int, 4, x), \
                lambda x : 4 * len(x)))
        self._add(FieldType(LONGARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_long, x), \
                lambda x : codecs.dec_array(codecs.dec_long, 8, x), \
                lambda x : 8 * len(x)))
                        
        self._add(FieldType(FLOAT_TYPE_ID, float, False, 4, \
                codecs.enc_float, codecs.dec_float))
        self._add(FieldType(DOUBLE_TYPE_ID, float, False, 8, \
                codecs.enc_double, codecs.dec_double))
        self._add(FieldType(FLOATARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_float, x), \
                lambda x : codecs.dec_array(codecs.dec_float, 4, x), \
                lambda x : 4 * len(x)))
        self._add(FieldType(INTARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_double, x), \
                lambda x : codecs.dec_array(codecs.dec_double, 8, x), \
                lambda x : 8 * len(x)))
        
        self._add(FieldType(STRING_TYPE_ID, unicode, True, 0, \
                codecs.enc_unicode, codecs.dec_unicode, types.size_unicode))

        self._add(FieldType(FUDGEMSG_TYPE_ID, None, True, 
                None, None, calc_size = lambda x : x.size()))

        self._add(FieldType(BYTEARRAY4_TYPE_ID, str, False, 4, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY8_TYPE_ID, str, False, 8, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY16_TYPE_ID, str, False, 16, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY20_TYPE_ID, str, False, 20, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY32_TYPE_ID, str, False, 32, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY64_TYPE_ID, str, False, 64, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY128_TYPE_ID, str, False, 128, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY256_TYPE_ID, str, False, 256, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(BYTEARRAY512_TYPE_ID, str, False, 512, \
                codecs.enc_str, codecs.dec_str))

        
        self._narrower_fns = {
            BYTE_TYPE_ID: self._narrow_int,
            SHORT_TYPE_ID: self._narrow_int,
            INT_TYPE_ID: self._narrow_int, 
            LONG_TYPE_ID: self._narrow_int,
            
            BYTEARRAY_TYPE_ID: self._narrow_str,
            BYTEARRAY4_TYPE_ID: self._narrow_str,
            BYTEARRAY8_TYPE_ID: self._narrow_str,
            BYTEARRAY16_TYPE_ID: self._narrow_str,
            BYTEARRAY20_TYPE_ID: self._narrow_str,
            BYTEARRAY32_TYPE_ID: self._narrow_str,
            BYTEARRAY64_TYPE_ID: self._narrow_str,
            BYTEARRAY128_TYPE_ID: self._narrow_str,
            BYTEARRAY256_TYPE_ID: self._narrow_str,
            BYTEARRAY512_TYPE_ID: self._narrow_str,
            
        }
     
    def __getitem__(self, key):
        return self.types_by_id[key]
           
    def _add(self, field_type):
        self.types_by_id[field_type.type_id] = field_type 
        if field_type.class_:
            self.types_by_class[field_type.class_] = field_type 
    
    def type_by_id(self, type_id):
        """Given a type_id return the Fudge FieldType which 
        it represents.
        
        Arguments:
           type_id: the Fudge Type ID
           
        Return:
          The FieldType object for the Type Id
          
        Raise:
          UnknownType: if we can't find a suitable class in the registry"""
        try:
            return self.types_by_id[type_id] 
        except KeyError:
            raise UnknownType("Did not recognize ID : %s"%type_id) 
            
    def type_by_class(self, value, class_=None): 
        """Given a value and an optional class return the Fudge FieldType which 
        can hold it.
        
        Arguments:
           value: the object to find a class for                                        
           class_: The class we wish to map to. (default: None)
           
        Return:
          A FieldType which can hold the object
          
        Raise:
          UnknownType if we can't find a suitable class in the registry"""
        if not class_:
            class_ = value.__class__
        try:
            return self.types_by_class[class_]
        except KeyError:
            raise UnknownType("No type mapping for class : %s"%class_)    
            
    def narrow(self, type_, value):
        """Narrow a type if the value can fit into a smaller type."""  
        
        if type_.type_id not in self._narrower_fns:
            return type_
        return self._narrower_fns[type_.type_id](value)
     
    def _narrow_int(self, value):
        if value >= utils.MIN_BYTE and value <= utils.MAX_BYTE:
            return self[BYTE_TYPE_ID]
        elif value >= utils.MIN_SHORT and value <= utils.MAX_SHORT:
            return self[SHORT_TYPE_ID]
        elif value >= utils.MIN_INT and value <= utils.MAX_INT:
            return self[INT_TYPE_ID]
        else: 
            return  self[LONG_TYPE_ID]
 
    def _narrow_str(self, value): 
        
        fixed_bytelen = { 4: self[BYTEARRAY4_TYPE_ID],
                8: self[BYTEARRAY8_TYPE_ID],
                16: self[BYTEARRAY16_TYPE_ID],
                20: self[BYTEARRAY20_TYPE_ID],
                32: self[BYTEARRAY32_TYPE_ID],
                64:  self[BYTEARRAY64_TYPE_ID],
                128:  self[BYTEARRAY128_TYPE_ID],
                256: self[BYTEARRAY256_TYPE_ID],
                512: self[BYTEARRAY512_TYPE_ID],
            } 
        array_len = len(value)
        if array_len in fixed_bytelen:
            return fixed_bytelen[array_len]
        return self[BYTEARRAY_TYPE_ID]
        
            
            
DEFAULT_REGISTRY = Registry()
