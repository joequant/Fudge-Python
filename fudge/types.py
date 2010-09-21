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

"""Functions for working with types. """

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
# No 16
BYTEARRAY4_TYPE_ID = 17
BYTEARRAY8_TYPE_ID = 18
BYTEARRAY16_TYPE_ID = 19
BYTEARRAY20_TYPE_ID = 20
BYTEARRAY32_TYPE_ID = 21
BYTEARRAY64_TYPE_ID = 22
BYTEARRAY128_TYPE_ID = 23
BYTEARRAY256_TYPE_ID = 24
BYTEARRAY512_TYPE_ID = 25

FUDGE_TYPE_NAMES =  {
    0 : "indicator",
    1 : "boolean",
    2 : "byte",
    3 : "short",
    4 : "int",
    5 : "long",
    6 : "byte[]",
    SHORTARRAY_TYPE_ID : "short[]",
    INTARRAY_TYPE_ID : "int[]",
    LONGARRAY_TYPE_ID : "long[]",
    FLOAT_TYPE_ID : "float",
    DOUBLE_TYPE_ID : "double",
    FLOATARRAY_TYPE_ID : "float[]",
    DOUBLEARRAY_TYPE_ID :"double[]",
    STRING_TYPE_ID : "string",           
    FUDGEMSG_TYPE_ID : "message",
    BYTEARRAY4_TYPE_ID : "byte[4]",
    BYTEARRAY8_TYPE_ID : "byte[8]",
    BYTEARRAY16_TYPE_ID : "byte[16]",
    BYTEARRAY20_TYPE_ID : "byte[20]",
    BYTEARRAY32_TYPE_ID : "byte[32]",
    BYTEARRAY64_TYPE_ID : "byte[64]",
    BYTEARRAY128_TYPE_ID : "byte[128]",
    BYTEARRAY256_TYPE_ID : "byte[256]",
    BYTEARRAY512_TYPE_ID : "byte[512]",
}   

def name_for_type(type_id):
    """Return the human friendly name of a Fudge Type.
    
    Arguments:
        type_id:  the ID of the Type
        
    Return:
        The name of the type, if known, otherwise 'unknown(type_id)'
    """
    try:
        return FUDGE_TYPE_NAMES[type_id]
    except KeyError:
        return 'unknown(%s)'%type_id


def size_unicode(arg):
    """Calculate the size of a unicode string"""
    return len(arg.encode('utf-8'))
    
def size_str(arg):
    """Return the size of a bytestring"""  
    return len(arg)

class Indicator(object): 
    """A instance of a Fudge Indicator object.
    
    This is a zero-length type, and we nornally just return
    this singleton instance."""
    pass
    
    def __repr(self):
        return "Indicator()"
INDICATOR = Indicator()            