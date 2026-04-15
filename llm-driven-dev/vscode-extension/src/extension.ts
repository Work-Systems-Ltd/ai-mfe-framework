import * as vscode from "vscode";
import { scaffoldApp } from "./commands/scaffoldApp";
import { runDev } from "./commands/runDev";

export function activate(context: vscode.ExtensionContext): void {
  context.subscriptions.push(
    vscode.commands.registerCommand("mfe.scaffoldApp", scaffoldApp),
    vscode.commands.registerCommand("mfe.startDev", runDev),
    vscode.commands.registerCommand("mfe.openShell", () => {
      vscode.env.openExternal(vscode.Uri.parse("http://localhost:5173"));
    })
  );
}

export function deactivate(): void {
  // Cleanup if needed
}
