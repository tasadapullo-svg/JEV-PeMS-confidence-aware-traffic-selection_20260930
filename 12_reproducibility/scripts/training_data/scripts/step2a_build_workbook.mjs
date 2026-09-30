import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const payloadPath = process.argv[2];
if (!payloadPath) throw new Error("Payload path required");
const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
const workbook = Workbook.create();
const font = "Arial";
const dark = "#1F4E78";
const light = "#D9EAF7";

function scalar(value) {
  if (value === null || value === undefined) return "";
  if (typeof value === "object") return JSON.stringify(value);
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) return `'${value}`;
  return value;
}

function columnName(columnCount) {
  let n = columnCount;
  let name = "";
  while (n > 0) {
    n -= 1;
    name = String.fromCharCode(65 + (n % 26)) + name;
    n = Math.floor(n / 26);
  }
  return name || "A";
}

const configRows = Array.isArray(payload.sheets.CONFIG) ? payload.sheets.CONFIG : [];
const reportMode = String(configRows.find(row => String(row.field).toLowerCase() === "mode")?.value || "").toLowerCase();

function reportRows(name, records) {
  const rows = Array.isArray(records) ? records : [];
  if (reportMode !== "production") return rows;
  return rows.map(row => {
    if (name === "README" && row.field === "Warning" && /smoke/i.test(String(row.value))) {
      return { ...row, value: "Production results; Test split held out and not loaded" };
    }
    if (name === "ISSUES" && /smoke statistics/i.test(String(row.issue))) {
      return {
        ...row,
        severity: "INFO",
        issue: "Test split held out and not loaded",
        action: "Do not use Test for design or threshold selection",
      };
    }
    return row;
  });
}

for (const [name, records] of Object.entries(payload.sheets)) {
  const sheet = workbook.worksheets.add(name.slice(0, 31));
  sheet.showGridLines = false;
  const rows = reportRows(name, records);
  const headers = rows.length ? [...new Set(rows.flatMap(r => Object.keys(r)))] : ["Status"];
  sheet.getRange("A2").values = [[name.replaceAll("_", " ")]];
  sheet.getRange("A2").format.font = { name: font, size: 14, bold: true, color: "#1F2937" };
  sheet.getRangeByIndexes(3, 0, 1, headers.length).values = [headers];
  const headerRange = sheet.getRangeByIndexes(3, 0, 1, headers.length);
  headerRange.format = { fill: dark, font: { name: font, size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
  if (rows.length) {
    const matrix = rows.map(row => headers.map(h => scalar(row[h])));
    const body = sheet.getRangeByIndexes(4, 0, matrix.length, headers.length);
    body.values = matrix;
    body.format.font = { name: font, size: 10, color: "#1F2937" };
    body.format.verticalAlignment = "center";
    if (matrix.length > 20) sheet.freezePanes.freezeRows(4);
  } else {
    sheet.getRange("A5").values = [["No records"]];
  }
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
  const maxCols = Math.max(headers.length, 1);
  for (let c = 0; c < maxCols; c++) {
    const col = sheet.getRangeByIndexes(0, c, Math.max(rows.length + 5, 5), 1);
    const wideText = ["path", "value", "issue", "action", "sha256", "timestamp", "timestamp_utc", "missing_candidate_ids"].includes(headers[c]);
    const cap = wideText ? 56 : 36;
    if (col.format.columnWidth > cap) col.format.columnWidth = cap;
    if (wideText) col.format.wrapText = true;
  }
  used.format.autofitRows();
  sheet.getRangeByIndexes(3, 0, Math.max(rows.length + 1, 1), headers.length).format.borders = { preset: "outside", style: "thin", color: "#B8C4CE" };
  sheet.tabColor = name === "README" ? dark : (name === "CONFIG" ? light : undefined);
}

workbook.recalculate();
const summary = await workbook.inspect({ kind: "workbook,sheet,table", maxChars: 9000, tableMaxRows: 8, tableMaxCols: 12, tableMaxCellChars: 100 });
await fs.writeFile(payload.output_xlsx + ".inspect.ndjson", summary.ndjson, "utf8");
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
await fs.writeFile(payload.output_xlsx + ".formula_errors.ndjson", errors.ndjson, "utf8");
await fs.mkdir(payload.preview_dir, { recursive: true });
for (const name of Object.keys(payload.sheets)) {
  const rows = Array.isArray(payload.sheets[name]) ? payload.sheets[name] : [];
  const headers = rows.length ? [...new Set(rows.flatMap(r => Object.keys(r)))] : ["Status"];
  const previewLastRow = rows.length ? Math.min(rows.length, 50) + 4 : 5;
  const previewRange = `A1:${columnName(headers.length)}${previewLastRow}`;
  const preview = await workbook.render({ sheetName: name.slice(0, 31), range: previewRange, scale: 1, format: "png" });
  await fs.writeFile(`${payload.preview_dir}/${name}.png`, new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(payload.output_xlsx);
console.log(JSON.stringify({ output: payload.output_xlsx, sheets: Object.keys(payload.sheets), status: "PASS" }));
