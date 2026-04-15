import * as vscode from "vscode";

export async function scaffoldApp(): Promise<void> {
  const name = await vscode.window.showInputBox({
    prompt: "Enter the app name (e.g., inventory)",
    placeHolder: "my-app",
    validateInput: (value) => {
      if (!value) return "App name is required";
      if (!/^[a-z][a-z0-9-]*$/.test(value))
        return "App name must be lowercase alphanumeric with dashes";
      return null;
    },
  });

  if (!name) return;

  const displayName = await vscode.window.showInputBox({
    prompt: "Enter display name (or leave empty for auto)",
    placeHolder: name.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
  });

  const terminal = vscode.window.createTerminal("MFE CLI");
  const cmd = displayName
    ? `mfe new-app ${name} --display-name "${displayName}"`
    : `mfe new-app ${name}`;

  terminal.show();
  terminal.sendText(cmd);
}
