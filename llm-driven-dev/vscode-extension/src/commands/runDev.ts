import * as vscode from "vscode";

export async function runDev(): Promise<void> {
  const options = ["All services", "Select specific app"];
  const choice = await vscode.window.showQuickPick(options, {
    placeHolder: "What do you want to start?",
  });

  if (!choice) return;

  const terminal = vscode.window.createTerminal("MFE Dev");
  terminal.show();

  if (choice === "All services") {
    terminal.sendText("mfe dev");
  } else {
    const appName = await vscode.window.showInputBox({
      prompt: "Enter the app name to run",
      placeHolder: "example1",
    });
    if (appName) {
      terminal.sendText(`mfe dev ${appName}`);
    }
  }
}
