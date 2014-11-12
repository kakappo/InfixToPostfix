#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re

'''中缀表达式转换为逆兰波表达式：
支持正负数，浮点数
输入要求每个操作数与操作符以单个空格分离，例如：
-1 + 2 - 3.6 * ( -2 / 2 )
'''
class InfixToPostfix():
    def __init__(self):
        self.operators = ['+', '-', '*', '/', '%', '^', '(', ')']
        self.str_list = []
        self.output_str = ""

    # 检查表达式是否合法
    def checkValidation(self, src_str):
        # 去掉首尾空格符
        src_str = src_str.strip()
        # 检查表达式括号符是否成对
        if src_str.count("(") != src_str.count(")"):
            raise InvalidFormatError("Invalid input!")
            return False
        # 检查输入格式是否为操作符和操作数交替出现，并以操作数开头结尾
        # 去掉去括号符后
        new_src_list = src_str.replace("( ", "").replace(" )", "").split(" ")
        # 数组长度应为单数
        if len(new_src_list) % 2 == 0:
            raise InvalidFormatError("Invalid input!")
            return False
        # 规范的排列应为：双数位置是操作数，单数位置是操作符
        for i in range(0, len(new_src_list)):
            # 若为数字型,则包括整形和浮点型
            if int(i) % 2 == 0 and re.match('^\+?-?\d+\.?\d*$', new_src_list[i]):
                continue
                # print "numeric:"+local_src_list[i]
            elif int(i) % 2 == 1 and new_src_list[i] in self.operators:
                continue
            # print "operator:"+local_src_list[i]
            else:
                raise InvalidFormatError("Invalid input!")
                return False
        # 检查合法则获取数组
        self.str_list = src_str.split(" ")
        return True

    # 获取操作符优先级
    def getPriority(self, operator):
        if operator == '(':
            return 0
        elif operator in ['+', '-']:
            return 1
        elif operator in ['*', '/', '%']:
            return 2
        elif operator == '^':
            return 3
        else:
            return 4

    # 转换表达式
    def convert(self, src_str):
        '''convert infix expression to postfix expression'''
        if self.checkValidation(src_str):
            src_list = self.str_list
            stackOutput = []      # 输出符栈
            stackOperator = []     # 操作符栈
            for item in src_list:
                    # item为操作符时
                    if item in self.operators:
                        # 遇到左括号，将其放入输出栈中
                        if item == '(':
                            stackOperator.append(item)
                        # 遇到右括号，则将操作符栈元素弹出并加入输出栈直到遇到左括号为止，最后弹出但不输出左括号
                        elif item == ')':
                            while stackOperator:
                                topOperator = stackOperator[len(stackOperator)-1]
                                if topOperator != "(":
                                    # 弹出操作符并加入输出栈
                                    stackOutput.append(stackOperator.pop())
                                else:
                                    # 弹出但不输出左括号
                                    stackOperator.pop()
                                    break
                        # 遇到括号以外的操作符
                        else:
                            # 操作符栈不为空时，则比较当前操作符与栈顶操作符的优先级
                            if stackOperator:
                                # 当前操作符优先级大于栈顶操作符时，将该操作符入栈
                                if self.getPriority(item) > self.getPriority(stackOperator[len(stackOperator)-1]):
                                    stackOperator.append(item)
                                # 当前操作符优先级小于等于栈顶操作符时，则弹出并输出栈顶操作符，循环直到大于栈顶操作符的优先级，或栈为空
                                else:
                                    while stackOperator:
                                        topOperator = stackOperator[len(stackOperator)-1]
                                        if self.getPriority(item) <= self.getPriority(topOperator):
                                            # 弹出栈顶操作符并加入输出栈
                                            stackOutput.append(stackOperator.pop())
                                        else:
                                            break
                                    # 将该操作符加入操作符栈
                                    stackOperator.append(item)
                            # 操作符栈为空时，将该操作符入栈
                            else:
                                stackOperator.append(item)
                    # item为操作数时，直接加入输出栈
                    else:
                        stackOutput.append(item)
            # 将操作符栈剩余元素全部弹出并加入输出栈
            while stackOperator:
                stackOutput.append(stackOperator.pop())
            # 组装成转换后的表达式字符串
            self.output_str = " ".join(stackOutput)
            # print self.output_str
        # 返回转换后的表达式字符串
        return self.output_str


class InvalidFormatError(ValueError):
    pass


# if __name__ == '__main__':
#     # 提示输入，并获取字符串
#     src_str = raw_input("Please input expression:")
#     # 初始化转换类并调用转换函数
#     conversion = InfixToPostfix()
#     output_str = conversion.convert(src_str)
#     if output_str != "":
#         print "Infix expression_r:", src_str
#         print "Postfix expression_r:", output_str

import unittest
class KnownExpressions(unittest.TestCase):
    known_expressions = (('1 + 2', '1 2 +'),    # 不同优先级操作符的组合排列
                         ('11 * 22', '11 22 *'),
                         ('123 ^ 234', '123 234 ^'),
                         ('1 + 2 * 3 ^ 4', '1 2 3 4 ^ * +'),
                         ('1 ^ 2 / 3 - 4', '1 2 ^ 3 / 4 -'),
                         ('1 % 2 ^ 3 + 4', '1 2 3 ^ % 4 +'),
                         ('1 / ( 2 )', '1 2 /'),  # 括号的组合排列
                         ('( 10 + 20 )', '10 20 +'),
                         ('( 321 ^ 2 )', '321 2 ^'),
                         ('( ( 1 + 2 ) * 3 ) ^ 4', '1 2 + 3 * 4 ^'),
                         ('1 ^ ( ( 2 / 3 ) - 4 )', '1 2 3 / 4 - ^'),
                         ('( 1 % 2 ) ^ ( 3 + 4 )', '1 2 % 3 4 + ^'),
                         ('-1 + +2', '-1 +2 +'),    # 正负数，浮点数的组合排列
                         ('12.34 / -0.25', '12.34 -0.25 /'),
                         ('268.0 * 50.05 ^ 2', '268.0 50.05 2 ^ *'),
                         (' 1 + 2', '1 2 +'),    # 前后带空格
                         ('1 % 2   ', '1 2 %'),
                         ('    1 ^ 2   ', '1 2 ^'),
                         ('10 ( % 3 )', '10 3 %'),    # 其它组合排列
                         ('( 3000 % +7 ) ^ ( ( ( -8.8 * 0.02345 ) + 2 ) / 4 - 5432.0 )', '3000 +7 % -8.8 0.02345 * 2 + 4 / 5432.0 - ^'))
    invalid_expressions = ('',      # 空输入
                           '1  ^   2',  # 操作数与操作符间存在多空格
                           '4 *',    # 非法表达式
                           '% 5',
                           '+ - 6',
                           '/ 7 ^',
                           '8 + 2 ^ 3 -',
                           '(9 / )',
                           '9 * ( 5 - 2 ',
                           '( 10 + ( 2 + 3 )',
                           '+ 1 / 2 * 5 ^',
                           'invalid + 10',      # 包含非法字符
                           '11 @ 11.11',
                           '[12] / 20',
                           '13 \ ( 33 ~ 333 ) & 30')

    def test_convert_known_expressions(self):
        '''convert should give known result with known input'''
        for input_str, output_str in self.known_expressions:
            result = InfixToPostfix().convert(input_str)
            self.assertEqual(result, output_str)

    def test_convert_invalid_expressions(self):
        '''convert should fail with Invalid input'''
        for input_str in self.invalid_expressions:
            self.assertRaises(InvalidFormatError, InfixToPostfix().convert, input_str)

if __name__ == '__main__':
    unittest.main()
