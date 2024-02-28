// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	
	vscode.workspace.onDidSaveTextDocument(function (document) {
		if (!document.fileName.endsWith('.cnf') && !document.fileName.endsWith('.wcnf')) {
			return;
		}
		let config = vscode.workspace.getConfiguration('dimacs');
		let enableAutoFormat = config.get('enableAutoFormat');

		if (!enableAutoFormat) {
			return;
		}

		const { exec } = require('child_process');
		const path = require('path');

		const filePath = document.fileName;
		const pythonScript = path.join(__dirname, 'dimacs_formatter.py');


		exec(`python3 ${pythonScript} "${filePath}"`, (error, stdout, stderr) => {
			if (error) {
				console.error(`exec error: ${error}`);
				return;
			}
			console.log(`Output: ${stdout}`);
		});
	});
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
