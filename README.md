# pyincometaxuk
## UK income tax calculator in Python

Based loosely on https://github.com/tameemsafi/uk-tax-calculator

Currently based on 2017/18 tax year.

## Installation

Package is not yet on pip, so you need to download the module and import.

E.g.

```
import path/to/src/pyinctaxuk
```

## Usage

Primary uses are the functions:

`output_annual_tax_results(gross_income, salary_sacrifice, bonus=0, student_loan_plan=False, print_results=True)`
`output_monthly_tax_results(gross_income, salary_sacrifice, bonus=0, student_loan_plan=False, print_results=True)`


* Gross income and salary sacrifice should be annual £ amounts
* Student loan plan can be plan_1, plan_2 or False
* Setting print_results to False will prevent the verbose print

In any case, the functions output a list:

```
[post_tax_income, income_tax, national_insurance, student_loan_repayment]
```

Or if specifying a bonus in the monthly function, a list of monthly figures zipped with a list of the same figures
in the bonus period.

Other functions are mainly intermediate calculations.

## To-do

* Generalise tax settings to enable specifying tax year
* Add marriage and blind allowances
* Add childcare
* Add support for >69 year olds
* Add overtime
* Add resident of Scotland
* Add non-salary-sacrifice pensions
* Create tests