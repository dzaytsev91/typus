# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from builtins import *  # noqa

from tests.test_expressions import EnRuExpressionsTest
from typus import Typus, typus
from typus.chars import *  # noqa
from typus.decorators import escape_html
from typus.expressions import EnRuExpressions


class SummaryTest(EnRuExpressionsTest):
    maxDiff = None

    def typus(self, *args):
        return lambda text, test: self.assertEqual(typus(text), test)

    def test_quotes(self):
        test = self.typus()
        test('00 "11" 00', '00 «11» 00')
        test('''00" "11 '22' 11"? "11 '22 "33 33?"' 11" 00 "11 '22' 11" 0"''',
             '00{0} «11 „22“ 11»? «11 „22 «33 33?»“ 11» 00 «11 „22“ 11» 0{0}'
             .format(DPRIME))

    def test_mdash(self):
        test = self.typus()
        test('--', '--')
        test('-- ', MDASH + NBSP)
        test(' -- ', MDASH_PAIR)
        test(', -- ', ',' + MDASH_PAIR)
        # Differencies
        test(', - foo', ',{0}foo'.format(MDASH_PAIR))
        test('2 - 2foo', '2{0}2{1}foo'.format(MDASH_PAIR, NBSP))  # + units
        test('2 - 2', '2{0}{1}{0}2'.format(NBSP, MINUS))  # + minus
        test('foo - "11" 00', 'foo{0}«11» 00'.format(MDASH_PAIR))

    def test_dprime(self):
        test = self.typus()
        test('4"', '4' + DPRIME)
        test('"4"', '«4»')
        test('" 22"', '" 22' + DPRIME)

    def test_phones(self):
        test = self.typus()
        test('555-55-55', '555{0}55{0}55'.format(NDASH))
        test('55-555-55', '55{0}555{0}55'.format(NDASH))
        # Skips to mdash
        test('55-555', '55{0}555'.format(MDASH))

    def test_ranges(self):
        test = self.typus()
        test('2-3', '2{0}3'.format(MDASH))
        test('2-3 44', '2{0}3 44'.format(MDASH))

        # Fails to math
        test('2 - 3', '2{0}{1}{0}3'.format(NBSP, MINUS))
        test('2-3 x 4', '2{1}3{0}{2}{0}4'.format(NBSP, MINUS, TIMES))
        test('2-3 * 4', '2{1}3{0}{2}{0}4'.format(NBSP, MINUS, TIMES))
        test('2-3 - 4', '2{1}3{0}{1}{0}4'.format(NBSP, MINUS))

    def test_ruble(self):
        test = self.typus()
        test('111 руб.', '111{0}₽'.format(NBSP))
        # This happens because of digit_spaces
        test('111 рублей', '111{0}рублей'.format(NBSP))
        # But it doesn't support digit longer than 4
        test('1111 рублей', '1111 рублей')

    def test_math(self):
        test = self.typus()
        for options, result in EnRuExpressions.math.items():
            for option in options:
                # -3, 3-3, 3 - 3, x - 3
                if result == MINUS:
                    # This one clashes with range
                    test('3{0}3'.format(option), '3{0}3'.format(MDASH))
                    # This one clashes with mdash
                    test('x{0}{1}{0}3'.format(NBSP, option),
                         'x{0}{1} 3'.format(NBSP, MDASH))
                else:
                    test('3{0}3'.format(option), '3{0}3'.format(result))
                    test('x{0}{1}{0}3'.format(NBSP, option),
                         'x{0}{1}{0}3'.format(NBSP, result))

                test(option + '3', result + '3')
                test('3{0}{1}{0}3'.format(NBSP, option),
                     '3{0}{1}{0}3'.format(NBSP, result))

    def test_pairs(self):
        test = self.typus()
        test('aaa aaa', 'aaa aaa')
        test('aaa 2a', 'aaa 2{0}a'.format(NBSP))  # clashes with units
        test('aaa-aa aa', 'aaa-aa aa')  # important check -- dash and 2 letters
        test('aaa aa', 'aaa aa')
        test('a aa a', 'a{0}aa{0}a'.format(NBSP))

    def test_digit_spaces(self):
        test = self.typus()
        test('4444444 foo', '4444444 foo')
        test('444 foo', '444{0}foo'.format(NBSP))
        test('444 +', '444{0}+'.format(NBSP))
        test('444 -', '444{0}{1}'.format(NBSP, MDASH))

    def test_example(self):
        test = self.typus()
        text = (
            'Излучение, как следует из вышесказанного, концентрирует '
            'внутримолекулярный предмет - деятельности. "...ff \'Можно?\' '
            'предположить, что силовое - "поле "мент "d" ально" отклоняет" '
            'сенсибельный \'квазар!..\' cc", не учитывая мнения авторитетов. '
            'Искусство испускает данный электрон, учитывая опасность, '
            '<code> "d" test -- test(c)</code> которую    представляли '
            'собой писания Дюринга для не окрепшего еще немецкого рабочего '
            'движения. Смысл жизни -- амбивалентно (с) дискредитирует '
            'закон (r) исключённого(tm) третьего (тм)...\n\n\n'
            '- Химическое соединение ненаблюдаемо контролирует экран-ый '
            'квазар. Идеи 3/4   гедонизма занимают b & b центральное место '
            'в утилитаризме "Милля и Бентама", однако <- гравитирующая -> '
            'сфера масштабирует фотон, +-2мм изменяя привычную реальность. '
            'Силовое *3 поле -3 реально 3 * 2 /= 6   3x3 восстанавливает '
            'трансцендентальный 3" 2\' принцип 1000р. восприятия.'
            '"...\'test\'" (c) m&m\'s'
        )
        result = (
            'Излучение, как следует из_вышесказанного, концентрирует '
            'внутримолекулярный предмет_— деятельности. «…ff „Можно?“ '
            'предположить, что силовое_— „поле «мент „d“ ально» отклоняет“ '
            'сенсибельный „квазар!..“ cc», не_учитывая мнения авторитетов. '
            'Искусство испускает данный электрон, учитывая опасность, '
            '<code> "d" test -- test(c)</code> которую представляли собой '
            'писания Дюринга для не_окрепшего еще немецкого рабочего '
            'движения. Смысл жизни_— амбивалентно ©_дискредитирует закон_® '
            'исключённого™ третьего_™…\n\n'
            '—_Химическое соединение ненаблюдаемо контролирует экран-ый '
            'квазар. Идеи ¾_гедонизма занимают b_&_b_центральное место '
            'в_утилитаризме «Милля и_Бентама», однако ←_гравитирующая_→ '
            'сфера масштабирует фотон, ±2_мм изменяя привычную реальность. '
            'Силовое ×3_поле −3_реально 3_×_2_≠_6 3×3 восстанавливает '
            'трансцендентальный 3″ 2′ принцип 1000_₽ восприятия.'
            '«…„test“» ©_m&m\'s'
        ).replace('_', NBSP)
        test(text, result)


class SummaryTest2(SummaryTest):
    class Testus(Typus):
        loq, roq, leq, req = LDQUO, RDQUO, LSQUO, RSQUO

    def typus(self, *args):
        testus = escape_html(self.Testus())

        def testcase(text, test):
            test = (test.replace(Typus.leq, self.Testus.leq)
                        .replace(Typus.req, self.Testus.req)
                        .replace(Typus.loq, self.Testus.loq)
                        .replace(Typus.roq, self.Testus.roq))
            self.assertEqual(testus(text), test)
        return testcase