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
 
from fudge.codecs import *

INDICATOR_TYPE_ID = 0
BOOLEAN_TYPE_ID = 1
BYTE_TYPE_ID = 2
SHORT_TYPE_ID = 3
INT_TYPE_ID = 4
LONG_TYPE_ID = 5
  
STRING_TYPE_ID = 14
       

class UnknownType(Exception):
    pass
    
class FieldType:
    """"""
    def __init__(self, type_id, class_, is_variable_sized, fixed_size,
                 encoder = None, decoder = None):         
        """Create a new Field type.  
    
        Arguments:
        type_id : the Fudge Type Identifier
        class : The python class this maps to
        is_variable_sized:  
        fixed_size : the fixed size of the type
    
        """
        self.type_id = type_id
        self.class_ = class_
        self.is_variable_sized = is_variable_sized
        self.fixed_size = fixed_size
        self.encoder = encoder 
        self.decoder = decoder
           
    def __repr__(self):
        return "FieldType(%r, %r, %r, %r)"%(self.type_id, self.class_, self.is_variable_sized, self.fixed_size) 
        
        
class Registry:
    """A Fudge Type registry.
    
    """
    def __init__(self):
        self.types_by_id = {} 
        self.types_by_class = {}

        self._add(FieldType(INDICATOR_TYPE_ID, None, False, 0))
        self._add(FieldType(BOOLEAN_TYPE_ID, bool, False, 1, enc_bool))
        self._add(FieldType(BYTE_TYPE_ID, int, False, 1, enc_byte))
        self._add(FieldType(SHORT_TYPE_ID, int, False, 2, enc_short))  
        self._add(FieldType(INT_TYPE_ID, int, False, 4, enc_int))  
        self._add(FieldType(LONG_TYPE_ID, long, False, 8, enc_long))  
        
        self._add(FieldType(STRING_TYPE_ID, unicode, True, 0, enc_unicode))  
        
        self.NARROWERS = {
            SHORT_TYPE_ID: self._narrow_int,
            INT_TYPE_ID: self._narrow_int,
        }
        
    def _add(self, field_type):
        self.types_by_id[field_type.type_id] = field_type 
        self.types_by_class[field_type.class_] = field_type 
    
    def type_by_id(self, type_id):
        try:
            return self.types_by_id[type_id] 
        except KeyError:
            raise UnknownType("Did not recognize ID : %s"%type_id) 
            
    def type_by_class(self, value, class_= None):
        if not class_:
            class_ = value.__class__
        
        try:
            return self.types_by_class[class_]
        except KeyError:
            raise UnknownType("No type mapping for class : %s"%class_)    
            
            
    def narrow(self, type_, value):
        """Narrow a type if the value can fit into a smaller type."""  
        
        if not self.NARROWERS.has_key(type_.type_id):
            return type_    
        return self.NARROWERS[type_.type_id](value)
     
    def _narrow_int(self, value):
        if value <= 255:
            return self.types_by_id[BYTE_TYPE_ID]
        elif value <= 2**15-1:
            return self.types_by_id[SHORT_TYPE_ID]
        else: 
            return  self.types_by_id[INT_TYPE_ID]