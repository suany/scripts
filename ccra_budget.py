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
from copy import copy
from openpyxl import load_workbook, Workbook # pip3 install openpyxl
from openpyxl.utils import get_column_letter # XXX unused

SIMPLE_APPEND_MODE = False # XXX

class Err(Exception):
    def __str__(self):
        return "\n" + self.args[0]

def verbose(*args, **kwargs):
    print(*args, **kwargs)

def account_number(s):
    if len(s) < 5:
        return None
    if s[4] != ' ':
        return None
    try:
        return int(s[:4])
    except:
        return None

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

# Main sections
income_range = (4000, 4999)   # lb, ub
expenses_range = (5000, 8999) # lb, ub
other_income = (4850, 4860) # Donations, Prior Period Clean Up
other_expenses = (5900,) # Asset Deprecation

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
            if acctno in other_expenses:
                self.other_expenses.append(acct)
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
    def get_parent(self, acct):
        pass # XXX
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

def add_row(ws, rowno, acct,
            actual = None, budget = None, notes = None, pct = None):
    ws.cell(row = rowno, column = 1, value = acct)       # A
    ws.cell(row = rowno, column = 2, value = actual)     # B
    if budget: # Skip budget and % if 0
        ws.cell(row = rowno, column = 3, value = budget) # C
        if pct is None:
            pct = f"=B{rowno}/C{rowno}"
        ws.cell(row = rowno, column = 4, value = pct)    # D
    ws.cell(row = rowno, column = 6, value = notes)      # F

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

# sumrows is an out parameter
def addcells_section(ws, rowno, secname, accts, a2e, sumrows):
    add_row(ws, rowno, secname)
    rowno += 1
    total = ActualBudget()
    for acct in accts:
        entries = a2e.numbered[acct]
        actual = entries.get("Total", None)
        budget = entries.get("Budget", None)
        notes = entries.get("Notes", None)
        add_row(ws, rowno, acct, actual, budget, notes)
        rowno += 1
        if subaccounts.is_parent(acct):
            print("XXX subaccount", acct)
        if actual is not None:
            total.actual += actual
        if total.budget is not None:
            total.budget += budget
    totalname = "Total for " + secname
    if accts:
        add_row(ws, rowno, totalname, total.actual, total.budget)
        sumrows.add(rowno)
        rowno += 1
    # Sanity check against a2e entry
    sanity_check_numbers(a2e, totalname, total)
    return rowno, total

def addcells_pnl_vs_budget(ws, pnlws, a2e):
    rowno = 1
    mergerows = set()
    sumrows = set() # embolden, add overline
    ###########
    # Prefix Rows
    for row in a2e.prefix_rows:
        for colno, val in enumerate(row, start = 1):
            ws.cell(row = rowno, column = colno, value = val)
            if val:
                mergerows.add(rowno)
        rowno += 1
    ###########
    # Headers
    add_row(ws, rowno, a2e.acct_header,
            "Actual", "Budget", "Notes", pct = "Pct")
    check_header_presence(("Total", "Budget", "Notes"), a2e.headers)
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
                        ws, rowno, "Income", secs.income, a2e, sumrows)
    rowno, expenses = addcells_section(
                        ws, rowno, "Expenses", secs.expenses, a2e, sumrows)
    # Net Operating Income
    netop = income - expenses
    nopi = "Net Operating Income"
    add_row(ws, rowno, nopi, netop.actual, netop.budget)
    sumrows.add(rowno)
    rowno += 1
    sanity_check_numbers(a2e, nopi, netop)
    # Other Income and Expenses
    rowno, oincome = addcells_section(
                        ws, rowno, "Other Income", secs.other_income,
                        a2e, sumrows)
    rowno, oexpenses = addcells_section(
                        ws, rowno, "Other Expenses", secs.other_expenses,
                        a2e, sumrows)
    # Net Other Income
    netoth = oincome - oexpenses
    noti = "Net Other Income"
    add_row(ws, rowno, noti, netoth.actual, netoth.budget)
    sumrows.add(rowno)
    rowno += 1
    sanity_check_numbers(a2e, noti, netoth)
    # Net Income
    netinc = netop + netoth
    ni = "Net Income"
    add_row(ws, rowno, ni, netinc.actual, netinc.budget)
    sumrows.add(rowno)
    rowno += 1
    sanity_check_numbers(a2e, ni, netinc)
    ###########
    # Suffix Rows
    for row in a2e.suffix_rows:
        for colno, val in enumerate(row, start = 1):
            ws.cell(row = rowno, column = colno, value = val)
            if val:
                mergerows.add(rowno)
        rowno += 1
    ###########
    print("XXX mergerows", mergerows) # TODO: merge
    print("XXX sumrows", sumrows) # TODO: bold, overline

def read_budget_and_notes(budget):
    budget_dict = dict()
    notes_dict = dict()
    first_time = True # to check header
    for row in budget.rows:
        assert len(row) >= 3
        acct = row[0].value
        amt = row[1].value
        notes = row[2].value
        if first_time:
            assert acct == "Distribution account"
            assert amt == "Budget"
            assert notes == "Notes"
            first_time = False
            # Insert into table anyways
        if not acct:
            verbose("Empty first cell, stopping at", row)
            break
        if acct in budget_dict:
            print("Warning: repeated budget key(", acct, ") at", row)
        if acct in notes_dict:
            print("Warning: repeated notes key(", acct, ") at", row)
        if amt:
            budget_dict[acct] = amt
        if notes:
            notes_dict[acct] = notes
    return budget_dict, notes_dict

def copy_styles(src, dst,
                font = None,
                border = None,
                fill = None,
                number_format = None,
                protection = None,
                alignment = None):
    if src.has_style:
        dst.font = (copy(src.font)
                    if font is None else font)
        dst.border = (copy(src.border)
                      if border is None else border)
        dst.fill = (copy(src.fill)
                    if fill is None else fill)
        dst.number_format = (copy(src.number_format)
                             if number_format is None else number_format)
        dst.protection = (copy(src.protection)
                          if protection is None else protection)
        dst.alignment = (copy(src.alignment)
                         if alignment is None else alignment)

def append_budget_and_notes(pnlws, budget_dict, notes_dict):
    for row in pnlws.rows:
        assert len(row) <= 2
        acct = row[0].value
        rowno = row[0].row
        budget = budget_dict.get(acct)
        notes = notes_dict.get(acct)
        if budget:
            c3 = pnlws.cell(row=rowno, column=3, value=budget)
            copy_styles(row[1], c3)
            if budget == "Budget": # Header row
                c4 = pnlws.cell(row=rowno, column=4, value="Pct")
                copy_styles(row[1], c4)
            else:
                c4 = pnlws.cell(row=rowno, column=4,
                                value=f"=B{rowno}/C{rowno}")
                copy_styles(row[1], c4, number_format = "##0.0%")
        if notes:
            c6 = pnlws.cell(row=rowno, column=6, value=notes)
            copy_styles(row[0], c6)

def expand_merge(pnlws, mcr):
    if mcr.min_row == mcr.max_row and mcr.min_col == 1 and mcr.max_col == 2:
        pnlws.unmerge_cells(
            start_row=mcr.min_row,
            start_column=mcr.min_col,
            end_row=mcr.max_row,
            end_column=mcr.max_col)
        pnlws.merge_cells(
            start_row=mcr.min_row,
            start_column=mcr.min_col,
            end_row=mcr.max_row,
            end_column=mcr.max_col + 4)
    else:
        print("Warning: expand merge skipping", mcr)

def reformat_updated_pnl(pnlws):
    # Set column widths - these work well for 2025
    pnlws.column_dimensions['A'].width = 31 # =310px
    pnlws.column_dimensions['B'].width = 9
    pnlws.column_dimensions['C'].width = 9
    pnlws.column_dimensions['D'].width = 7
    pnlws.column_dimensions['E'].width = 1
    pnlws.column_dimensions['F'].width = 26
    # TODO: set row heights for multilines?
    # Expand merged cells
    for mcr in list(pnlws.merged_cells.ranges):
        expand_merge(pnlws, mcr)

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
        if SIMPLE_APPEND_MODE:
            return tmp[0] + "-mod1.xlsx"
        return tmp[0] + "-mod3.xlsx"

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
    if SIMPLE_APPEND_MODE:
        budget_dict, notes_dict = read_budget_and_notes(budget_ws)
        append_budget_and_notes(pnl.ws, budget_dict, notes_dict)
        reformat_updated_pnl(pnl.ws)
        pnl.wb.save(pnl.out_fname)
    else:
        a2e = Acct2Entries()
        read_entries(budget_ws, a2e)
        read_entries(pnl.ws, a2e, keep_affixes = True)
        wb = Workbook()
        addcells_pnl_vs_budget(wb.active, pnl.ws, a2e)
        wb.save(pnl.out_fname)

if __name__ == "__main__":
    main(sys.argv[1:])
