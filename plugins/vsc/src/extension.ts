// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as request from 'request-promise-native';
import { isDeepStrictEqual } from 'util';

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
		
		let diagnosticCollection = vscode.languages.createDiagnosticCollection('repltalk');
			let disposable = vscode.commands.registerCommand('extension.repltalk', () => {
			request('http://localhost:2096/start', {'json': true})
				.then((body:any) => {
					loadDiagnostics(diagnosticCollection, body);
				})
				.catch(err => 
					vscode.window.showInformationMessage("There was an error connecting to Haskell server!"));

			var onSave = vscode.workspace.onDidSaveTextDocument((e: vscode.TextDocument) => {
				vscode.window.setStatusBarMessage("Reloading...");
				request({'uri': 'http://localhost:2096/command',
					'json': true,
					'method': 'POST',
					'body': {'command': ':reload'},
					'headers': {'content-type': 'application/json'}})
				.then((body:ReplServerResponse) => {
					loadDiagnostics(diagnosticCollection, body);					
				})
				.catch(err => 
					vscode.window.showInformationMessage("There was an error connecting to Haskell server!" + err.toString()));
				});
			context.subscriptions.push(onSave);
			context.subscriptions.push(diagnosticCollection);
		});
}

function loadDiagnostics(dc: vscode.DiagnosticCollection, output: ReplServerResponse) {	
	if ((<ReplServerResponseError>output).error) {
		let o = (<ReplServerResponseError>output);
		vscode.window.showInformationMessage("There was an error:" + o.error);		
	} else {
		let o = (<ReplServerResponseReport>output);		
		let diagnosticMap: Map<string, vscode.Diagnostic[]> = new Map();
		let msg = "Errors: "+ o.output.errors.length.toString() + "; Warnings: " + o.output.warnings.length.toString();
		vscode.window.setStatusBarMessage(msg);
		if (o.output.errors.length) {
			vscode.window.showErrorMessage(msg);
		}
		
		if (o.output.warnings.length ) {
			vscode.window.showWarningMessage(msg);
		} 
			
		o.output.errors.forEach(issue => {
			addDiagnostic(diagnosticMap, issue, vscode.DiagnosticSeverity.Error);
		});
		o.output.warnings.forEach(issue => {
			addDiagnostic(diagnosticMap, issue, vscode.DiagnosticSeverity.Warning);			
		});

		dc.clear();
		diagnosticMap.forEach((diags, file) => {							
			dc.set(vscode.Uri.parse(file), diags);
		});
						
	}
}

function addDiagnostic(diagnosticMap:Map<string, vscode.Diagnostic[]>,issue:Issue, s:vscode.DiagnosticSeverity) {
	let filename = issue.file_name;
	let diagnostics = diagnosticMap.get(filename);
	if (!diagnostics) { diagnostics = []; }
	diagnostics.push(makeDiagnosticItem(issue, s));
	diagnosticMap.set(filename, diagnostics);				
}

function makeDiagnosticItem(issue: Issue, s:vscode.DiagnosticSeverity):vscode.Diagnostic {	
	let line = parseInt(issue.line);
	let column = parseInt(issue.column);	
	let range = new vscode.Range(line-1, column, line-1, column);		
	return new vscode.Diagnostic(range, issue.text, s);
}

// this method is called when your extension is deactivated
export function deactivate() {
	request('http://localhost:2096/stop');	
}