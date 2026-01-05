# Naming Template System - Quick Reference

## Overview
The naming template system allows you to define reusable patterns for naming PDF files with dynamic variables and date arithmetic.

---

## Template Syntax

### Basic Structure
Templates combine literal text with variables enclosed in curly braces: `{variable}`

**Example**: `Invoice_{date}_{name}.pdf`

---

## Available Variables

### Date & Time Variables

#### `{date}`
Current date using configured format

**Example**: 
- Template: `Document_{date}.pdf`
- Result: `Document_2024-01-05.pdf`

#### `{date+N}` or `{date-N}`
Current date plus/minus N days

**Examples**:
- `{date+7}` → Date 7 days from now
- `{date-30}` → Date 30 days ago
- Template: `Invoice_{date+7}.pdf` → `Invoice_2024-01-12.pdf`

**Use Cases**:
- Payment due dates: `{date+30}`
- Filing deadlines: `{date+7}`
- Historical records: `{date-90}`

#### `{timestamp}`
Full timestamp with date and time

**Example**:
- Template: `Scan_{timestamp}.pdf`
- Result: `Scan_2024-01-05_143022.pdf`

### User Input Variables

#### `{name}`
User-provided name (prompted during save)

**Example**:
- Template: `Contract_{name}_{date}.pdf`
- User enters: "Smith"
- Result: `Contract_Smith_2024-01-05.pdf`

#### `{filename}`
Original filename (without extension)

**Example**:
- Original: `scan001.pdf`
- Template: `Processed_{filename}_{date}.pdf`
- Result: `Processed_scan001_2024-01-05.pdf`

### Auto-Generated Variables

#### `{counter}`
Sequential number (auto-increments)

**Example**:
- Template: `Document_{counter}.pdf`
- Results: `Document_001.pdf`, `Document_002.pdf`, `Document_003.pdf`

#### `{counter:N}`
Counter with N digits (zero-padded)

**Examples**:
- `{counter:3}` → 001, 002, 003, ..., 999
- `{counter:5}` → 00001, 00002, 00003, ...

---

## Date Format Options

Configure date format in `config.json`:

```json
{
  "naming": {
    "date_format": "YYYY-MM-DD"
  }
}
```

### Supported Formats

| Format | Example | Description |
|--------|---------|-------------|
| `YYYY-MM-DD` | 2024-01-05 | ISO 8601 (recommended) |
| `DD-MM-YYYY` | 05-01-2024 | European format |
| `MM-DD-YYYY` | 01-05-2024 | US format |
| `YYYY_MM_DD` | 2024_01_05 | Underscore separator |
| `YYYYMMDD` | 20240105 | Compact format |
| `DD.MM.YYYY` | 05.01.2024 | Dot separator |
| `MMM DD YYYY` | Jan 05 2024 | Month abbreviation |
| `MMMM DD YYYY` | January 05 2024 | Full month name |

**Custom Formats**: Use standard date format tokens:
- `YYYY` - 4-digit year
- `YY` - 2-digit year
- `MM` - 2-digit month
- `MMM` - Short month name (Jan, Feb, etc.)
- `MMMM` - Full month name
- `DD` - 2-digit day

---

## Template Examples

### Basic Templates

#### Simple Date Prefix
```
Template: {date}_Document.pdf
Result: 2024-01-05_Document.pdf
Use: Daily logs, scans
```

#### Name and Date
```
Template: {name}_{date}.pdf
Result: ClientReport_2024-01-05.pdf
Use: Client deliverables
```

### Business Templates

#### Invoice with Due Date
```
Template: Invoice_{date}_{name}_Due_{date+30}.pdf
Result: Invoice_2024-01-05_AcmeCorp_Due_2024-02-04.pdf
Use: Invoicing with 30-day terms
```

#### Contract with Expiry
```
Template: Contract_{name}_{date}_Expires_{date+365}.pdf
Result: Contract_Smith_2024-01-05_Expires_2025-01-05.pdf
Use: Annual contracts
```

#### Receipt with Filing Date
```
Template: Receipt_{date+7}_{name}.pdf
Result: Receipt_2024-01-12_OfficeSupplies.pdf
Use: Receipts filed weekly
```

### Office Templates

#### Scanned Document with Timestamp
```
Template: Scan_{timestamp}_{name}.pdf
Result: Scan_2024-01-05_143022_EmployeeForm.pdf
Use: General scanning
```

#### Batch Processing
```
Template: Processed_{counter:3}_{date}.pdf
Result: Processed_001_2024-01-05.pdf, Processed_002_2024-01-05.pdf
Use: Bulk document processing
```

#### Archive Copy
```
Template: {filename}_Archive_{date}.pdf
Result: OriginalDoc_Archive_2024-01-05.pdf
Use: Creating archives of originals
```

### Legal Templates

#### Case Document
```
Template: Case_{name}_{date}_{counter:2}.pdf
Result: Case_Smith-v-Jones_2024-01-05_01.pdf
Use: Case file organization
```

#### Filing Deadline
```
Template: Filing_{name}_{date+14}.pdf
Result: Filing_PetitionToAppeal_2024-01-19.pdf
Use: Court filings with deadlines
```

### Accounting Templates

#### Monthly Statement
```
Template: Statement_{name}_{date}.pdf
Result: Statement_January2024_2024-01-05.pdf
Use: Monthly financial statements
```

#### Tax Document
```
Template: Tax_{date-365}_to_{date}_{name}.pdf
Result: Tax_2023-01-05_to_2024-01-05_AnnualReturn.pdf
Use: Tax year documents
```

---

## Configuration Examples

### Basic Configuration
```json
{
  "naming": {
    "templates": [
      "{date}_{name}",
      "{name}_{date}",
      "Document_{date}_{counter:3}"
    ],
    "date_format": "YYYY-MM-DD",
    "default_template": "{date}_{name}"
  }
}
```

### Advanced Configuration
```json
{
  "naming": {
    "templates": [
      "Invoice_{date}_{name}_Due_{date+30}",
      "Receipt_{date+7}_{name}",
      "Contract_{name}_{date}_Expires_{date+365}",
      "Scan_{timestamp}_{name}",
      "{filename}_Archive_{date}"
    ],
    "date_format": "YYYY-MM-DD",
    "default_template": "{date}_{name}",
    "prompt_for_name": true,
    "sanitize_filenames": true,
    "max_filename_length": 255
  }
}
```

---

## Best Practices

### 1. Use ISO Date Format (YYYY-MM-DD)
✅ Sorts correctly alphabetically  
✅ Universally understood  
✅ No ambiguity (unlike MM-DD vs DD-MM)

### 2. Start with Date for Chronological Sorting
```
Good: {date}_{name}.pdf
Bad:  {name}_{date}.pdf (unless name is more important)
```

### 3. Use Meaningful Variable Names
```
Good: Contract_{name}_{date}.pdf
Bad:  {name}.pdf (too generic)
```

### 4. Include Context in Literal Text
```
Good: Invoice_{date}_{name}.pdf
Bad:  {date}_{name}.pdf (what type of document?)
```

### 5. Avoid Special Characters
Templates automatically sanitize:
- `/` → `_`
- `:` → `-`
- `*`, `?`, `<`, `>`, `|`, `"` → removed

### 6. Keep Filenames Reasonable Length
- Maximum: 255 characters (enforced)
- Recommended: < 100 characters for readability

### 7. Use Counters for Batches
```
Template: Batch_{date}_{counter:3}.pdf
Result: Batch_2024-01-05_001.pdf, Batch_2024-01-05_002.pdf, ...
```

### 8. Plan for Future Dates
```
Due dates: {date+N}
Expiry dates: {date+N}
Filing dates: {date+N}
```

---

## Common Patterns

### Pattern: Daily Workflow
```
Template: {date}_{name}
When: Every day you process similar documents
Example: 2024-01-05_DailyReport.pdf
```

### Pattern: Client Projects
```
Template: {name}_Project_{date}_{counter:2}
When: Multiple documents per client
Example: AcmeCorp_Project_2024-01-05_01.pdf
```

### Pattern: Payment Tracking
```
Template: {name}_Invoice_{date}_Due_{date+30}
When: Invoices with payment terms
Example: ClientA_Invoice_2024-01-05_Due_2024-02-04.pdf
```

### Pattern: Compliance/Deadlines
```
Template: {name}_Filing_{date+14}
When: Documents with regulatory deadlines
Example: TaxReturn_Filing_2024-01-19.pdf
```

### Pattern: Archive/Backup
```
Template: {filename}_Backup_{timestamp}
When: Creating versioned backups
Example: ImportantDoc_Backup_2024-01-05_143022.pdf
```

---

## Troubleshooting

### Problem: "Invalid template syntax"
**Cause**: Malformed variable or missing closing brace  
**Solution**: Check all `{variables}` are properly closed

### Problem: "Name prompt not appearing"
**Cause**: `prompt_for_name: false` in config  
**Solution**: Set `"prompt_for_name": true` in config.json

### Problem: "Date arithmetic not working"
**Cause**: Wrong syntax for date offset  
**Solution**: Use `{date+7}` not `{date +7}` (no spaces)

### Problem: "Filename too long"
**Cause**: Template generates name > 255 characters  
**Solution**: Shorten literal text or use abbreviations

### Problem: "Special characters in filename"
**Cause**: User input contains invalid characters  
**Solution**: Auto-sanitization enabled by default; check `sanitize_filenames: true`

---

## Template Testing

Before using templates in production, test them:

1. **Preview**: Use the preview feature to see generated names
2. **Test Data**: Try with various inputs (long names, edge dates, etc.)
3. **Verify Sorting**: Check if files sort correctly in file explorer
4. **Check Compatibility**: Test on target operating system(s)

---

## Migration Guide

### From Manual Naming to Templates

**Before**: Manually typing `Invoice_2024-01-05_ClientName.pdf`  
**After**: Template `Invoice_{date}_{name}.pdf` + prompt for "ClientName"

**Benefits**:
- Consistency across all files
- No typos or format errors
- Faster processing
- Easy to update format organization-wide

---

## API Reference (For Developers)

### Template Parser
```python
from naming import TemplateParser

parser = TemplateParser()
template = "Invoice_{date+7}_{name}.pdf"
variables = {"name": "AcmeCorp"}

result = parser.parse(template, variables)
# Result: "Invoice_2024-01-12_AcmeCorp.pdf"
```

### Custom Variables
```python
parser.add_variable("project_id", "PRJ-001")
template = "{project_id}_{date}_{name}.pdf"
# Result: "PRJ-001_2024-01-05_Report.pdf"
```

---

## Quick Reference Card

| Variable | Description | Example |
|----------|-------------|---------|
| `{date}` | Current date | 2024-01-05 |
| `{date+7}` | Date + 7 days | 2024-01-12 |
| `{date-30}` | Date - 30 days | 2023-12-06 |
| `{timestamp}` | Date + Time | 2024-01-05_143022 |
| `{name}` | User input | ClientName |
| `{filename}` | Original name | document |
| `{counter}` | Auto number | 1, 2, 3... |
| `{counter:3}` | Padded number | 001, 002, 003... |

**Default Date Format**: YYYY-MM-DD  
**Max Length**: 255 characters  
**Auto-Sanitize**: Yes

---

For more information, see [TODO.md](TODO.md) section 5 and [USER_STORIES.md](USER_STORIES.md).
