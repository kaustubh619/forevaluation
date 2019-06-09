from import_export import resources, widgets
from import_export.fields import Field
from .models import FSAPL, FSABS, WACC, Input
from django.forms import ValidationError


class FSAPLResource(resources.ModelResource):
    project_id = Field(column_name='project', attribute='project', widget=widgets.ForeignKeyWidget(Input))
    report = Field(column_name='report', attribute='report')
    year_neg_2 = Field(column_name='year_neg_2', attribute='year_neg_2')
    year_neg_1 = Field(column_name='year_neg_1', attribute='year_neg_1')
    year_0 = Field(column_name='year_0', attribute='year_0')
    year_pos_1 = Field(column_name='year_pos_1', attribute='year_pos_1')
    year_pos_2 = Field(column_name='year_pos_2', attribute='year_pos_2')
    year_pos_3 = Field(column_name='year_pos_3', attribute='year_pos_3')
    year_pos_4 = Field(column_name='year_pos_4', attribute='year_pos_4')
    year_pos_5 = Field(column_name='year_pos_5', attribute='year_pos_5')

    class Meta:
        model = FSAPL
        fields = ('id', 'project_id', 'report', 'year_neg_2', 'year_neg_1', 'year_0', 'year_pos_1', 'year_pos_2', 'year_neg_2', 'year_pos_3', 'year_pos_4', 'year_pos_5')

    def before_import_row(self, row, **kwargs):
        value = row['project']
        obj = Input.objects.filter(project=value)
        for i in obj:
            row['project'] = i.id


class FSABSResource(resources.ModelResource):
    project_id = Field(column_name='project', attribute='project', widget=widgets.ForeignKeyWidget(Input))
    report = Field(column_name='report', attribute='report')
    year_0 = Field(column_name='year_0', attribute='year_0')
    year_pos_1 = Field(column_name='year_pos_1', attribute='year_pos_1')
    year_pos_2 = Field(column_name='year_pos_2', attribute='year_pos_2')
    year_pos_3 = Field(column_name='year_pos_3', attribute='year_pos_3')
    year_pos_4 = Field(column_name='year_pos_4', attribute='year_pos_4')
    year_pos_5 = Field(column_name='year_pos_5', attribute='year_pos_5')

    class Meta:
        model = FSABS
        fields = ('id', 'project_id', 'report', 'year_0', 'year_pos_1', 'year_pos_2', 'year_neg_2', 'year_pos_3', 'year_pos_4', 'year_pos_5')

    def before_import_row(self, row, **kwargs):
        value = row['project']
        obj = Input.objects.filter(project=value)
        for i in obj:
            row['project'] = i.id


class WACCResource(resources.ModelResource):
    project_id = Field(column_name='project', attribute='project', widget=widgets.ForeignKeyWidget(Input))
    particulars = Field(column_name='particulars', attribute='particulars')
    percentage = Field(column_name='percentage', attribute='percentage')

    class Meta:
        model = WACC
        # fields = ('id', 'project_id', 'particulars', 'percentage')

    # def before_import_row(self, row, **kwargs):
    #     value = row['project']
    #     obj = Input.objects.filter(project=value)
    #     for i in obj:
    #         row['project'] = i.id
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset:
            if row[1] == '':
                raise ValidationError('hello')

