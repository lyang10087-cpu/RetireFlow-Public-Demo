# RetireFlow · 公开展示版

RetireFlow 用三组虚构退休材料展示档案比对、V2 预审、人工确认与 HR 留痕。`PUBLIC_DEMO` 是此独立应用的唯一模式。材料识别与工具选择为预设演示，真实大模型推理和模型端到端写入待验收。

## 本机运行

需要 Python 3.11。在本目录运行以下命令，打开 [本机预览](http://127.0.0.1:8502)。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

在 Linux 或 macOS 使用 `.venv/bin/python`。离线回归保留在本地验收工作区。

## 交互与证据

- A 展示三字段一致。脱敏快照为「待人工复核」，固定场景预期为「通过预审」。
- B 展示工作时间材料值 `1991-07`、基准 `1990-07` 以及保留原值的拟写入预览。
- C 展示缺 1 类材料和重建的 HR 历史示例。示例序号为虚构编号，页面只显示操作和状态变化。
- 「确认预览」只在本次浏览器会话生效。切换场景、重载当前场景或刷新页面会清除确认。

本地 DEV 版本曾验证飞书只读查询与 HR 留痕。公开版从随附资料读取脱敏快照，用 Python 逐项比较，并显示预设模型输出、模拟工具轨迹和独立的场景预期。公开入口只导入 Streamlit 和 Python 标准库。代码中没有飞书、模型或远程写入适配器，也没有密钥加载或运行模式切换入口。

## GitHub 与 Streamlit Community Cloud

仅以此目录作为新仓库根目录。推荐结构为 `app.py`、`requirements.txt`、`.streamlit/config.toml`、`.gitignore`、`assets/`、`README.md`。该目录的本地 Git 历史与本地 DEV 项目分开，发布时只使用这一仓库。

1. 确认发布后登录 GitHub，新建空的公开仓库，按 GitHub 提示推送此目录的 `main`。保留现有本地首提交，使用自己的账号登录。
2. 登录 Streamlit Community Cloud 并授权访问该 GitHub 仓库。在 `Create app` 选择仓库、`main` 分支和入口 `app.py`。
3. 在高级设置选 Python 3.11，Secrets 留空。部署后用无痕窗口打开分配的公开地址，复跑 A、B、C、确认与重载，最后填回作品集链接。

[Streamlit 部署说明](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) · [仓库文件结构](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)

备用平台使用 Hugging Face Docker Spaces 运行同一份应用。选择 Docker SDK，在 Space 中以 `python:3.11-slim` 安装 `requirements.txt`，用 `streamlit run app.py --server.address 0.0.0.0 --server.port 7860` 启动，并在 Space 配置中指定 `app_port: 7860`。只有 Community Cloud 无法使用时才准备这个容器。GitHub Pages 静态版留待 Python 托管均不可用时评估。 [Docker Spaces 文档](https://huggingface.co/docs/hub/spaces-sdks-docker)

公开演示 · [在线体验（免登录）](https://retireflow-public-demo.streamlit.app/)

GitHub 仓库 · [RetireFlow-Public-Demo](https://github.com/lyang10087-cpu/RetireFlow-Public-Demo)

2026-11-10 在未登录的 Edge 无痕会话中验证了 A、B、C、确认后刷新和 HR 历史示例。当前 Community Cloud 实例使用 Python 3.14.10、Streamlit 1.67.0，Secrets 为空。公开版业务路径使用随附材料和预设模型输出。托管平台可产生访问统计请求。
