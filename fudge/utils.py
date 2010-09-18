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

"""Some utility functions, constants and classes"""

from  cStringIO import StringIO

from fudge import types

MIN_BYTE = 0
MAX_BYTE = 255

MIN_SHORT = -32768
MAX_SHORT = 32767

MIN_INT = -2147483648
MAX_INT = 2147483647 

MIN_LONG = long(-2**63)
MAX_LONG = long(2**63-1)
      

class PrettyPrinter(object):
    """A PrettyPrinter for Fudge messages.
     
    Based on the Java FudgeMsgFormatter.
    
    """
    
    """The default indentation amount for a Pretty Printer : 2 """
    DEFAULT_INDENT = 2    
 
    

    def __init__(self, writer, indent = DEFAULT_INDENT):
        """Create a new PrettyPrinter
        
        Arguments:
            writer:  the writer stream to output to
            indent:  how much to indent a sub-message (Default:2)
        """
        self._writer = writer
        self._indent = indent
        self._indentText = u' '*self._indent 
        
    def format(self, message, depth=0): 
        """Output a formatted message to the underlying writer
        
        Arguments:
            message:  the message to write
            depth:  The depth of this message/sub-message (Default:0)
            
        """
        fields = message.fields
        max_typename_width = -1  
        fieldspecs = []
        for field, index in zip(fields, range(0, len(fields))):
            fieldspec = self._get_fieldspec(field, index, depth)
            fieldspecs.append(fieldspec) 
       
        max_fieldspec_width = len(max(fieldspecs, key=str.__len__))
        max_typename_width = len(max(map(lambda x : types.name_for_type(x.type_), fields), key=str.__len__))

        for field, fieldspec, index in  zip(fields, fieldspecs, range(0, len(fields))) :
            self._format_field(field, fieldspec, index, depth, \
                    max_fieldspec_width, max_typename_width)

    def _format_field(self, field, fieldspec, index, depth, max_fs, max_tn):
        """Format a single field on a line"""
        typename = types.name_for_type(field.type_)
        self._writer.write("{0:<{width}} {1:<{tn_width}} ".format(fieldspec, typename, width=max_fs, tn_width=max_tn) )
        if field.is_type(types.FUDGEMSG_TYPE_ID):
            format(field.value, depth + 1)
        else:
            self._write_typed_value(field.type_, field.value)
        self._writer.write('\n')
        self._writer.flush()

    def _get_fieldspec(self, field, index, depth):
        """Create a string representation of a Field specification header.
        
        Arguments:
            field : The field
            index : Index within the current message of this field
            depth : Depth of current message 
        Return:
            Formatted string representation of the Field header
            
        """
        buf = StringIO() 
        for i in range(0, depth):
            buf.write(self._indentText)
        buf.write("%d"%index) 
        buf.write('-')
        if field.ordinal:
            buf.write('(%s)'%field.ordinal)
            if field.name:
                buf.write(' ') 
        if field.name:
            buf.write(field.name)
        return buf.getvalue()
    
    def _outputArray(self, value, truncate=8):
        num_elements = len(value)
        if truncate > num_elements:
            truncate = num_elements 
        self._writer.write('[')
        for i in range(0, truncate):
            self._writer.write(str(value[i]))
            if i + 1 < truncate:
                self._writer.write(', ')
        if truncate < num_elements:
            self._writer.write(" ... %s more"%(num_elements - truncate))
        self._writer.write(']')
         
    def _write_typed_value(self, type_, value):
        renderers = {
            types.SHORTARRAY_TYPE_ID : self._outputArray,
            types.FLOATARRAY_TYPE_ID : self._outputArray,
            types.DOUBLEARRAY_TYPE_ID : self._outputArray,
            types.INTARRAY_TYPE_ID : self._outputArray,
            types.LONGARRAY_TYPE_ID : self._outputArray,
            types.BYTEARRAY_TYPE_ID : self._outputArray,
            types.BYTEARRAY4_TYPE_ID : self._outputArray,
            types.BYTEARRAY8_TYPE_ID : self._outputArray,
            types.BYTEARRAY16_TYPE_ID : self._outputArray,
            types.BYTEARRAY20_TYPE_ID : self._outputArray,
            types.BYTEARRAY32_TYPE_ID : self._outputArray,
            types.BYTEARRAY64_TYPE_ID : self._outputArray,
            types.BYTEARRAY128_TYPE_ID : self._outputArray,
            types.BYTEARRAY256_TYPE_ID : self._outputArray,
            types.BYTEARRAY512_TYPE_ID : self._outputArray,
        
        }   
        
        try : 
            renderers[type_.type_id](value)
        except KeyError:
            self._writer.write(str(value))
           