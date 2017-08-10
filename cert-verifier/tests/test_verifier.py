import unittest

from cert_verifier import verifier, StepStatus

# Final result is last position in results array
VERIFICATION_RESULT_INDEX = -1
# second to last
AUTHENTICITY_RESULT_INDEX = -2
# revocation 3rd to last
REVOCATION_RESULT_INDEX = -3
# integrity is first check
INTEGRITY_RESULT_INDEX = 0

class TestVerify(unittest.TestCase):
    # end-to-end tests
    def test_verify_v1_2(self):
        result = verifier.verify_certificate_file('data/1.2/sample_signed_cert-1.2.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_v1_1(self):
        result = verifier.verify_certificate_file('data/1.1/sample_signed_cert-1.1.json',
                                                  '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v1_2(self):
        result = verifier.verify_certificate_file('data/1.2/sample_signed_cert-1.2.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v1_2_609(self):
        result = verifier.verify_certificate_file('data/1.2/609c2989-275f-4f4c-ab02-b245cfb09017.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v1_2_b5d(self):
        result = verifier.verify_certificate_file('data/1.2/b5dee02e-50cd-4e48-ad33-de7d2eafa359.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v1_1(self):
        result = verifier.verify_certificate_file('data/1.1/sample_signed_cert-1.1.json',
                                                  '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v2(self):
        result = verifier.verify_certificate_file('data/2.0/valid.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v2_with_v1_issuer(self):
        result = verifier.verify_certificate_file('data/2.0/valid_v2_certificate_with_v1_issuer.json')
        self.assertEquals(StepStatus.passed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v2_tampered(self):
        result = verifier.verify_certificate_file('data/2.0/invalid_tampered.json')
        self.assertEquals(StepStatus.failed.name, result[INTEGRITY_RESULT_INDEX]['status'])
        self.assertEquals(StepStatus.failed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v2_tampered_unmapped(self):
        result = verifier.verify_certificate_file('data/2.0/invalid_unmapped_fields.json')
        self.assertEquals(StepStatus.failed.name, result[INTEGRITY_RESULT_INDEX]['status'])
        self.assertEquals(StepStatus.failed.name, result[VERIFICATION_RESULT_INDEX]['status'])

    def test_verify_cert_file_v2_revoked(self):
        result = verifier.verify_certificate_file('data/2.0/invalid_revoked.json')
        self.assertEquals(StepStatus.failed.name, result[REVOCATION_RESULT_INDEX]['status'])
        self.assertEquals(StepStatus.failed.name, result[VERIFICATION_RESULT_INDEX]['status'])
        print(result)

    def test_verify_cert_file_v2_authenticity_fail(self):
        result = verifier.verify_certificate_file('data/2.0/invalid_authenticity.json')
        self.assertEquals(StepStatus.failed.name, result[AUTHENTICITY_RESULT_INDEX]['status'])
        self.assertEquals(StepStatus.failed.name, result[VERIFICATION_RESULT_INDEX]['status'])

if __name__ == '__main__':
    unittest.main()
