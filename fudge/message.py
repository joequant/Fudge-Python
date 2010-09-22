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

from fudge.field import Field
from fudge import registry

HEADER_PACKING = "!BBhl"

class Message(object):
    """A Fudge Message.

    """

    def __init__(self, registry=registry.Registry()):
        self.fields = []
        self.registry = registry


    def __str__(self):
        return "Message[fields=%s]"%self.fields

    def size(self, taxonomy=None):
        """Compute the size for the fields in the message."""
        size = 0
        for field in self.fields:
            size = size + field.size(taxonomy)
        return size

    def add(self, value, name=None, ordinal=None, type_=None, classname=None):
        """Add a new value to the message"""
        if not type_:
            # Try and work it out
            type_ = self.registry.type_by_class(value, classname=classname)

        type_ = self.registry.narrow(type_, value)
        self._add_field(Field(type_, ordinal, name, value),)

    def _add_field(self, field):
        self.fields.append(field)

    def encode(self, writer, taxonomy=None):
        for field in self.fields:
            field.encode(writer, taxonomy)

    @classmethod
    def decode(cls, encoded, taxonomy=None):
        message = Message()
        while encoded:
            next_field, num_read = Field.decode(encoded, taxonomy)
            message._add_field(next_field)
            encoded = encoded[num_read:]
        return message

class Envelope(object):
    """A Fudge envelope.

    This contains a message, and holds the metadata for the message (Schema
    Version and Taxonomy used)"""
    def __init__(self, message, directives=0, schema_version=0, taxonomy_resolver=None):
        self.message = message
        self.schema_version = schema_version
        self.directives = directives
        self.taxonomy_resolver = None

    def __str__(self):
        return "Envelope(directives=%r, schema version=%r)"% \
            (self.directives, self.schema_version)

    def encode(self, writer, taxonomy_id=0):
        """Encode an envelope"""

        taxonomy = None
        if taxonomy_id:
            taxonomy = self.taxonomy_resolver.resolve_taxonomy(taxonomy_id)
        size = self.message.size(taxonomy) + struct.calcsize(HEADER_PACKING)

        writer.write(struct.pack(HEADER_PACKING, self.directives, \
                self.schema_version, taxonomy_id, size))

        self.message.encode(writer, taxonomy)

    @classmethod
    def decode(cls, encoded, taxonomy_resolver=None):
        # TODO(jamesc) - throw exception on message length < 8
        assert len(encoded) >= 8
        (directives, schema_version, taxonomy_id, size) = \
                struct.unpack(HEADER_PACKING, encoded[:8])
        width = size - struct.calcsize(HEADER_PACKING)

        # TODO(jamesc) - assert doesn't work for submsg
        # assert len(encoded) == width + 8
        taxonomy = None
        if taxonomy_resolver:
            taxonomy = taxonomy_resolver.resolve_taxonomy[taxonomy_id]

        message = Message.decode(encoded[8:], taxonomy=taxonomy)
        envelope = Envelope(message, directives, schema_version, taxonomy_resolver)
        return envelope