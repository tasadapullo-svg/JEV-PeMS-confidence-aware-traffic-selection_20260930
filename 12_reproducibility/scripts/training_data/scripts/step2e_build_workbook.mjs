import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const payload = JSON.parse(await fs.readFile(process.argv[2], "utf8"));
const workbook = Workbook.create();
const dark = "#1F4E78";
function scalar(v) { if (v === null || v === undefined) return ""; if (typeof v === "object") return JSON.stringify(v); return v; }
function colName(n) { let s=""; while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);} return s||"A"; }
for (const [name, value] of Object.entries(payload.sheets)) {
  const records = Array.isArray(value) ? value : [];
  const sheet = workbook.worksheets.add(name.slice(0,31)); sheet.showGridLines=false;
  const headers = records.length ? [...new Set(records.flatMap(r=>Object.keys(r)))] : ["Status"];
  sheet.getRange("A2").values=[[name.replaceAll("_"," ")]]; sheet.getRange("A2").format.font={name:"Arial",size:14,bold:true,color:"#1F2937"};
  sheet.getRangeByIndexes(3,0,1,headers.length).values=[headers]; sheet.getRangeByIndexes(3,0,1,headers.length).format={fill:dark,font:{name:"Arial",size:10,bold:true,color:"#FFFFFF"},horizontalAlignment:"center",verticalAlignment:"center",wrapText:true};
  if(records.length){const matrix=records.map(r=>headers.map(h=>scalar(r[h])));sheet.getRangeByIndexes(4,0,matrix.length,headers.length).values=matrix;sheet.getRangeByIndexes(4,0,matrix.length,headers.length).format.font={name:"Arial",size:10,color:"#1F2937"};} else sheet.getRange("A5").values=[["No records"]];
  sheet.freezePanes.freezeRows(4); const used=sheet.getUsedRange(); used.format.autofitColumns(); used.format.autofitRows();
  for(let c=0;c<headers.length;c++){const range=sheet.getRangeByIndexes(0,c,Math.max(records.length+5,5),1);const cap=headers[c]==="value"?60:34;if(range.format.columnWidth>cap)range.format.columnWidth=cap;if(headers[c]==="value")range.format.wrapText=true;}
  used.format.autofitRows();
  if(headers.includes("value") && records.length) sheet.getRangeByIndexes(4,0,records.length,headers.length).format.rowHeight=48;
  if(name==="README") sheet.tabColor=dark;
}
workbook.recalculate();
const inspect=await workbook.inspect({kind:"workbook,sheet,table",maxChars:12000,tableMaxRows:8,tableMaxCols:14,tableMaxCellChars:100}); await fs.writeFile(payload.output_xlsx+".inspect.ndjson",inspect.ndjson,"utf8");
const errors=await workbook.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",options:{useRegex:true,maxResults:300},summary:"final formula error scan"}); await fs.writeFile(payload.output_xlsx+".formula_errors.ndjson",errors.ndjson,"utf8");
await fs.mkdir(payload.preview_dir,{recursive:true});
for(const [name,value] of Object.entries(payload.sheets)){const records=Array.isArray(value)?value:[];const headers=records.length?[...new Set(records.flatMap(r=>Object.keys(r)))]:["Status"];const last=Math.min(records.length,40)+4;const png=await workbook.render({sheetName:name.slice(0,31),range:`A1:${colName(headers.length)}${Math.max(last,5)}`,scale:1,format:"png"});await fs.writeFile(`${payload.preview_dir}/${name}.png`,new Uint8Array(await png.arrayBuffer()));}
const output=await SpreadsheetFile.exportXlsx(workbook); await output.save(payload.output_xlsx); console.log(JSON.stringify({status:"PASS",output:payload.output_xlsx,sheets:Object.keys(payload.sheets)}));
