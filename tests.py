
# TODO list in EDN => tuple in Python ; vector in EDN => list in Python
# TODO Handle tagged elements
# TODO Handle comments
# TODO Handle discard #_
# TODO Handle integers with N, minus, plus
# TODO Handle floats with e, M, minus, plus
# TODO Handle symbols


import unittest
import edn_lex
import edn_parse
import edn_format


class ConsoleTest(unittest.TestCase):
    def test_dumping(self):
        is_exception = False
        try:
            edn_format.loads("[1 true nil]")
        except AttributeError as x:
            is_exception = True
            print x
        self.assertFalse(is_exception)


class EdnTest(unittest.TestCase):
    def check_lex(self, expected_output, actual_input):
        self.assertEqual(expected_output, str(list(edn_lex.lex(actual_input))))


    def test_lexer(self):
        self.check_lex("[LexToken(NIL,None,1,0)]",
                       "nil")
        self.check_lex("[LexToken(BOOLEAN,True,1,0)]",
                       "true")
        self.check_lex("[LexToken(NUMBER,123,1,0)]",
                       "123")
        self.check_lex("[LexToken(NUMBER,456,1,0), LexToken(NIL,None,1,4), LexToken(BOOLEAN,False,1,8)]",
                       "456 nil false")
        self.check_lex("[LexToken(CHAR,'\\\\c',1,0)]",
                       r"\c")
        self.check_lex("[LexToken(KEYWORD,':abc',1,0)]",
                       r":abc")
        self.check_lex("[LexToken(KEYWORD,':+',1,0)]",
                       r":+")


    def check_parse(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_parse.parse(actual_input))


    def test_parser(self):
        self.check_parse(1,
                         "1")
        self.check_parse([1, 2, 3],
                         "[1 2 3]")
        self.check_parse({1, 2, 3},
                         "#{1 2 3}")
        self.check_parse([1, True, None],
                         "[1 true nil]")
        self.check_parse("\\c",
                         "\\c")
        self.check_parse(":abc",
                         ":abc")
        self.check_parse([":abc", 1, True, None],
                         "[:abc 1 true nil]")
        self.check_parse([":abc", 1, True, None],
            "(:abc 1 true nil)")
        self.check_parse({":a" : 1, ":b" : 2},
                         "{:a 1 :b 2}")


    def check_dump(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_format.dumps(actual_input))


    def test_dump(self):
        self.check_dump("#{1 2 3}",
                        {1, 2, 3})


    def test_round_trip(self):
        EDN_LITERALS = (
            "nil",
            "true",
            "false",
#            r"\\c",
            '"hello world"',
            ":keyword",
            ":+",
            ":!",
            ":-",
            ":_",
            ":$",
            ":&",
            ":=",
            ":.",
            ":abc/def",
            #"symbol",
            "123",
            #"123N",
            #"32.23",
            #"32.23M",
            '["abc"]',
            '[1]',
            '[1 "abc"]',
            '[1 "abc" true]',
            '[:ghi]',
#            '[1 "abc" true :ghi]',
#            '(1 "abc" true :ghi)',
#            '{:a 1 "foo" :gone :bar [1 2 3]}',
            #'#{:a :b [1 2 3]',
            #'#myapp/Person {:first "Fred" :last "Mertz',
            #'#inst "1985-04-12T23:20:50.52Z"',
            #'#uuid "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"'
        )

        for literal in EDN_LITERALS:
            step1 = literal
            step2 = edn_format.loads(literal)
            step3 = edn_format.dumps(step2)
            print step1, "->", step2, "->", step3
            self.assertEqual(step1, step3)