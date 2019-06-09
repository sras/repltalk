// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import {exec} from 'child_process';
import * as request from 'request-promise-native';

interface ReplServerResponseError  {error: String;} 

interface ReplServerResponseReport {
	output : {
		errors:[Issue];
		warnings: [Issue]; 
	};
}

interface Issue {
	file_name: string;
	line: string;
	column: string;
	text: string;
}

type ReplServerResponse = ReplServerResponseReport | ReplServerResponseError;

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
		let diagnosticCollection: vscode.DiagnosticCollection;
		diagnosticCollection = vscode.languages.createDiagnosticCollection('hs');
		request('http://localhost:2096/start', {'json': true})
			.then((body:any) => {
				loadDiagnostics(diagnosticCollection, body);
			})
			.catch(err => 
				vscode.window.showInformationMessage("There was an error connecting to Haskell server!"));

		var onSave = vscode.workspace.onDidSaveTextDocument((e: vscode.TextDocument) => {
			request({'uri': 'http://localhost:2096/command',
				 'json': true,
				 'method': 'POST',
				 'body': {'command': ':reload'},
				 'headers': {'content-type': 'application/json'}})
			.then((body:any) => {
				let diagnosticMap = loadDiagnostics(diagnosticCollection, body);
				if (diagnosticMap !== null) {
					diagnosticCollection.clear();
					diagnosticMap.forEach((diags, file) => {
						vscode.window.showInformationMessage(file);
						diagnosticCollection.set(vscode.Uri.parse(file), diags);
					});
				}
			})
			.catch(err => 
				vscode.window.showInformationMessage("There was an error connecting to Haskell server!" + err.toString()));
			});
	context.subscriptions.push(onSave);
	context.subscriptions.push(diagnosticCollection);
}

function loadDiagnostics(dc: vscode.DiagnosticCollection, output: ReplServerResponse):Map<string,vscode.Diagnostic[]>|null {	
	if ((<ReplServerResponseError>output).error) {
		let o = (<ReplServerResponseError>output);
		vscode.window.showInformationMessage("There was an error:" + o.error);
		return null;
	} else {
		let o = (<ReplServerResponseReport>output);		
		let diagnosticMap: Map<string, vscode.Diagnostic[]> = new Map();
		o.output.errors.forEach(issue => {
			addDiagnostic(diagnosticMap, issue, true);
		});
		o.output.warnings.forEach(issue => {
			addDiagnostic(diagnosticMap, issue, false);			
		});
		return diagnosticMap;				
	}
}

function addDiagnostic(diagnosticMap:Map<string, vscode.Diagnostic[]>,issue:Issue, isError: boolean) {
	let filename = issue.file_name;
	let diagnostics = diagnosticMap.get(filename);
	if (!diagnostics) { diagnostics = []; }
	diagnostics.push(makeDiagnosticItem(issue, true));
	diagnosticMap.set(filename, diagnostics);				
}

function makeDiagnosticItem(issue: Issue, isError: boolean):vscode.Diagnostic {	
	let line = parseInt(issue.line);
	let column = parseInt(issue.column);	
	let range = new vscode.Range(line-1, column, line-1, column);		
	let s:number;
	if (isError) {
		s = 5;
	} else {
		s = 0;
	}
	return new vscode.Diagnostic(range, issue.text, s);
}

// this method is called when your extension is deactivated
export function deactivate() {}
