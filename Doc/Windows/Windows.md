# Windows 疑难解惑

## Powershell脚本执行权限

当您遇到UnauthorizedAccess问题，请以管理员身份运行Powershell后执行以下命令，即可解决。

```powershell
Set-ExecutionPolicy Unrestricted
```

详细解释请参考
[MSDN](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.4)
或
[PowerShell执行策略](PowershellExecutionPolicy.md)
