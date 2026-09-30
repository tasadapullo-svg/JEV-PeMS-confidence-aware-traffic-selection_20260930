import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const payloadPath = process.argv[2];
if (!payloadPath) throw new Error("Payload path required");
const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
const workbook = Workbook.create();
const font = "Arial";
const dark = "#1F4E78";

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

for (const [name, recordsValue] of Object.entries(payload.sheets)) {
  const records = Array.isArray(recordsValue) ? recordsValue : [];
  const sheet = workbook.worksheets.add(name.slice(0, 31));
  sheet.showGridLines = false;
  const headers = records.length ? [...new Set(records.flatMap(record => Object.keys(record)))] : ["Status"];
  sheet.getRange("A2").values = [[name.replaceAll("_", " ")]];
  sheet.getRange("A2").format.font = { name: font, size: 14, bold: true, color: "#1F2937" };
  sheet.getRangeByIndexes(3, 0, 1, headers.length).values = [headers];
  sheet.getRangeByIndexes(3, 0, 1, headers.length).format = {
    fill: dark, font: { name: font, size: 10, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center", verticalAlignment: "center", wrapText: true,
  };
  if (records.length) {
    const matrix = records.map(record => headers.map(header => scalar(record[header])));
    const body = sheet.getRangeByIndexes(4, 0, matrix.length, headers.length);
    body.values = matrix;
    body.format.font = { name: font, size: 10, color: "#1F2937" };
    body.format.verticalAlignment = "center";
    if (matrix.length > 20) sheet.freezePanes.freezeRows(4);
  } else {
    sheet.getRange("A5").values = [["No records"]];
  }
  const used = sheet.getUsedRange();
  used.format.autofitColumns(); used.format.autofitRows();
  for (let col = 0; col < headers.length; col++) {
    const range = sheet.getRangeByIndexes(0, col, Math.max(records.length + 5, 5), 1);
    const cap = ["definition", "value", "field"].includes(headers[col]) ? 58 : 34;
    if (range.format.columnWidth > cap) range.format.columnWidth = cap;
    if (["definition", "value"].includes(headers[col])) range.format.wrapText = true;
  }
  used.format.autofitRows();
  sheet.tabColor = name === "README" ? dark : undefined;
}

workbook.recalculate();
const summary = await workbook.inspect({ kind: "workbook,sheet,table", maxChars: 9000, tableMaxRows: 8, tableMaxCols: 12, tableMaxCellChars: 100 });
await fs.writeFile(payload.output_xlsx + ".inspect.ndjson", summary.ndjson, "utf8");
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
await fs.writeFile(payload.output_xlsx + ".formula_errors.ndjson", errors.ndjson, "utf8");
await fs.mkdir(payload.preview_dir, { recursive: true });
for (const [name, recordsValue] of Object.entries(payload.sheets)) {
  const records = Array.isArray(recordsValue) ? recordsValue : [];
  const headers = records.length ? [...new Set(records.flatMap(record => Object.keys(record)))] : ["Status"];
  const lastRow = records.length ? Math.min(records.length, 50) + 4 : 5;
  const preview = await workbook.render({ sheetName: name.slice(0, 31), range: `A1:${columnName(headers.length)}${lastRow}`, scale: 1, format: "png" });
  await fs.writeFile(`${payload.preview_dir}/${name}.png`, new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(payload.output_xlsx);
console.log(JSON.stringify({ output: payload.output_xlsx, sheets: Object.keys(payload.sheets), status: "PASS" }));
