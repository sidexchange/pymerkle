"""
Provides JSON encoders used implicitly for serialization accross this library
"""
import json


class MerkleTreeSerializer(json.JSONEncoder):
    """Used implicitly in the JSON serialization of Merkle-trees.
    Extends the built-in JSON encoder for data structures.
    """

    def default(self, obj):
        """ Overrides the built-in method of JSON encoders according to the needs of this library
        """
        try:
            hash_type, encoding, security = obj.hash_type, obj.encoding, obj.security
            leaves = obj.leaves
        except TypeError:
            return json.JSONEncoder.default(self, obj)
        else:
            return {
                'header': {
                    'hash_type': hash_type,
                    'encoding': encoding,
                    'security': security},
                'hashes': [
                    leaf.stored_hash.decode(
                        encoding=encoding) for leaf in leaves]}


class NodeSerializer(json.JSONEncoder):
    """Used implicitly in the JSON serialization of nodes.
    Extends the built-in JSON encoder for data structures.
    """

    def default(self, obj):
        """ Overrides the built-in method of JSON encoders according to the needs of this library.
        """
        try:
            left, right = obj.left, obj.right
            hash = obj.stored_hash
        except TypeError:
            return json.JSONEncoder.default(self, obj)
        else:
            if isinstance(obj, Leaf):
                return {
                    'hash': hash.decode(encoding=obj.encoding)
                }
            return {
                'left': left.serialize(),
                'right': right.serialize(),
                'hash': hash.decode(encoding=obj.encoding)
            }  # Non-leaf case


class ProofSerializer(json.JSONEncoder):
    """Used implicitly in the JSON serialization of proofs.
    Extends the built-in JSON encoder for data structures.
    """

    def default(self, obj):
        """ Overrides the built-in method of JSON encoders according to the needs of this library
        """
        try:
            uuid = obj.header['uuid']
            generation = obj.header['generation']
            timestamp = obj.header['timestamp']
            creation_moment = obj.header['creation_moment']
            provider = obj.header['provider']
            hash_type = obj.header['hash_type']
            encoding = obj.header['encoding']
            security = obj.header['security']
            proof_index = obj.body['proof_index']
            proof_path = obj.body['proof_path']
            status = obj.header['status']
        except TypeError:
            return json.JSONEncoder.default(self, obj)
        else:
            return {
                'header': {
                    'uuid': uuid,
                    'generation': generation,
                    'timestamp': timestamp,
                    'creation_moment': creation_moment,
                    'provider': provider,
                    'hash_type': hash_type,
                    'encoding': encoding,
                    'security': security,
                    'status': status
                },
                'body': {
                    'proof_index': proof_index,
                    'proof_path': [
                        [sign, hash
                            if isinstance(hash, str) else hash.decode(encoding=encoding)
                         ] for (sign, hash) in proof_path]if proof_path is not None else []
                }
            }


class ValidationReceiptSerializer(json.JSONEncoder):
    """Used implicitly in the JSON serialization of validation receipts.
    Extends the built-in JSON encoder for data structures.
    """

    def default(self, obj):
        """ Overrides the built-in method of JSON encoders according to the needs of this library
        """
        try:
            uuid = obj.header['uuid']
            timestamp = obj.header['timestamp']
            validation_moment = obj.header['validation_moment']
            proof_uuid = obj.body['proof_uuid']
            proof_provider = obj.body['proof_provider']
            result = obj.body['result']
        except TypeError:
            return json.JSONEncoder.default(self, obj)
        else:
            return {
                'header': {
                    'uuid': uuid,
                    'timestamp': timestamp,
                    'validation_moment': validation_moment
                },
                'body': {
                    'proof_uuid': proof_uuid,
                    'proof_provider': proof_provider,
                    'result': result
                }
            }
