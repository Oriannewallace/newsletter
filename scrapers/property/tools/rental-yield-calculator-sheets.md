# Rental Yield Calculator - Google Sheets Template

## Quick Setup

1. Open Google Sheets: https://sheets.new
2. Copy the structure below
3. Or import the CSV file: `rental-yield-template.csv`

---

## Sheet Structure

### SECTION 1: Single Property Calculator (Rows 1-25)

```
| Row | Column A              | Column B              | Column C (Formula)           |
|-----|----------------------|----------------------|------------------------------|
| 1   | RENTAL YIELD CALCULATOR |                      |                              |
| 2   | The Winning Formula   |                      |                              |
| 3   |                      |                      |                              |
| 4   | PROPERTY DETAILS     |                      |                              |
| 5   | Purchase Price       | R 1,500,000          |                              |
| 6   | Monthly Rent         | R 12,000             |                              |
| 7   |                      |                      |                              |
| 8   | MONTHLY EXPENSES     |                      |                              |
| 9   | Rates & Taxes        | R 1,500              |                              |
| 10  | Levies               | R 2,000              |                              |
| 11  | Insurance            | R 500                |                              |
| 12  | Maintenance Reserve  | R 600                |                              |
| 13  | Vacancy Allowance    | 5%                   |                              |
| 14  |                      |                      |                              |
| 15  | RESULTS              |                      |                              |
| 16  | Annual Rent          |                      | =B6*12                       |
| 17  | Annual Expenses      |                      | =(B9+B10+B11+B12)*12         |
| 18  | Vacancy Cost         |                      | =C16*B13                     |
| 19  | Net Annual Income    |                      | =C16-C17-C18                 |
| 20  | Monthly Cash Flow    |                      | =C19/12                      |
| 21  |                      |                      |                              |
| 22  | GROSS YIELD          |                      | =C16/B5                      |
| 23  | NET YIELD            |                      | =C19/B5                      |
| 24  |                      |                      |                              |
| 25  | Rating               |                      | =IF(C23>=0.08,"GOOD",IF(C23>=0.05,"OKAY","POOR")) |
```

### SECTION 2: Property Comparison Table (Rows 28+)

```
| Row | A           | B              | C            | D          | E         | F            | G         | H                    |
|-----|-------------|----------------|--------------|------------|-----------|--------------|-----------|----------------------|
| 28  | PROPERTY COMPARISON |         |              |            |           |              |           |                      |
| 29  | Name        | Purchase Price | Monthly Rent | Annual Rent| Expenses  | Net Income   | Gross %   | Net %                |
| 30  | Property 1  | 1500000        | 12000        | =C30*12    | 55200     | =D30-E30     | =D30/B30  | =F30/B30             |
| 31  | Property 2  | 2000000        | 15000        | =C31*12    | 72000     | =D31-E31     | =D31/B31  | =F31/B31             |
| 32  | Property 3  | 1200000        | 10000        | =C32*12    | 48000     | =D32-E32     | =D32/B32  | =F32/B32             |
| 33  | Property 4  |                |              |            |           |              |           |                      |
| 34  | Property 5  |                |              |            |           |              |           |                      |
```

---

## All Formulas (Copy-Paste Ready)

### Single Property Section

| Cell | Formula | Description |
|------|---------|-------------|
| C16 | `=B6*12` | Annual rent |
| C17 | `=(B9+B10+B11+B12)*12` | Annual expenses |
| C18 | `=C16*B13` | Vacancy cost |
| C19 | `=C16-C17-C18` | Net annual income |
| C20 | `=C19/12` | Monthly cash flow |
| C22 | `=C16/B5` | Gross yield (format as %) |
| C23 | `=C19/B5` | Net yield (format as %) |
| C25 | `=IF(C23>=0.08,"🟢 GOOD",IF(C23>=0.05,"🟡 OKAY","🔴 POOR"))` | Rating |

### Comparison Table (for each row)

| Column | Formula (Row 30 example) | Description |
|--------|--------------------------|-------------|
| D30 | `=C30*12` | Annual rent |
| F30 | `=D30-E30` | Net income (simple) |
| G30 | `=D30/B30` | Gross yield |
| H30 | `=F30/B30` | Net yield |

### Conditional Formatting for Net Yield

Apply to column H (Net Yield %):
- Green background if `>=8%`
- Yellow background if `>=5%` and `<8%`
- Red background if `<5%`

---

## Formatting Tips

### Number Formats
- Purchase Price, Rent: Currency (R #,##0)
- Yields: Percentage (0.0%)
- Vacancy: Percentage (0%)

### Cell Colors (Dark Theme Style)
- Background: #1a1a1a (dark gray)
- Text: #ffffff (white)
- Headers: #4CAF50 (green)
- Section titles: Bold, #4CAF50

### Column Widths
- A: 180px (labels)
- B: 150px (inputs)
- C: 150px (results)

---

## Advanced: Expense Estimator

Add this section to auto-estimate expenses based on property price:

```
| Row | A                    | B        | C (Formula)                |
|-----|---------------------|----------|----------------------------|
| 35  | EXPENSE ESTIMATOR   |          |                            |
| 36  | Rates (est. 1% of price/yr) |   | =B5*0.01/12                |
| 37  | Levies (est. R25/sqm) | sqm:   | =B37*25                    |
| 38  | Insurance (est. 0.2%/yr) |      | =B5*0.002/12               |
| 39  | Maintenance (5% of rent) |      | =B6*0.05                   |
```

---

## How to Use

### For Newsletter Readers:

1. **Make a copy**: File → Make a copy
2. **Enter your numbers** in the yellow cells (B5, B6, B9-B13)
3. **Read results** in the green cells
4. **Compare properties** by filling in the comparison table

### Sharing in Newsletter:

Link format: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/copy`

This creates a "Make a copy" prompt for readers.

---

## Example Properties (Cape Town)

| Area | Typical Price | Typical Rent | Expected Yield |
|------|---------------|--------------|----------------|
| Sea Point | R2.5M | R18,000 | 6-7% |
| Observatory | R1.5M | R12,000 | 7-8% |
| Woodstock | R1.8M | R14,000 | 7-8% |
| CBD | R1.2M | R10,000 | 8-9% |
| Bellville | R1.0M | R9,000 | 9-10% |

*These are rough estimates - always verify with current listings!*

---

Built by The Winning Formula
Data-driven property decisions
