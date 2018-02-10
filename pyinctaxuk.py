"""
UK income tax calculator

Functions:
get_net_adjusted_income -- return gross income after salary sacrifice
get_personal_allowance -- return the income tax personal allowance applicable
get_total_taxable_income -- return the portion of income subject to tax
get_tax_breakdown -- return the amount paid in each band for NI or income tax
get_annual_tax -- return the total NI or income tax paid
get_annual_student_loan_rep -- return the student loan repayments
format_currency -- convert a float to £x,xxx.xx format
output_annual_tax_results -- return (and optionally print) post tax income,
    income tax paid, national insurance and student loan repayments on an
    annual basis
output_monthly_tax_results -- return (and optionally print) post tax income,
    income tax paid, national insurance and student loan repayments on a
    monthly basis, with a second list output for results in bonus period

Example usage:
Calculate the annual income tax for someone with a salary of £50k,
5% employee pension contribution, a plan 1 student loan. Don't print.
    results = output_tax_results(50000.0, 0.05*50000.0, 'plan_1', False)

"""
# UK income tax calculator
# Initially excluding childcare, tax codes, >69 year olds,
#    married/blind, resident in Scotland, overtime, non-salary-sacrifice pension

# Inputs:
#   Tax settings
#   Gross annual income
#   Salary sacrifice
#   Student loan type

# Set up tax settings. This can later be imported from somewhere

TAX_SETTINGS = {

    'year' : '2017/18',

    'allowance' : {

        'basic' : 11500.0,
        'taper' : 100000.0

    },

    'income_tax' : {

        0 : {

            'start' : 0.0,
            'end' : 33500.0,
            'rate' : 0.20

        },

        1 : {

            'start' : 33500.0,
            'end' : 150000.0,
            'rate' : 0.40

        },

        2 : {

            'start' : 150000.0,
            'end' : 999999999999.0,
            'rate' : 0.40

        }

    },

    'national_insurance' : {

        0 : {

            'start' : 0.0,
            'end' : 157.0,
            'rate' : 0.0

        },

        1 : {

            'start' : 157.0,
            'end' : 866.0,
            'rate' : 0.12

        },

        2 : {

            'start' : 866.0,
            'end' : 999999999999.0, # do this better
            'rate' : 0.02

        }


    },

    'student_loan' : {

        'plan_1' : {

            'threshold' : 17775.0,
            'rate' : 0.09

        },

        'plan_2' : {

            'threshold' : 21000.0,
            'rate' : 0.09

        }

    }


}

# Define functions

def get_net_adjusted_income(gross_income, salary_sacrifice):

    """Returns net adjusted income, i.e. gross income net of salary sacrifice.

    Should be fed with an absolute salary sacrifice."""

    net_adjusted_income = gross_income - salary_sacrifice

    return net_adjusted_income

def get_personal_allowance(gross_income, salary_sacrifice):

    """Returns the personal allowance taking into account any tapering"""

    personal_allowance = TAX_SETTINGS['allowance']['basic']

    if gross_income > TAX_SETTINGS['allowance']['taper']:
        # If earn above the taper amount, personal allowance
        # is reduced by £1 for every £2 income exceeds taper amount
        personal_allowance_reduction = \
            max(0, (get_net_adjusted_income(gross_income, salary_sacrifice) \
            - TAX_SETTINGS['allowance']['taper']) / 2)
        personal_allowance -= personal_allowance_reduction

    return personal_allowance

def get_total_taxable_income(gross_income, salary_sacrifice):

    """Returns the taxable income after salary sacrifice and personal allowance"""

    taxable_income = get_net_adjusted_income(gross_income, salary_sacrifice)\
     - get_personal_allowance(gross_income, salary_sacrifice)

    return taxable_income

def get_tax_breakdown(gross_income, salary_sacrifice, tax_type):

    """Returns a list with the annual tax paid in each band.

    Tax type can be income_tax or national_insurance"""

    if tax_type == 'income_tax':
        # income tax calculated annually but net of personal allowance
        taxable_income = get_total_taxable_income(gross_income, salary_sacrifice)

    elif tax_type == 'national_insurance':
        # national insurance is calculated weekly before any salary sacrifice
        # we will later output annual
        taxable_income = gross_income / 52.0

    band_1_paid = 0.0
    band_2_paid = 0.0
    band_3_paid = 0.0

    # This set of nested ifs will incrementally check if tax should be paid within a band
    # and then update the tax paid in that band if so

    if taxable_income >= TAX_SETTINGS[tax_type][0]['start']:

        band_1_paid = min(taxable_income, TAX_SETTINGS[tax_type][0]['end'])\
         * TAX_SETTINGS[tax_type][0]['rate']

        if taxable_income >= TAX_SETTINGS[tax_type][1]['start']:

            band_2_paid =\
             (min(taxable_income, TAX_SETTINGS[tax_type][1]['end'])\
             - TAX_SETTINGS[tax_type][1]['start'])\
             * TAX_SETTINGS[tax_type][1]['rate']

            if taxable_income >= TAX_SETTINGS[tax_type][2]['start']:

                band_3_paid =\
                 (min(taxable_income, TAX_SETTINGS[tax_type][2]['end'])\
                 - TAX_SETTINGS[tax_type][2]['start'])\
                 * TAX_SETTINGS[tax_type][2]['rate']

    results = [band_1_paid, band_2_paid, band_3_paid]

    if tax_type == 'national_insurance':
        # NI calculated weekly but we want annual
        results = [i * 52 for i in results]

    return results

def get_annual_tax(gross_income, salary_sacrifice, tax_type):

    """Sum the tax paid in each threshold and return"""

    annual_tax = sum(get_tax_breakdown(gross_income, salary_sacrifice, tax_type))

    return annual_tax

def get_annual_student_loan_rep(gross_income, salary_sacrifice, plan):

    """Returns student loan repayments.

    Plan can be plan_1 or plan_2"""

    student_loan_repayment = 0

    taxable_income = get_net_adjusted_income(gross_income, salary_sacrifice)

    if taxable_income\
      > TAX_SETTINGS['student_loan'][plan]['threshold']:

        student_loan_repayment = TAX_SETTINGS['student_loan'][plan]['rate'] *\
         (taxable_income - TAX_SETTINGS['student_loan'][plan]['threshold'])

    return student_loan_repayment

def format_currency(flt):
    """Return a formatted UK currency string from a float"""
    return '£{:,.2f}'.format(flt)

def output_annual_tax_results(gross_income, salary_sacrifice, bonus=0, \
        student_loan_plan=False, print_results=True):
    """Return all tax results in annual terms

    Inputs: gross income, bonus, salary sacrifice (absolute), student loan plan (plan_1, plan_2),
        boolean to print results (defaults to true)
    Outputs: returns a list with post tax income, income tax, national insurance and student loan
    """
    taxable_income = get_total_taxable_income(gross_income+bonus, salary_sacrifice)
    income_tax = get_annual_tax(gross_income+bonus, salary_sacrifice, 'income_tax')
    national_insurance = get_annual_tax(gross_income+bonus, salary_sacrifice, 'national_insurance')

    if student_loan_plan:
        student_loan_repayment = \
         get_annual_student_loan_rep(gross_income+bonus, salary_sacrifice, student_loan_plan)

    else:
        student_loan_repayment = 0

    post_tax_income = get_net_adjusted_income(gross_income+bonus, salary_sacrifice)\
     - income_tax - national_insurance - student_loan_repayment

    if print_results:
        print('Your gross salary is {}'.format(format_currency(gross_income)))
        print('Your annual bonus is {}'.format(format_currency(bonus)))
        print('You have gross salary deductions of {}'.format(format_currency(salary_sacrifice)))
        print('Your total taxable income is therefore {}'.format(format_currency(taxable_income)))
        print('')
        print('RESULTS:')
        print('Income tax: {}'.format(format_currency(income_tax)))
        print('National insurance: {}'.format(format_currency(national_insurance)))
        print('Student loan repayments: {}'.format(format_currency(student_loan_repayment)))
        print('Total annual income after tax: {}'.format(format_currency(post_tax_income)))

    return [post_tax_income, income_tax, national_insurance, student_loan_repayment]

def output_monthly_tax_results(gross_income, salary_sacrifice, bonus=0, \
        student_loan_plan=False, print_results=True):
    """Return all tax results in monthly terms, including bonus period if applicable.

    Inputs: gross income, bonus (default 0), salary sacrifice, student loan plan
    (plan_1, plan_2, defaults false), boolean to print results (defaults true)

    Outputs: returns either one or two zipped lists, one with monthly earnings in normal
    period and one with monthly earnings in bonus period (blank if no bonus specified)
    """

    annual_income_ex_bonus = \
     output_annual_tax_results(gross_income, salary_sacrifice, 0, student_loan_plan,\
      False)

    monthly_income_ex_bonus = [i/12 for i in annual_income_ex_bonus]

    if bonus > 0:

        annual_income_inc_bonus = \
        output_annual_tax_results(gross_income, salary_sacrifice, bonus, student_loan_plan, \
        False)

        monthly_income_in_bonus_period = \
        [a + b - c for a, b, c in zip(monthly_income_ex_bonus, \
        annual_income_inc_bonus, annual_income_ex_bonus)]

        output = zip(monthly_income_ex_bonus, monthly_income_in_bonus_period)

    else:

        output = monthly_income_ex_bonus

    if print_results:
        print('IN A REGULAR MONTH:')
        print('Income tax: {}'.format(format_currency(monthly_income_ex_bonus[1])))
        print('National insurance: {}'.format(format_currency(monthly_income_ex_bonus[2])))
        print('Student loan repayments: {}'.format(format_currency(monthly_income_ex_bonus[3])))
        print('Total monthly income after tax: {}'.format(\
         format_currency(monthly_income_ex_bonus[0])))
        print('')

        if bonus > 0:

            print('IN A BONUS MONTH:')
            print('Income tax: {}'.format(format_currency(\
             monthly_income_in_bonus_period[1])))
            print('National insurance: {}'.format(format_currency(\
             monthly_income_in_bonus_period[2])))
            print('Student loan repayments: {}'.format(format_currency(\
             monthly_income_in_bonus_period[3])))
            print('Total monthly income after tax: {}'.format(format_currency(\
             monthly_income_in_bonus_period[0])))

        else:
            print('No bonus specified.')

    return output
