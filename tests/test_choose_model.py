import copy,json,unittest
from pathlib import Path
from scripts.choose_model import select

class RoutingTests(unittest.TestCase):
    def setUp(self):self.data=json.loads((Path(__file__).resolve().parents[1]/'examples/catalog.json').read_text())
    def test_lowest_capable_not_absolute_smallest(self):self.assertEqual(select(self.data)['route']['model'],'example-small')
    def test_missing_tools(self):
        self.data['models'][1]['capabilities']=['text'];self.assertEqual(select(self.data)['status'],'unchanged')
    def test_context(self):
        self.data['task']['required_context_tokens']=100000;self.assertEqual(select(self.data)['status'],'unchanged')
    def test_no_unavailable_fallback(self):
        self.data['models'][1]['available']=False;self.assertEqual(select(self.data)['status'],'unchanged')
    def test_unverified_order(self):
        for m in self.data['models']:m['rank_verified']=False
        self.assertEqual(select(self.data)['status'],'unverified')
    def test_unsupported_host(self):
        self.data['task']['host_supports_route']=False;self.assertEqual(select(self.data)['status'],'unsupported')
    def test_no_foreground_change_without_authorization(self):
        self.data['task']['scope']='foreground';self.assertEqual(select(self.data)['status'],'unchanged')
    def test_no_cross_account_or_provider(self):
        for field in ['provider','account']:
            d=copy.deepcopy(self.data);d['models'][1][field]='other';self.assertEqual(select(d)['status'],'unchanged')
    def test_current_already_lowest(self):
        self.data['current']['model']='example-small';self.assertEqual(select(self.data)['status'],'unchanged')
    def test_no_unknown_current_downgrade_claim(self):
        self.data['current']['model']='unknown';self.assertEqual(select(self.data)['status'],'unverified')
    def test_invalid_rank_not_eligible(self):
        self.data['models'][1]['rank']=float('nan');self.assertEqual(select(self.data)['status'],'unchanged')
    def test_never_mutates_or_claims_measured_savings(self):
        old=copy.deepcopy(self.data);r=select(self.data);self.assertEqual(self.data,old);self.assertFalse(r['applied']);self.assertEqual(r['savings'],'unmeasured')

if __name__=='__main__':unittest.main()
