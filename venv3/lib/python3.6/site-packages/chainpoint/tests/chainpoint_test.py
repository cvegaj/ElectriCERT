import unittest
from ..chainpoint import Chainpoint

class ChainpointCommonTestCase(unittest.TestCase):
    def test_null_receipt(self):
        validator = Chainpoint()
        receipt = None
        with self.assertRaises(TypeError):
            validator.valid_receipt(receipt)

    def test_non_json_receipt(self):
        validator = Chainpoint()
        receipt = 'Adhf4saEOIJ'
        with self.assertRaises(ValueError):
            validator.valid_receipt(receipt)

    def test_number_receipt(self):
        validator = Chainpoint()
        receipt = '12345'
        with self.assertRaises(TypeError):
            validator.valid_receipt(receipt)

    def test_empty_receipt(self):
        validator = Chainpoint()
        receipt = '{}'
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Cannot identify Chainpoint version')

    def test_unsupported_version(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "0.9"
            }
        }'''
        with self.assertRaises(ValueError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid Chainpoint version: 0.9')


class Chainpointv1xTestCase(unittest.TestCase):
    def test_missing_hash_type(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1"
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing hash_type')

    def test_missing_target(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing target')

    def test_missing_root(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256"
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing tx_id')

    def test_missing_tx(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404"
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing target')

    def test_missing_timestamp(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a"
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing timestamp')

    def test_unsupported_hash_type(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "sha1"
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash type: sha1')

    def test_bad_root(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "bad-non-hash-value",
                "tx_id": "",
                "timestamp": 1458126637
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing target')

    def test_bad_tx(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "bad-tx-id-value"
            },
            "target" :{}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid hash value: bad-tx-id-value")

    def test_bad_timestamp(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": "sdfsdf"
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid timestamp: sdfsdf')

    def test_missing_target_hash(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing target_hash')

    def test_bad_target_hash(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_proof": {},
                "target_hash": "badhash"
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash value: badhash')

    def test_missing_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19"
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing target_proof')

    def test_bad_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": null
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid target_proof: None')

    def test_empty_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": ""
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid target_proof: ')

    def test_garbage_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": "kjeflwi"
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid target_proof: kjeflwi')

    def test_empty_object_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": {}
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid target_proof: {}')

    def test_bad_object_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": { "parent": "something" }
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid target_proof: {u'parent': u'something'}")

    def test_empty_list_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1458126637
            },
            "target": {
                "target_hash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
                "target_proof": []
            }
        }'''
        self.assertFalse(validator.valid_receipt(receipt))

    def test_invalid_target_proof_missing_parent(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Missing parent")

    def test_invalid_target_proof_bad_right(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [
                    {
                        "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                        "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                        "right": "cvbcvb"
                    },
                    {
                        "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                        "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                        "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                    }
                ]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid hash value: cvbcvb")

    def test_invalid_target_proof_parent_matching(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "bbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "b52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid proof path")

    def test_invalid_target_proof_parent_matching_target_hash0(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "11da53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid proof path")

    def test_invalid_target_proof_parent_matching_target_hash1(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "5f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Invalid proof path")

    def test_invalid_target_proof_missing_left(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, "Missing left")

    def test_invalid_target_proof_parent_merkle_matching(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "6faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        self.assertFalse(validator.valid_receipt(receipt))

    def test_valid_empty_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "tx_id": "6d14a219a9aef975377bad9236cbc4e1e062cb5dd29b3dd3c1a1cb63540c1c9a",
                "timestamp": 1463018411
            },
            "target": {
                "target_hash": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
                "target_proof": []
            }
        }'''
        self.assertTrue(validator.valid_receipt(receipt))

    def test_valid_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        self.assertTrue(validator.valid_receipt(receipt))


class Chainpointv2TestCase(unittest.TestCase):
    def test_unsupported_version(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v35",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid Chainpoint type: ChainpointSHA256v35')

    def test_unsupported_version2(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v35"
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid Chainpoint type: ChainpointSHA256v35')

    def test_missing_hash_type(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "Chainpointv2",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid Chainpoint type: Chainpointv2')

    def test_unsupported_hash_type(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA2048v2",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid Chainpoint type: ChainpointSHA2048v2')

    def test_missing_target_hash(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing targetHash')

    def test_invalid_target_hash(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "invalid",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash value: invalid')

    def test_missing_merkle_root(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "proof": []
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing merkleRoot')

    def test_invalid_merkle_root(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "invalid",
            "proof": {}}'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash value: invalid')

    def test_missing_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404"
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing proof')

    def test_missing_target_proof97861(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": null
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing proof')

    def test_invalid_target_proof3(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": "invalid"
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid path')

    def test_invalid_target_proof2(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": {}
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing proof')

    def test_invalid_target_proof3(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": { "tree": "orange tree" }
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Missing proof')

    def test_invalid_empty_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": []
        }'''
        self.assertFalse(validator.valid_receipt(receipt))

    def test_invalid_missing_left_right_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": [{ "parent": "something" }]
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid proof path')

    def test_invalid_missing_left_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": [{ "right": "something" }]
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash value: something')

    def test_invalid_missing_right_target_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": [{ "left": "something" }]
        }'''
        with self.assertRaises(AssertionError) as err:
            validator.valid_receipt(receipt)
        self.assertEqual(err.exception.message, 'Invalid hash value: something')

    def test_invalid_target_proof_4(self):
        validator = Chainpoint()
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "@type": "ChainpointSHA256v2",
            "targetHash": "f17fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19",
            "merkleRoot": "fd3f0550fd1164f463d3e57b7bb6834872ada68501102cec6ce93cdbe7a17404",
            "proof": [{ "right": "a99fbe8fc1a6e5a8289da6fea45d16a92b35c629fa1fd34178245420378bea19" }]
        }'''
        self.assertFalse(validator.valid_receipt(receipt))

    def test_valid_with_proof(self):
        validator = Chainpoint()
        receipt = '''{
            "header": {
                "chainpoint_version": "1.1",
                "hash_type": "SHA-256",
                "merkle_root": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                "tx_id": "b84a92f28cc9dbdc4cd51834f6595cf97f018b925167c299097754780d7dea09",
                "timestamp": 1445033433
            },
            "target": {
                "target_hash": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                "target_proof": [{
                    "parent": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "left": "cbda53ca51a184b366cbde3cb026987c53021de26fa5aabf814917c894769b65",
                    "right": "a52d9c0a0b077237f58c7e5b8b38d2dd7756176ca379947a093105574a465685"
                }, {
                    "parent": "5faa75ca2c838ceac7fb1b62127cfba51f011813c6c491335c2b69d54dd7d79c",
                    "left": "4f0398f4707c7ddb8d5a85508bdaa9e22fb541fa0182ae54f25513b6bd3f8cb9",
                    "right": "3bd99c8660a226a62a7df1efc2a296a398ad91e2aa56d68fefd08571a853096e"
                }]
            }
        }'''
        self.assertTrue(validator.valid_receipt(receipt))


    def test_key_path(self):
        receipt = '''{
            "@context": "https://w3id.org/chainpoint/v2",
            "type": "ChainpointSHA256v2",
            "targetHash": "bdf8c9bdf076d6aff0292a1c9448691d2ae283f2ce41b045355e2c8cb8e85ef2",
            "merkleRoot": "51296468ea48ddbcc546abb85b935c73058fd8acdb0b953da6aa1ae966581a7a",
            "proof": [{
                "left": "bdf8c9bdf076d6aff0292a1c9448691d2ae283f2ce41b045355e2c8cb8e85ef2"
            }, {
                "left": "cb0dbbedb5ec5363e39be9fc43f56f321e1572cfcf304d26fc67cb6ea2e49faf"
            }, {
                "right": "cb0dbbedb5ec5363e39be9fc43f56f321e1572cfcf304d26fc67cb6ea2e49faf"
            }],
            "anchors": [{
                "type": "BTCOpReturn",
                "sourceId": "f3be82fe1b5d8f18e009cb9a491781289d2e01678311fe2b2e4e84381aafadee"
            }]
        }'''
        verifier = Chainpoint()
        self.assertTrue(verifier.valid_receipt(receipt))


if __name__ == '__main__':
    unittest.main()

