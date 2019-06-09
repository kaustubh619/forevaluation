from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm, InputsForm, Registration
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Input, FSAPLReport, FSABSReport, WACCParticulars, YOYGrowth, FSAPL, WACC, FSABS, DCF, Output
import xlwt
from .resources import FSAPLResource, FSABSResource, WACCResource
from tablib import Dataset
from django.contrib.auth.models import User


def registration(request):
    if request.user.username:
        return redirect(home)
    form = Registration()
    message = ''
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username__iexact=username).exists():
                return redirect(error)
            password = form.cleaned_data['password']
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            return redirect(log_in)
    return render(request, 'registration.html', {'form': form, 'msg': message})


def error(request):
    return render(request, 'registration_error.html')


def log_in(request):
    if request.user.username:
        return redirect(home)
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                message = 'Invalid log in details!'
            else:
                login(request, user)
                return redirect(home)
    return render(request, 'login.html', {'form': form, 'msg': message})


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def inputs(request):
    form = InputsForm()
    if request.method == 'POST':
        form = InputsForm(request.POST)
        if form.is_valid():
            obj = Input()
            obj.user = request.user
            obj.organization = form.cleaned_data['organization']
            obj.project = form.cleaned_data['project']
            obj.valuation_date = form.cleaned_data['valuation_date']
            obj.statutory_corporate_tax_rate = form.cleaned_data['statutory_corporate_tax_rate']
            obj.statutory_mat_rate = form.cleaned_data['statutory_mat_rate']
            obj.post_tax_wacc = form.cleaned_data['post_tax_wacc']
            obj.long_term_growth_rate = form.cleaned_data['long_term_growth_rate']
            obj.company_specific_risk = form.cleaned_data['company_specific_risk']
            obj.contingent_liability = form.cleaned_data['contingent_liability']
            obj.total_shares_outstanding = form.cleaned_data['total_shares_outstanding']
            obj.save()
            return redirect(user_details)
    return render(request, 'inputs.html', {'form': form})


@login_required(login_url='login')
def fsapl(request):
    user = request.user
    data_1 = Input.objects.filter(user=user)
    error = ''
    for i in data_1:
        pid = i.project
    id = request.GET['id']
    data = FSAPL.objects.filter(project=id)
    if request.method == 'POST':
        input_resource = FSAPLResource()
        dataset = Dataset()
        new_input = request.FILES['myFile']if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            imported_data = dataset.load(new_input.read())
            for i in imported_data['project']:
                vari = i
                break
            any_data = FSAPL.objects.filter(project=vari)
            if not any_data:
                result = input_resource.import_data(dataset, dry_run=True)  # Test the data import
                if result.has_errors():
                    error = "Invalid Input Data!"

                if not result.has_errors():
                    input_resource.import_data(dataset, dry_run=False)  # Actually import now
                    return redirect(user_details)
            else:
                error = 'Invalid Input Data!'
            # data = FSAPL.objects.all()
            # for i in data:
            #     obj = YOYGrowth()
            #     obj.project = i.project
            #     obj.report = i.report
            #     obj.year_neg_1 = i.yoy_growth_neg_1
            #     obj.year_0 = i.yoy_growth_0
            #     obj.year_pos_1 = i.yoy_growth_pos_1
            #     obj.year_pos_2 = i.yoy_growth_pos_2
            #     obj.year_pos_3 = i.yoy_growth_pos_3
            #     obj.year_pos_4 = i.yoy_growth_pos_4
            #     obj.year_pos_5 = i.yoy_growth_pos_5
            #     obj.save()
    return render(request, 'fsapl.html', {'data': data, 'pid': pid, 'error': error})


@login_required(login_url='login')
def fsapl_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="FSAP&L.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Input')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'project', 'report', 'year_neg_2', 'year_neg_1', 'year_0', 'year_pos_1', 'year_pos_2', 'year_pos_3', 'year_pos_4', 'year_pos_5']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = FSAPLReport.objects.all().values_list('report')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num+2, row[col_num], font_style)
    # row_num = 0
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num + 1, request.GET['id'], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def fsabs(request):
    user = request.user
    data_1 = Input.objects.filter(user=user)
    error = ''
    for i in data_1:
        pid = i.project
    id = request.GET['id']
    data = FSABS.objects.filter(project=id)
    if request.method == 'POST':
        input_resource = FSABSResource()
        dataset = Dataset()
        new_input = request.FILES['myFile']if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            imported_data = dataset.load(new_input.read())
            for i in imported_data['project']:
                vari = i
                break
            any_data = FSABS.objects.filter(project=vari)
            if not any_data:
                result = input_resource.import_data(dataset, dry_run=True)  # Test the data import
                if result.has_errors():
                    error = "Invalid Input Data!"

                if not result.has_errors():
                    input_resource.import_data(dataset, dry_run=False)  # Actually import now
                    return redirect(user_details)
            else:
                error = 'Invalid Input Data!'
    return render(request, 'fsabs.html', {'data': data, 'pid': pid, 'error': error})


@login_required(login_url='login')
def fsabs_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="FSABS.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Input')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'project', 'report', 'year_0', 'year_pos_1', 'year_pos_2',
               'year_pos_3', 'year_pos_4', 'year_pos_5']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = FSABSReport.objects.all().values_list('report')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], font_style)
    # row_num = 0
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num + 1, request.GET['id'], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def wacc(request):
    id = request.GET['id']
    data = WACC.objects.filter(project=id)
    error = ''
    user = request.user
    data_1 = Input.objects.filter(user=user)
    for i in data_1:
        pid = i.project
    if request.method == 'POST':
        input_resource = WACCResource()
        dataset = Dataset()
        new_input = request.FILES['myFile']if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            imported_data = dataset.load(new_input.read())
            for i in imported_data['project']:
                vari = i
                break
            any_data = WACC.objects.filter(project=vari)
            if not any_data:
                result = input_resource.import_data(dataset, dry_run=True)  # Test the data import
                if result.has_errors():
                    error = "Invalid Input Data!"

                if not result.has_errors():
                    input_resource.import_data(dataset, dry_run=False)  # Actually import now
                    return redirect(user_details)
            else:
                error = 'Invalid Input Data!'
    return render(request, 'wacc.html', {'data': data, 'pid': pid, 'error': error})


@login_required(login_url='login')
def wacc_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="WACC.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Input')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'project', 'particulars', 'percentage']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = WACCParticulars.objects.all().values_list('particulars')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], font_style)
    # row_num = 0
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, request.GET['id'], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def user_details(request):
    user = request.user
    data = Input.objects.filter(user=user)
    return render(request, 'user_details.html', {'data': data})


def log_out(request):
    logout(request)
    return redirect(log_in)


@login_required(login_url='login')
def dcf(request):
    id = request.GET['id']
    net_sales_data = FSAPL.objects.filter(project=id, report='Total Opertating Income')
    for i in net_sales_data:
        obj = DCF()
        growth_rate = Input.objects.filter(id=id)
        obj.project = i.project
        obj.report = 'Net Sales'
        obj.year_1 = i.year_pos_1
        ns1 = obj.year_1
        obj.year_2 = i.year_pos_2
        ns2 = obj.year_2
        obj.year_3 = i.year_pos_3
        ns3 = obj.year_3
        obj.year_4 = i.year_pos_4
        ns4 = obj.year_4
        obj.year_5 = i.year_pos_5
        ns5 = obj.year_5
        for j in growth_rate:
            gr = j.long_term_growth_rate
            obj.terminal_period = i.year_pos_5 * ((100 + j.long_term_growth_rate)/100)
            value = obj.terminal_period
        obj.save()
        obj = DCF()
        obj.project = i.project
        obj.report = 'Growth Rate in percentage'
        obj.year_1 = 0
        obj.year_2 = ((i.year_pos_2 - i.year_pos_1) / i.year_pos_1) * 100
        obj.year_3 = ((i.year_pos_3 - i.year_pos_2) / i.year_pos_2) * 100
        obj.year_4 = ((i.year_pos_4 - i.year_pos_3) / i.year_pos_3) * 100
        obj.year_5 = ((i.year_pos_5 - i.year_pos_4) / i.year_pos_4) * 100
        obj.terminal_period = gr
        obj.save()
    ebitda_data = FSAPL.objects.filter(project=id, report='EBITDA')
    for x in ebitda_data:
        obj = DCF()
        for a in net_sales_data:
            for b in ebitda_data:
                rate = b.year_pos_4/a.year_pos_5
        obj.project = x.project
        obj.report = 'Earnings Before Interest, Depreciation and Tax'
        obj.year_1 = x.year_0
        eb1 = obj.year_1
        obj.year_2 = x.year_pos_1
        eb2 = obj.year_2
        obj.year_3 = x.year_pos_2
        eb3 = obj.year_3
        obj.year_4 = x.year_pos_3
        eb4 = obj.year_4
        obj.year_5 = x.year_pos_4
        eb5 = obj.year_5
        obj.terminal_period = value*rate
        tp = obj.terminal_period
        obj.save()
        obj = DCF()
        obj.project = i.project
        obj.report = 'Margin in percentage'
        obj.year_1 = (eb1 / ns1) * 100
        obj.year_2 = (eb2 / ns2) * 100
        obj.year_3 = (eb3 / ns3) * 100
        obj.year_4 = (eb4 / ns4) * 100
        obj.year_5 = (eb5 / ns5) * 100
        obj.terminal_period = (eb5 / ns5) * 100
        obj.save()
    ebit_data = FSAPL.objects.filter(project=id, report="EBITDA")
    for i in ebit_data:
        obj = DCF()
        dbj = DCF()
        obj.project = i.project
        obj.report = "Earnings Before Interest and Tax"
        depreciation_data = FSAPL.objects.filter(project=id, report="Depreciation")
        for j in depreciation_data:
            obj.year_1 = i.year_0 - j.year_pos_1
            dp_1 = j.year_pos_1
            ebit_year_1 = obj.year_1
            obj.year_2 = i.year_pos_1 - j.year_pos_2
            dp_2 = j.year_pos_2
            ebit_year_2 = obj.year_2
            obj.year_3 = i.year_pos_2 - j.year_pos_3
            dp_3 = j.year_pos_3
            ebit_year_3 = obj.year_3
            obj.year_4 = i.year_pos_3 - j.year_pos_4
            dp_4 = j.year_pos_4
            ebit_year_4 = obj.year_4
            obj.year_5 = i.year_pos_4 - j.year_pos_5
            dp_5 = j.year_pos_5
            ebit_year_5 = obj.year_5
            gross_block_data = FSABS.objects.filter(project=id, report="Gross Block")
            for k in gross_block_data:
                depreciation = k.year_pos_5 - k.year_pos_4
            obj.terminal_period = tp - depreciation
            tp_value = obj.terminal_period
            dbj.project = i.project
            dbj.report = 'Less: Depreciation'
            dbj.year_1 = dp_1
            dbj.year_2 = dp_2
            dbj.year_3 = dp_3
            dbj.year_4 = dp_4
            dbj.year_5 = dp_5
            dbj.terminal_period = depreciation
            dbj.save()
            obj.save()
        obj = DCF()
        obj.project = i.project
        obj.report = 'Margin in percentage'
        obj.year_1 = (ebit_year_1 / ns1) * 100
        obj.year_2 = (ebit_year_2 / ns2) * 100
        obj.year_3 = (ebit_year_3 / ns3) * 100
        obj.year_4 = (ebit_year_4 / ns4) * 100
        obj.year_5 = (ebit_year_5 / ns5) * 100
        obj.terminal_period = (tp_value / value) * 100
        obj.save()
    fsapl_data = FSAPL.objects.filter(project=id)
    for d in fsapl_data:
        input_data = Input.objects.filter(id=id)
        for i in input_data:
            x = i.statutory_corporate_tax_rate
        obj = DCF()
        obj.project = d.project
        obj.report = "Gross Free Cash Flows to Equity"
        obj.year_1 = ebit_year_1 - (ebit_year_1 * (x/100))
        it1 = ebit_year_1 * (x/100)
        gfcg_1 = obj.year_1
        obj.year_2 = ebit_year_2 - (ebit_year_2 * (x/100))
        it2 = ebit_year_2 * (x/100)
        gfcg_2 = obj.year_2
        obj.year_3 = ebit_year_3 - (ebit_year_3 * (x/100))
        it3 = ebit_year_3 * (x/100)
        gfcg_3 = obj.year_3
        obj.year_4 = ebit_year_4 - (ebit_year_4 * (x/100))
        it4 = ebit_year_4 * (x/100)
        gfcg_4 = obj.year_4
        obj.year_5 = ebit_year_5 - (ebit_year_5 * (x/100))
        it5 = ebit_year_5 * (x/100)
        gfcg_5 = obj.year_5
        obj.terminal_period = tp_value - (tp_value * (x/100))
        ittp = tp_value * (x/100)
        gfcg_tp = obj.terminal_period
        it = DCF()
        it.project = d.project
        it.report = 'Income Tax'
        it.year_1 = it1
        it.year_2 = it2
        it.year_3 = it1
        it.year_4 = it4
        it.year_5 = it5
        it.terminal_period = ittp
        etr = DCF()
        etr.project = d.project
        etr.report = 'Effective Tax Rate (c) in percentage'
        etr.year_1 = x
        etr.year_2 = x
        etr.year_3 = x
        etr.year_4 = x
        etr.year_5 = x
        etr.terminal_period = x
        dep = DCF()
        dep.project = d.project
        dep.report = 'Add: Depreciation'
        dep.year_1 = dp_1
        dep.year_2 = dp_2
        dep.year_3 = dp_3
        dep.year_4 = dp_4
        dep.year_5 = dp_5
        dep.terminal_period = depreciation
    it.save()
    etr.save()
    obj.save()
    dep.save()
    fsabs_data = FSABS.objects.filter(project=id, report='Gross Block')
    for i in fsabs_data:
        obj = DCF()
        ice = DCF()
        cnc = DCF()
        obj.project = i.project
        ice.project = i.project
        cnc.project = i.project
        obj.report = "Net Free Cash Flows to Equity"
        ice.report = 'Less: Increase in Capital Expenditure'
        cnc.report = 'Add/Less: Change in Non Cash Net Working Capital'
        ciwc_data = FSABS.objects.filter(project=id, report='Change in Working Capital')
        for n in ciwc_data:
            obj.year_1 = gfcg_1 + dp_1 - (i.year_pos_1-i.year_0) - n.year_pos_1
            ice.year_1 = i.year_pos_1-i.year_0
            cnc.year_1 = n.year_pos_1
            z1 = obj.year_1
            obj.year_2 = gfcg_2 + dp_2 - (i.year_pos_2-i.year_pos_1) - n.year_pos_2
            ice.year_2 = i.year_pos_2-i.year_pos_1
            cnc.year_2 = n.year_pos_2
            z2 = obj.year_2
            obj.year_3 = gfcg_3 + dp_3 - (i.year_pos_3-i.year_pos_2) - n.year_pos_3
            ice.year_3 = i.year_pos_3-i.year_pos_2
            cnc.year_3 = n.year_pos_3
            z3 = obj.year_3
            obj.year_4 = gfcg_4 + dp_4 - (i.year_pos_4-i.year_pos_3) - n.year_pos_4
            ice.year_4 = i.year_pos_4-i.year_pos_3
            cnc.year_4 = n.year_pos_4
            z4 = obj.year_4
            obj.year_5 = gfcg_5 + dp_5 - depreciation - n.year_pos_5
            ice.year_5 = depreciation
            cnc.year_5 = n.year_pos_5
            z5 = obj.year_5
            obj.terminal_period = gfcg_tp - (n.year_pos_5/(ns5-ns4)*(value-ns5))
            ice.terminal_period = depreciation
            cnc.terminal_period = n.year_pos_5/(ns5-ns4)*(value-ns5)
            ztp = obj.terminal_period
        ice.save()
        cnc.save()
        obj.save()
    f_data = FSABS.objects.filter(project=id)
    for i in f_data:
        obj = DCF()
        pv = DCF()
        obj.project = i.project
        pv.project = i.project
        obj.report = "Present Value of Free Cash Flows to Equity"
        pv.report = "Present Value Factors (d)"
        i_data = Input.objects.filter(id=id)
        for j in i_data:
            ptwacc = j.post_tax_wacc
        obj.year_1 = z1 / ((1 + (ptwacc / 100)) ** (1 / 2))
        pv.year_1 = 1/((1 + (ptwacc / 100)) ** (1 / 2))
        i_value1 = obj.year_1
        obj.year_2 = z2 / ((1 + (ptwacc / 100)) ** (3 / 2))
        pv.year_2 = 1/((1 + (ptwacc / 100)) ** (3 / 2))
        i_value2 = obj.year_2
        obj.year_3 = z3 / ((1 + (ptwacc / 100)) ** (5 / 2))
        pv.year_3 = 1/((1 + (ptwacc / 100)) ** (5 / 2))
        i_value3 = obj.year_3
        obj.year_4 = z4 / ((1 + (ptwacc / 100)) ** (7 / 2))
        pv.year_4 = 1/((1 + (ptwacc / 100)) ** (7 / 2))
        i_value4 = obj.year_4
        obj.year_5 = z5 / ((1 + (ptwacc / 100)) ** (9 / 2))
        pv.year_5 = 1/((1 + (ptwacc / 100)) ** (9 / 2))
        t_value = (1 + (ptwacc / 100)) ** (9 / 2)
        i_value5 = obj.year_5
        obj.terminal_period = 0
        pv.terminal_period = 0
    pv.save()
    obj.save()
    n_data = FSAPL.objects.filter(project=id)
    obj = Output()
    for i in n_data:
        obj.project = i.project
        a_data = Input.objects.filter(id=id)
        for j in a_data:
            prate = j.post_tax_wacc
            lrate = j.long_term_growth_rate
        obj.long_term_sustainable_growth_rate = lrate
        obj.terminal_value = ztp/((prate-lrate)/100)
        x_value = obj.terminal_value
        i_total = i_value1 + i_value2 + i_value3 + i_value4 + i_value5
        obj.sum_of_present_value_of_net_free_cash_flows_to_equity = i_total
        l_value = x_value * (1/t_value)
        obj.present_value_of_terminal_value = l_value
        obj.gross_equity_value = i_total + l_value
        final_value = obj.gross_equity_value
        for a in FSABS.objects.filter(project=id, report="Investments"):
            ab_value = a.year_pos_1
            obj.investments = ab_value
        for b in FSABS.objects.filter(project=id, report="Cash & Bank"):
            bc_value = b.year_pos_1
            obj.cash_and_equivalent = bc_value
        for c in FSABS.objects.filter(project=id, report="Other Assets"):
            cd_value = c.year_pos_1
            obj.other_non_current_assets = cd_value
        for d in FSABS.objects.filter(project=id, report="Preference Shares"):
            de_value = d.year_pos_1
            obj.pref_shares = de_value
        for e in FSABS.objects.filter(project=id, report="Total Loan Funds"):
            ef_value = e.year_pos_1
            obj.debt = ef_value
        for f in Input.objects.filter(id=id):
            fg_value = f.contingent_liability
            obj.contingent_liabilities = fg_value
        obj.equity_value = final_value + ab_value + bc_value + cd_value - de_value - ef_value - fg_value
    obj.save()
    return redirect(user_details)


def vdcf(request):
    id = request.GET['id']
    data = DCF.objects.filter(project=id)
    output = Output.objects.filter(project=id)
    wacc_data = WACC.objects.filter(project=id)
    pl_data = FSAPL.objects.filter(project=id)
    bs_data = FSABS.objects.filter(project=id)
    return render(request, 'vdcf.html', {'data': data, 'output': output, 'id': id, 'wacc_data': wacc_data, 'pl_data': pl_data, 'bs_data': bs_data})


def delete_input(request):
    id = request.GET['id']
    data = Input.objects.get(id=id)
    data.delete()
    return redirect(user_details)


@login_required(login_url='login')
def dcf_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="DCF.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Input')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['project', 'report', 'year_1', 'year_2', 'year_3', 'year_4', 'year_5', 'terminal_period']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    id = request.GET['id']

    rows = DCF.objects.filter(project=id).values_list('project', 'report', 'year_1', 'year_2', 'year_3', 'year_4', 'year_5', 'terminal_period')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            # print(row_num, col_num, row[col_num])
            ws.write(row_num, col_num, row[col_num], font_style)

    ocol = ['Long Term Sustainable Growth Rate', 'Terminal Value', 'Sum of Present Value of Net Free Cash Flows to Equity', 'Present Value of Terminal Value', 'Gross Equity Value', 'Add: Investments', 'Add: Cash & Equivalent', 'Add: Other Non Current Assets', 'Less: Preference Shares as on Valuation Date', 'Less: Debt', 'Less: Contingent Liabilities', 'Equity Value']
    ac = 1
    for x in range(len(ocol)):
        ws.write(x+18, ac, ocol[x], font_style)
    abcd = 1
    za = Output.objects.filter(project=id).values_list('long_term_sustainable_growth_rate', 'terminal_value', 'sum_of_present_value_of_net_free_cash_flows_to_equity', 'present_value_of_terminal_value', 'gross_equity_value', 'investments', 'cash_and_equivalent', 'other_non_current_assets', 'pref_shares', 'debt', 'contingent_liabilities', 'equity_value')
    for i in za:
        abcd += 1
        for j in range(len(i)):
            ws.write(j+18, abcd, i[j], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def wacc_delete(request):
    id = request.GET['id']
    data = WACC.objects.filter(project=id)
    data.delete()
    return redirect(user_details)


@login_required(login_url='login')
def fsapl_delete(request):
    id = request.GET['id']
    data = FSAPL.objects.filter(project=id)
    data.delete()
    return redirect(user_details)


@login_required(login_url='login')
def fsabs_delete(request):
    id = request.GET['id']
    data = FSABS.objects.filter(project=id)
    data.delete()
    return redirect(user_details)


@login_required(login_url='login')
def dcf_delete(request):
    id = request.GET['id']
    data = DCF.objects.filter(project=id)
    o_data = Output.objects.filter(project=id)
    o_data.delete()
    data.delete()
    return redirect(user_details)
