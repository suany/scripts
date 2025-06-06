#!/usr/bin/env python3
#
# openpyxl or xlswriter
#
# Alt: Data processing in python:
#   pandas library: pd.read_excel()
#   DataFrame.plot
#
# Excel functions
#   xlookup (2021), mine is 2016
#   -> in any case, would be quite clunky

import math, sys
from intervaltree import IntervalTree # pip3 install intervaltree
from openpyxl import load_workbook, Workbook # pip3 install openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

class Err(Exception):
    def __str__(self):
        return "\n" + self.args[0]

def verbose(*args, **kwargs):
    #pass
    print(*args, **kwargs)

def account_number(s):
    match s:
        case str():
            if len(s) < 5:
                return None
            if s[4] != ' ':
                return None
            try:
                return int(s[:4])
            except:
                return None
        case int():
            return s
        case x:
            raise Err("Bad type:" + str(type(x)))

def interval_lookup(interval_tree, number):
    if number is None:
        return None
    intervals = interval_tree.at(number)
    match len(intervals):
        case 0:
            return None
        case 1:
            return next(iter(intervals)).data
        case n:
            raise

# XXX unused, TODO
acct_categories = IntervalTree.from_tuples([
    (1000, 1999, ("Assets")),
    (2000, 2999, ("Liabilities")),
    (3000, 3999, ("Equities")),
    (4000, 4199, ("Income", "Normal")),
    (4200, 4399, ("Income", "Carport")),
    (4400, 4599, ("Income", "Interest")),
    (4600, 4799, ("Income")),
    (4800, 4899, ("Income", "Miscellaneous/bookkeeping")),
    (4900, 4999, ("Income")),
    (5000, 5199, ("Expenses", "Operational", "Administrative")),
    (5200, 5399, ("Expenses", "Operational", "Regular services")),
    (5400, 5599, ("Expenses", "Operational", "Routine maintenance")),
    (5600, 5799, ("Expenses", "Operational", "Maintenance and repair")),
    (5800, 5999, ("Expenses", "Operational", "Miscellaneous/bookkeeping")),
    (6000, 6999, ("Expenses", "Resident Property Improvements")),
    (7000, 7999, ("Expenses", "Common Property Improvements (Capital)")),
    (8000, 8499, ("Expenses", "Carport Maintenance (Operational)")),
    (8500, 8999, ("Expenses", "Carport Improvements")),
    ])

# Data is int, str pair, where int is used for sorting, 
expense_buckets = IntervalTree.from_tuples([
    (5000, 5199, (1, "Administrative")),
    (5200, 5399, (2, "Regular services")),
    (5400, 5599, (3, "Routine maintenance")),
    (5600, 5799, (4, "Maintenance and repair")),
    (5800, 5999, (5, "Contingency/Misc")),
    (6000, 6999, (6, "Resident Property Improvements")),
    (7000, 7999, (7, "Common Property Improvements")),
    #(8000, 8999, (8, "Carport")),
    ])

# Main sections
income_range = (4000, 4999)   # lb, ub
expenses_range = (5000, 8999) # lb, ub
other_income = (4850, 4860) # Donations, Prior Period Clean Up
other_expenses = (5900,) # Asset Depreciation

def is_income(acctno):
    return (acctno is not None
            and acctno >= income_range[0] and acctno <= income_range[1]
            and acctno not in other_income)
def is_expense(acctno):
    return (acctno is not None
            and acctno >= expenses_range[0] and acctno <= expenses_range[1]
            and acctno not in other_expenses)

class Sections(object):
    def __init__(self, accts):
        self.income = []
        self.expenses = []
        self.other_income = []
        self.other_expenses = []
        self.unnumbered = [] # should not happen?
        self.other = [] # should not happen?
        self.init(accts)

    def init(self, accts):
        for acct in accts:
            acctno = account_number(acct)
            if acctno is None:
                self.unnumbered.append(acct)
                continue
            if is_income(acctno):
                self.income.append(acct)
                continue
            if is_expense(acctno):
                self.expenses.append(acct)
                continue
            if acctno in other_income:
                self.other_income.append(acct)
                continue
            if acctno in other_expenses:
                self.other_expenses.append(acct)
                continue
            self.other.append(acct)

    def __repr__(self):
        def list2str(name, lst):
            s = f"  {name}=[\n"
            for item in lst:
                s += f"    {repr(item)},\n"
            s += "  ],\n"
            return s
        return ("Sections(\n"
            + list2str("income", self.income)
            + list2str("expenses", self.expenses)
            + list2str("other_income", self.other_income)
            + list2str("other_expenses", self.other_expenses)
            + list2str("unnumbered", self.unnumbered)
            + list2str("other", self.other)
            + ")\n")

class Subaccounts(object):
    def __init__(self, tuples):
        self.num2parent = IntervalTree.from_tuples(tuples)
        self.parent_strs = set(i[2] for i in self.num2parent.items())
        self.parent_num2str = { account_number(s) :
                                s for s in self.parent_strs }

    def is_child_of(self, child, parent):
        p = interval_lookup(self.num2parent, account_number(child))
        if p is None:
            return False
        return account_number(p) == account_number(parent)

    def is_parent(self, acct):
        match acct:
            case str():
                if acct in self.parent_strs:
                    return True
                acctno = account_number(acct)
                if acctno in self.parent_num2str:
                    print("Warning: subaccount number matches but not string:",
                          acct, self.parent_num2str[acctno])
                    return True
                return False
            case int():
                return acct in self.parent_num2str
            case _:
                raise

subaccounts = Subaccounts([
    #(4401, 4499, "4400 Interest Income"), # Not subaccounts - better this way
    (5601, 5799, "5600 Repairs and Maintenance"),
    (6001, 6999, "6000 Resident Property Improvement"), # FIXME ment/ments
    (7001, 7999, "7000 Common Property Improvements"), # FIXME ment/ments
    ])

class Acct2Entries(object):
    def __init__(self):
        self.numbered = dict()
        self.unnumbered = dict()
        self.acct_header = None
        self.headers = set()
        self.prefix_rows = []
        self.suffix_rows = []
        self.months = None  # str "January-April"
        self.nmonths = None # int

    def set_months(self, months, nmonths):
        assert self.months is None
        assert self.nmonths is None
        self.months = months
        self.nmonths = nmonths

    def numbered_get_entries(self, acct):
        if not acct in self.numbered:
            self.numbered[acct] = dict()
        return self.numbered[acct]

    def unnumbered_get_entries(self, acct):
        if not acct in self.unnumbered:
            self.unnumbered[acct] = dict()
        return self.unnumbered[acct]

    def __repr__(self):
        rv = "Acct2Entries(\n"
        rv += f"  Acct Header: {self.acct_header}\n"
        rv += f"  Headers({len(self.headers)}):"
        for h in self.headers:
            rv += f" {h}"
        rv += f"\n  Prefix Rows({len(self.prefix_rows)}):\n"
        for r in self.prefix_rows:
            rv += f"    {r}\n"
        rv += f"\n  Suffix Rows({len(self.suffix_rows)}):\n"
        for r in self.suffix_rows:
            rv += f"    {r}\n"
        rv += f"\n  Numbered Accts({len(self.numbered)}):\n"
        for k1 in sorted(self.numbered.keys()):
            rv += f"    {k1}\n"
            for k2 in sorted(self.numbered[k1].keys()):
                rv += f"      {k2}={self.numbered[k1][k2]}\n"
        rv += f"\n  Unnumbered Accts({len(self.unnumbered)}):\n"
        for k1 in sorted(self.unnumbered.keys()):
            rv += f"    {k1}\n"
            for k2 in sorted(self.unnumbered[k1].keys()):
                rv += f"      {k2}={self.unnumbered[k1][k2]}\n"
        rv += ")"
        return rv

def read_entries(ws, a2e,
                 table_header1 = "Distribution account",
                 keep_affixes = False):
    # Prefix: entry_headers is None     in_table = False
    # Table:  entry_headers is not None in_table = True
    # Suffix: entry_headers is not None in_table = False
    entry_headers = None
    in_table = False
    for row in ws.rows:
        rowvals = [x.value for x in row]
        acct = rowvals[0]
        if entry_headers is None:
            if acct != table_header1:
                # Haven't found headers: this is a prefix
                if keep_affixes:
                    a2e.prefix_rows.append(rowvals)
                continue
            if a2e.acct_header and a2e.acct_header != table_header1:
                print("Warning: header mismatch",
                      a2e.acct_header, table_header1)
            a2e.acct_header = table_header1
            entry_headers = rowvals[1:]
            a2e.headers.update(entry_headers)
            in_table = True
            continue
        if not in_table: # This is a suffix
            a2e.suffix_rows.append(rowvals)
            continue
        if not acct: # This is the start of the suffix
            in_table = False
            if keep_affixes:
                a2e.suffix_rows.append(rowvals)
            else: # Short circuit (not worth it?)
                verbose(f"Empty first cell, stopping at {row}")
                break
            continue
        if len(row) != len(entry_headers) + 1:
            ncols = len(row) - 1
            nhdrs = len(entry_headers)
            print("Warning: expected {nhdrs} got {ncols} columns, at {row}")
            assert ncols > nhdrs
        if account_number(acct):
            entries = a2e.numbered_get_entries(acct)
        else:
            entries = a2e.unnumbered_get_entries(acct)
        for i, hdr in enumerate(entry_headers):
            if hdr in entries:
                print(f"Warning: duplicate entry, hdr={hdr} acct={acct}")
            entries[hdr] = rowvals[i+1]
    return a2e

def check_header_presence(ref, data):
    for hdr in ref:
        if hdr not in data:
            print("Warning: {hdr} absent in data")

class Style(object):
    def __init__(self, bold = False, fontsize = 8, indent = 0,
                 underline = False, overline = False, center = False):
        self.bold = bold
        self.fontsize = fontsize
        self.indent = indent
        self.underline = underline
        self.overline = overline
        self.center = center

    def _font(self, cell):
        cell.font = Font(name = "Arial",
                         size = self.fontsize,
                         bold = self.bold)
    def _border(self, cell, underline, overline):
        if not underline and not overline:
            return
        top = None
        if overline:
            top = Side(border_style = 'thin', color = 'FF000000')
        bottom = None
        if underline:
            bottom = Side(border_style = 'thin', color = 'FF000000')
        cell.border = Border(top = top, bottom = bottom)
    def _center(self):
        return 'center' if self.center else None
    def text(self, cell): # For headers and footers
        self._font(cell)
        cell.alignment = Alignment(horizontal = self._center(), vertical='top')
    def acct(self, cell): # For account column entry (or header)
        self._font(cell)
        self._border(cell, self.underline, False) # no overline for account
        cell.alignment = Alignment(horizontal = self._center(), vertical='top',
                                   indent=self.indent)
    def actual(self, cell): # For actual column entry (or header) ~= budget
        self._font(cell)
        self._border(cell, self.underline, self.overline)
        cell.alignment = Alignment(horizontal = self._center(), vertical='top')
        cell.number_format = "#,##0.00"
    def budget(self, cell): # For budget column entry (or header) ~= actual
        self._font(cell)
        self._border(cell, self.underline, self.overline)
        cell.alignment = Alignment(horizontal = self._center(), vertical='top')
        cell.number_format = "#,##0.00"
    def pct(self, cell): # For pct column entry (or header)
        self._font(cell)
        self._border(cell, self.underline, self.overline)
        cell.alignment = Alignment(horizontal = self._center(), vertical='top')
        cell.number_format = "##0.0%"
    def note(self, cell): # For note column entry (or header)
        self._font(cell)
        self._border(cell, self.underline, False) # no overline for note
        cell.alignment = Alignment(horizontal = self._center(), vertical='top',
                                   wrap_text = True)

def set_column_widths(ws):
    # Set column widths - these work well for 2025
    ws.column_dimensions['A'].width = 31 # =310px
    ws.column_dimensions['B'].width = 9
    ws.column_dimensions['C'].width = 9
    ws.column_dimensions['D'].width = 7
    ws.column_dimensions['E'].width = 1
    ws.column_dimensions['F'].width = 26

def add_row(ws, rowno, acct,
            actual = None, budget = None, notes = None, pct = None,
            style = Style()):
    a = ws.cell(row = rowno, column = 1, value = acct)       # A
    style.acct(a)
    b = ws.cell(row = rowno, column = 2, value = actual)     # B
    style.actual(b)
    if budget: # Skip budget and % if 0
        c = ws.cell(row = rowno, column = 3, value = budget) # C
        style.budget(c)
        if pct is None:
            pct = f"=B{rowno}/C{rowno}"
        d = ws.cell(row = rowno, column = 4, value = pct)    # D
        style.pct(d)
    f = ws.cell(row = rowno, column = 6, value = notes)      # F
    style.note(f)

class ActualBudget(object):
    def __init__(self, actual = 0, budget = 0):
        self.actual = actual
        self.budget = budget
    def __bool__(self):
        return self.actual or self.budget
    def __add__(self, rhs):
        return ActualBudget(self.actual + rhs.actual, self.budget + rhs.budget)
    def __sub__(self, rhs):
        return ActualBudget(self.actual - rhs.actual, self.budget - rhs.budget)
    def __repr__(self):
        return f"actual={self.actual} budget={self.budget}"

def sanity_check_numbers(a2e, acct, total):
    entry = a2e.unnumbered.get(acct, None)
    if entry is None:
        return
    # Each may be None, float, or formula string (like "=B7+B8...")
    actual = entry.get("Total", None)
    budget = entry.get("Budget", None)
    if isinstance(actual, float) and not math.isclose(actual, total.actual):
        print(f"Warning: {acct} actual mismatch: {actual} vs {total.actual}")
    if isinstance(budget, float) and not math.isclose(budget, total.budget):
        print(f"Warning: {acct} budget mismatch: {budget} vs {total.budget}")

def addcells_section(ws, rowno, secname, accts, a2e):
    add_row(ws, rowno, secname)
    rowno += 1
    total = ActualBudget()
    curparent = None
    curparent_tot = None # tied to curparent
    for acct in accts:
        entries = a2e.numbered[acct]
        actual = entries.get("Total", None)
        budget = entries.get("Budget", None)
        notes = entries.get("Notes", None)
        indent = 1
        if curparent is not None:
            if subaccounts.is_child_of(acct, curparent):
                verbose("  Child", acct)
                indent = 2
                curparent_tot.actual += 0 if actual is None else actual
                curparent_tot.budget += 0 if budget is None else budget
            else:
                # Close out curparent and curparent_tot
                verbose("End parent", acct)
                totalname = "Total for " + curparent
                add_row(ws, rowno, totalname,
                        curparent_tot.actual, curparent_tot.budget,
                        style = Style(bold = True, indent = 1))
                rowno += 1
                # Sanity check against a2e entry
                sanity_check_numbers(a2e, totalname, curparent_tot)
                curparent = None
                curparent_tot = None
        elif subaccounts.is_parent(acct):
            if actual == 0:
                actual = None
            if budget == 0:
                budget = None
            curparent = acct
            curparent_tot = ActualBudget()
            verbose("Begin parent", acct)
        add_row(ws, rowno, acct, actual, budget, notes,
                style = Style(indent = indent))
        rowno += 1
        total.actual += 0 if actual is None else actual
        total.budget += 0 if budget is None else budget
    totalname = "Total for " + secname
    if accts:
        add_row(ws, rowno, totalname, total.actual, total.budget,
                style = Style(bold = 1, overline = 1))
        rowno += 1
    # Sanity check against a2e entry
    sanity_check_numbers(a2e, totalname, total)
    return rowno, total

def merge_row(ws, rowno, lcol = 1, rcol = 6):
    ws.merge_cells(start_row=rowno, end_row=rowno,
                   start_column=lcol, end_column=rcol)

MONTHS = {
    "January"   : 1,
    "February"  : 2,
    "March"     : 3,
    "April"     : 4,
    "May"       : 5,
    "June"      : 6,
    "July"      : 7,
    "August"    : 8,
    "September" : 9,
    "October"  : 10,
    "November" : 11,
    "December" : 12,
}

def parse_duration(s):
    months = s.split(",", 1)[0].split("-", 1)
    month1 = MONTHS.get(months[0], None)
    if month1 is None:
        return None
    if len(months) == 1:
        print("Duration is one month:", s)
        return 1
    month2 = MONTHS.get(months[1], None)
    if month2 is None:
        print("Warning: expecting second month:", s, months)
    assert month2 > month1
    return month2 - month1 + 1
    
def addcells_pnl_vs_budget(ws, pnlws, a2e):
    rowno = 1
    ###########
    # Prefix Rows
    for row in a2e.prefix_rows:
        style = None
        fontsize = { 1: 14, 2: 12, 3: 10 }.get(rowno, None)
        if fontsize is not None:
            style = Style(fontsize=fontsize, bold=True, center=True)
        for colno, val in enumerate(row, start = 1):
            if not val:
                continue
            if val == "Profit and Loss":
                val += " vs Budget"
            dur = parse_duration(val)
            if dur is not None:
                a2e.set_months(val, dur)
                val += " (" + str(round(dur * 100 / 12)) + "% of year)"
            newcell = ws.cell(row = rowno, column = colno, value = val)
            if style is not None:
                style.text(newcell)
            merge_row(ws, rowno)
        rowno += 1
    ###########
    # Headers
    verbose("Headers:", a2e.headers)
    check_header_presence(("Total", "Budget", "Notes"), a2e.headers)
    add_row(ws, rowno, a2e.acct_header,
            "Actual", "Budget", "Notes", pct = "Pct",
            style = Style(bold = True, fontsize = 9,
                          underline = True, center = True))
    rowno += 1
    ###########
    # Table
    secs = Sections(sorted(a2e.numbered))
    if secs.unnumbered:
        print(f"Warning: unnumbered accounts ({len(secs.unnumbered)}):")
        for acct in secs.unnumbered:
            print("  ", acct)
    if secs.other:
        print(f"Warning: unexpected accounts ({len(secs.other)}):")
        for acct in secs.other:
            print("  ", acct)
    # Income and Expenses
    rowno, income = addcells_section(
                        ws, rowno, "Income", secs.income, a2e)
    rowno, expenses = addcells_section(
                        ws, rowno, "Expenses", secs.expenses, a2e)
    # Net Operating Income
    netop = income - expenses
    nopi = "Net Operating Income"
    add_row(ws, rowno, nopi, netop.actual, netop.budget,
            style = Style(bold = True, overline = True))
    rowno += 1
    sanity_check_numbers(a2e, nopi, netop)
    # Other Income and Expenses
    rowno, oincome = addcells_section(
                        ws, rowno, "Other Income", secs.other_income, a2e)
    rowno, oexpenses = addcells_section(
                        ws, rowno, "Other Expenses", secs.other_expenses, a2e)
    # Net Other Income
    netoth = oincome - oexpenses
    noti = "Net Other Income"
    add_row(ws, rowno, noti, netoth.actual, netoth.budget,
            style = Style(bold = True, overline = True))
    rowno += 1
    sanity_check_numbers(a2e, noti, netoth)
    # Net Income
    netinc = netop + netoth
    ni = "Net Income"
    add_row(ws, rowno, ni, netinc.actual, netinc.budget,
            style = Style(bold = True, overline = True))
    rowno += 1
    sanity_check_numbers(a2e, ni, netinc)
    ###########
    # Suffix Rows
    for row in a2e.suffix_rows:
        for colno, val in enumerate(row, start = 1):
            if val is not None:
                newcell = ws.cell(row = rowno, column = colno, value = val)
                Style().text(newcell)
                merge_row(ws, rowno)
        rowno += 1
    ###########

def collect_expense_buckets(a2e) -> dict[str, ActualBudget]:
    buckets = dict()
    for acct in a2e.numbered:
        bucket = interval_lookup(expense_buckets, account_number(acct))
        if bucket is None:
            continue
        ba = buckets.setdefault(bucket, ActualBudget())
        entries = a2e.numbered[acct]
        ba.actual += entries.get("Total", 0)
        ba.budget += entries.get("Budget", 0)
    return buckets

def create_buckets_worksheet(wb, buckets, months, nmonths):
    budget_total = sum([ab.budget for ab in buckets.values()])
    assert budget_total
    budget_min = min([ab.budget for ab in buckets.values()])
    assert budget_min # min height = 12
    ws = wb.create_sheet(title = "Buckets")
    ROW_0 = 4
    COL_0 = 2
    HORIZ_NCELLS = 24
    COL_N = COL_0 + HORIZ_NCELLS
    for colno in range(COL_0, COL_N):
        ws.column_dimensions[get_column_letter(colno)].width = 1 # =10px
    ws.column_dimensions[get_column_letter(COL_N)].width = 2 # blank
    ws.column_dimensions[get_column_letter(COL_N+1)].width = 6 # pct
    ws.column_dimensions[get_column_letter(COL_N+2)].width = 10 # act/bud
    ws.column_dimensions[get_column_letter(COL_N+3)].width = 30 # acct
    curmonth_colno = None
    if nmonths is not None:
        curmonth_colno = nmonths * HORIZ_NCELLS / 12
    last_colno = COL_N + 3
    green = PatternFill(patternType='solid', fgColor='00CC00')
    cyan = PatternFill(patternType='solid', fgColor='00CCCC')
    yellow = PatternFill(patternType='solid', fgColor='FFFFCC')
    thinline = Side(border_style='thin', color='FF000000')
    dashedline = Side(border_style='dashed', color='FFFF0000')
    topbot = Border(top=thinline, bottom=thinline)
    topbotleft = Border(top=thinline, bottom=thinline,left=thinline)
    topbotright = Border(top=thinline, bottom=thinline, right=thinline)
    topbotrightdash = Border(top=thinline, bottom=thinline, right=dashedline)
    last_rowno = ROW_0
    for rowno, idxtext in enumerate(sorted(buckets), start=ROW_0):
        ba = buckets[idxtext]
        if not ba.budget:
            raise # TODO render buckets with 0 budget
        else:
            width = round(ba.actual * HORIZ_NCELLS / ba.budget)
            height = round(ba.budget * 12 / budget_min, 1)
            for i in range(0, HORIZ_NCELLS):
                cell = ws.cell(row = rowno, column = COL_0 + i)
                # XXX spent_color = green if rowno % 2 else cyan
                spent_color = green # XXX
                cell.fill = spent_color if i < width else yellow
                if i == 0:
                    cell.border = topbotleft
                elif i == HORIZ_NCELLS - 1:
                    cell.border = topbotright
                elif i == curmonth_colno:
                    cell.border = topbotrightdash
                else:
                    cell.border = topbot
            ws.row_dimensions[rowno].height = height
            verbose(f"Bucket height {height} : {idxtext[1]}")
        pct = ws.cell(row = rowno, column = COL_N + 1,
                      value = ba.actual / ba.budget)
        pct.number_format = "##0.0%"
        pct.alignment = Alignment(horizontal = 'right', vertical='center')
        budk = ws.cell(row = rowno, column = COL_N + 2,
                       value = (str(round(ba.actual / 1000)) + "k/" +
                                str(round(ba.budget / 1000)) + "k"))
        budk.alignment = Alignment(horizontal = 'right', vertical='center')
        bkt = ws.cell(row = rowno, column = COL_N + 3, value = idxtext[1])
        bkt.alignment = Alignment(horizontal = 'left', vertical='center')
        last_rowno = rowno
    # Write headers and footers - do this after we know last_colno
    # Headers: title and months
    ttl = ws.cell(row=1, column=COL_0,
                    value="Expenses vs Budget (excludes Carport)")
    Style(fontsize=14, bold=True, center=True).text(ttl)
    merge_row(ws, 1, COL_0, last_colno)
    ws.row_dimensions[1].height = 18
    if months:
        mths = ws.cell(row=2, column=COL_0, value=months)
        Style(fontsize=12, bold=True, center=True).text(mths)
        merge_row(ws, 2, COL_0, last_colno)
        ws.row_dimensions[2].height = 16
    # Footer: explanation
    expl_text = [
        "Each box represents an expense bucket. Its height indicates how much",
        "how much is budgeted for that bucket. The green portion to the left",
        "shows the amount spent year-to-date."
        ]
    if nmonths is not None:
        expl_text.append("The red line indicates where we are in the year" +
                         f" ({nmonths}/12 months).")
    expl_rowno = last_rowno + 2
    expl = ws.cell(row=expl_rowno, column=COL_0, value="\n".join(expl_text))
    expl.alignment = Alignment(horizontal='left', vertical='top',
                               wrap_text=True)
    merge_row(ws, expl_rowno, COL_0, last_colno)
    ws.row_dimensions[expl_rowno].height = 16*len(expl_text)
    return ws


def process_expense_buckets(wb, a2e):
    buckets = collect_expense_buckets(a2e)
    ws = create_buckets_worksheet(wb, buckets, a2e.months, a2e.nmonths)

class PNL(object):
    def __init__(self, fname, wb, ws):
        self.fname = fname
        self.wb = wb
        self.ws = ws
        self.out_fname = self._compute_out_fname() # does eager sanity assert

    def _compute_out_fname(self):
        tmp = self.fname.rsplit('.', 1)
        if len(tmp) == 2:
            assert tmp[1] in ("xls", "xlsx")
        return tmp[0] + "-mod.xlsx"

def main(args):
    budget_ws = None
    pnl = None
    for arg in args:
        wb = load_workbook(arg)
        wbl = len(wb.worksheets)
        if len(wb.worksheets) > 1:
            print(f"Warning: {arg} has {wbl} worksheets, doing first only")
        ws = wb.worksheets[0]
        a1 = ws.cell(1,1)
        if a1.value == "Profit and Loss":
            assert pnl is None
            pnl = PNL(arg, wb, ws)
            continue
        b1 = ws.cell(1,2)
        if b1.value == "Budget":
            assert budget_ws is None
            budget_ws = ws
            continue
        raise Err("Unrecognized spreadsheet")
    if not budget_ws:
        raise Err("Budget not loaded")
    if not pnl.ws:
        raise Err("P&L not loaded")
    a2e = Acct2Entries()
    read_entries(budget_ws, a2e)
    read_entries(pnl.ws, a2e, keep_affixes = True)
    wb = Workbook()
    addcells_pnl_vs_budget(wb.active, pnl.ws, a2e)
    set_column_widths(wb.active)
    process_expense_buckets(wb, a2e)
    wb.save(pnl.out_fname)
    print("Wrote", pnl.out_fname)

if __name__ == "__main__":
    main(sys.argv[1:])
