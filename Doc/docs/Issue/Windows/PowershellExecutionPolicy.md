## PowerShell 执行策略详解

PowerShell 执行策略规定了在系统上允许执行的脚本的级别。以下是 PowerShell 中的不同执行策略及其说明：

### 1. Restricted（受限制）

* **描述：** 仅允许 PowerShell 运行命令，不允许运行脚本。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 RemoteSigned（或其他适当的策略）
    Set-ExecutionPolicy RemoteSigned
    ```

### 2. AllSigned（已数字签名）

* **描述：** 只允许已数字签名的脚本运行。本地创建的脚本无需签名，但从远程下载的脚本必须经过数字签名。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 RemoteSigned（或其他适当的策略）
    Set-ExecutionPolicy RemoteSigned
    ```

### 3. RemoteSigned（远程已数字签名）

* **描述：** 允许本地创建的脚本运行，但从远程下载的脚本必须是数字签名的。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 Unrestricted（或其他适当的策略）
    Set-ExecutionPolicy Unrestricted
    ```

### 4. Unrestricted（不受限制）

* **描述：** 允许所有脚本运行，不考虑数字签名。这是最不限制的执行策略，但也是潜在的安全风险。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 Restricted（或其他适当的策略）
    Set-ExecutionPolicy Restricted
    ```

### 5. Bypass

* **描述：** 不执行任何检查，允许所有脚本运行。这是潜在的安全风险，仅在特殊情况下使用。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 Restricted（或其他适当的策略）
    Set-ExecutionPolicy Restricted
    ```

### 6. Undefined

* **描述：** 表示没有明确定义的执行策略。

* **命令：**

    ```powershell
    Get-ExecutionPolicy
    ```

* **修改策略：**

    ```powershell
    # 修改执行策略为 Restricted（或其他适当的策略）
    Set-ExecutionPolicy Restricted
    ```

> **注意：** 修改执行策略可能需要管理员权限。确保在适当的情况下执行修改，并了解每种执行策略的安全性和适用场景。