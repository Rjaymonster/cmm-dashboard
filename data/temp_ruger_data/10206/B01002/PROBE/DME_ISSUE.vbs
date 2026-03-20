Set WshShell = CreateObject("WScript.Shell")
DMISVarName = "SERVER_PATH"
ERROR_CODE = ModusUtils.GetDMISVariableChar(DMISVarName,ServerVersion)
DMISVarName = "DME_PATH"
ERROR_CODE = ModusUtils.GetDMISVariableChar(DMISVarName,DME_To_Run)
WshShell.Run Chr(34) & ServerVersion & Chr(34) & Chr(34) & DME_To_Run & Chr(34), 0, True
Set WshShell = Nothing
