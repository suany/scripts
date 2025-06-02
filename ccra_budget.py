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

import sys
from openpyxl import load_workbook # pip3 install openpyxl

class Err(Exception):
    def __str__(self):
        return "\n" + self.args[0]

def verbose(*args, **kwargs):
    print(*args, **kwargs)

def read_budget(budget):
    budget_dict = dict()
    notes_dict = dict()
    first_time = True # to skip header
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
            continue
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

def main(args):
    budget = None
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
            pnl = ws
            continue
        b1 = ws.cell(1,2)
        if b1.value == "Budget":
            assert budget is None
            budget = ws
            continue
        raise Err("Unrecognized spreadsheet")
    if not budget:
        raise Err("Budget not loaded")
    if not pnl:
        raise Err("P&L not loaded")
    print("XXX budget", budget)
    budget_dict, notes_dict = read_budget(budget)
    print("XXX budget dict", budget_dict)
    print("XXX notes dict", notes_dict)
    print("XXX pnl", pnl)

if __name__ == "__main__":
    main(sys.argv[1:])
