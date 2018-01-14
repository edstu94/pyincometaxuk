# pyincometaxuk
## UK income tax calculator in Python

Based loosely on https://github.com/tameemsafi/uk-tax-calculator

Currently based on 2017/18 tax year.

## Installation

Package is not yet on pip, so you need to download the module and import.

E.g.

'''
import path/to/src/pyinctaxuk
'''

## Usage

Primary usage is the function:

'output_tax_results(gross_income, salary_sacrifice, student_loan_plan=False, print_results=True)'

* Gross income and salary sacrifice should be annual £ amounts
* Student loan plan can be plan_1, plan_2 or False
* Setting print_results to False will prevent the verbose print

In any case, the function outputs a list:

'''
[[post_tax_income, income_tax, national_insurance, student_loan_repayment]]
'''

Other functions are mainly intermediate calculations.

## To-do

* Generalise tax settings to enable specifying tax year
* Incorporate annual bonus
* Add marriage and blind allowances
* Add childcare
* Add support for >69 year olds
* Add overtime
* Add resident of Scotland
* Add non-salary-sacrifice pensions
* Create tests