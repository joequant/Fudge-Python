#
# Copyright CERN, 2010
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

import struct

from fudge.codecs import enc_byte, enc_short
from fudge.registry import Registry
from fudge.prefix import encode_prefix, decode_prefix, calculate_variable_width

HEADER_PACKING="!BBhl"

REGISTRY = Registry()

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
        # TODO - deal with Taxonomy
        if self.name:
            # one for size prefix
            size = size + 1
            size = size + len(self.name) # TODO - wrong !

        if self.type_.is_variable_sized:
            # TODO - deal with varlength
            pass
        else:
            size = size + self.type_.fixed_size
        return size

    def __repr__(self):
        if self.name and not self.ordinal:
            return "Field[%s:%r-%s]"%(self.name, self.type_.type_id, self.value)
        elif self.name and self.ordinal:
            return "Field[%s,%d:%r-%s]"%(self.name, self.ordinal, self.type_.type_id, self.value)
        else:
            return "Field[%r-%s]"%(self.type_.type_id, self.value)

    def encode(self, writer):
        """Encode a Field.

        This encodes Field Prefix, Type, Ordinal, Name, Data
        """
        if self.type_.is_variable_sized:
            fixed_width = False
            variable_width = calculate_variable_width(len(self.value))
        else:
            fixed_width = True
            variable_width = 0

        writer.write(chr(encode_prefix(fixed_width, variable_width, \
            self.ordinal is not None, self.name is not None)))
        writer.write(enc_byte(self.type_.type_id))
        if self.ordinal:
            writer.write(enc_short(self.ordinal))
        if self.name:
            length = chr(len(self.name))
            writer.write(length)
            writer.write(self.name)
        writer.write(self.type_.encoder(self.value))

class Message:
    def __init__(self):
        self.fields = []

    def size(self):
        """Compute the size for the fields in the message."""
        size = 0
        for f in self.fields:
            size = size + f.size()
        return size

    def add(self, value, name=None, ordinal=None, type_=None, class_=None):
        """Add a new value to the message"""
        if not type_:
            # Try and work it out
            type_ = REGISTRY.type_by_class(value, class_=class_)

        type_ = REGISTRY.narrow(type_, value)
        self.fields.append(Field(type_, ordinal, name, value),)

    def encode(self, writer):
        for field in self.fields:
             field.encode(writer)
             

class Envelope:
    def __init__(self, message, directives=0, schema_version=0,taxonomy=0):
        self.message = message

        self.schema_version = schema_version
        self.directives = directives
        self.taxonomy = taxonomy


    def __str__(self):
        return "Envelope(%r, %r, %r, %r)"% \
            (self.directives, self.schema_version, self.taxonomy, self.message)

    def encode(self, writer):
        """Encode an envelope"""

        size = self.message.size() + struct.calcsize(HEADER_PACKING)
        writer.write(struct.pack(HEADER_PACKING, self.directives, self.schema_version, \
             self.taxonomy, size))

        self.message.encode(writer)

    @classmethod
    def decode(cls, bytes):
        # XXX - throw exception on message length < 8
        (directives, schema_version, taxonomy, size) = struct.unpack(HEADER_PACKING, bytes[:8])
        width = size - struct.calcsize(HEADER_PACKING)
        m = Message()
        e = Envelope(m, directives, schema_version, taxonomy)

        # XXX - Decode message

        return e