from django.db import models
from django.contrib.auth.models import User


class Input(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=50)
    project = models.CharField(max_length=50)
    valuation_date = models.DateField(blank=True, null=True)
    statutory_corporate_tax_rate = models.FloatField()
    statutory_mat_rate = models.FloatField(blank=True, null=True)
    post_tax_wacc = models.FloatField()
    long_term_growth_rate = models.FloatField()
    company_specific_risk = models.FloatField(blank=True, null=True)
    contingent_liability = models.FloatField(blank=True, null=True)
    total_shares_outstanding = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.project


class FSAPL(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    report = models.CharField(max_length=50)
    year_neg_2 = models.FloatField(verbose_name='Year -2')
    year_neg_1 = models.FloatField(verbose_name='Year -1')
    year_0 = models.FloatField(verbose_name='Year 0')
    year_pos_1 = models.FloatField(verbose_name='Year 1')
    year_pos_2 = models.FloatField(verbose_name='Year 2')
    year_pos_3 = models.FloatField(verbose_name='Year 3')
    year_pos_4 = models.FloatField(verbose_name='Year 4')
    year_pos_5 = models.FloatField(verbose_name='Year 5')

    def __str__(self):
        return str(self.project) + ', ' + str(self.report)

    @property
    def yoy_growth_neg_1(self):
        return int(((float(self.year_neg_1) / float(self.year_neg_2)) - 1) * 100)

    @property
    def yoy_growth_0(self):
        return int(((float(self.year_0) / float(self.year_neg_1)) - 1) * 100)

    @property
    def yoy_growth_pos_1(self):
        return int(((float(self.year_pos_1) / float(self.year_0)) - 1) * 100)

    @property
    def yoy_growth_pos_2(self):
        return int(((float(self.year_pos_2) / float(self.year_pos_1)) - 1) * 100)

    @property
    def yoy_growth_pos_3(self):
        return int(((float(self.year_pos_3) / float(self.year_pos_2)) - 1) * 100)

    @property
    def yoy_growth_pos_4(self):
        return int(((float(self.year_pos_4) / float(self.year_pos_3)) - 1) * 100)

    @property
    def yoy_growth_pos_5(self):
        return int(((float(self.year_pos_5) / float(self.year_pos_4)) - 1) * 100)


class FSAPLReport(models.Model):
    report = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.report


class FSABS(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    report = models.CharField(max_length=50)
    year_0 = models.FloatField(verbose_name='Year 0')
    year_pos_1 = models.FloatField(verbose_name='Year 1')
    year_pos_2 = models.FloatField(verbose_name='Year 2')
    year_pos_3 = models.FloatField(verbose_name='Year 3')
    year_pos_4 = models.FloatField(verbose_name='Year 4')
    year_pos_5 = models.FloatField(verbose_name='Year 5')

    def __str__(self):
        return str(self.project) + ', ' + str(self.report)


class FSABSReport(models.Model):
    report = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.report


class WACC(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    particulars = models.CharField(max_length=50)
    percentage = models.FloatField()

    def __str__(self):
        return str(self.project) + ', ' + str(self.particulars)


class WACCParticulars(models.Model):
    particulars = models.CharField(max_length=50)

    def __str__(self):
        return self.particulars


class YOYGrowth(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    report = models.CharField(max_length=50, default="Sales")
    year_neg_1 = models.FloatField()
    year_0 = models.FloatField()
    year_pos_1 = models.FloatField()
    year_pos_2 = models.FloatField()
    year_pos_3 = models.FloatField()
    year_pos_4 = models.FloatField()
    year_pos_5 = models.FloatField()

    def __str__(self):
        return str(self.project) + ', ' + str(self.report)


class DCF(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    report = models.CharField(max_length=50)
    year_1 = models.FloatField()
    year_2 = models.FloatField()
    year_3 = models.FloatField()
    year_4 = models.FloatField()
    year_5 = models.FloatField()
    terminal_period = models.FloatField()

    def __str__(self):
        return str(self.project) + ', ' + str(self.report)


class Output(models.Model):
    project = models.ForeignKey(Input, on_delete=models.CASCADE)
    long_term_sustainable_growth_rate = models.FloatField()
    terminal_value = models.FloatField()
    sum_of_present_value_of_net_free_cash_flows_to_equity = models.FloatField()
    present_value_of_terminal_value = models.FloatField()
    gross_equity_value = models.FloatField()
    investments = models.FloatField()
    cash_and_equivalent = models.FloatField()
    other_non_current_assets = models.FloatField()
    pref_shares = models.FloatField()
    debt = models.FloatField()
    contingent_liabilities = models.FloatField()
    equity_value = models.FloatField()

    def __str__(self):
        return str(self.project)
