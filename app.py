"""RetireFlow PUBLIC_DEMO entry point. Uses bundled, fictional fixtures only."""

import json
from pathlib import Path

import streamlit as st


PUBLIC_DEMO = "PUBLIC_DEMO"
ASSETS = Path(__file__).resolve().parent / "assets"
FIELDS = ("出生年月", "参加工作时间", "职称")
CASES = {"A": "正常材料", "B": "工作时间冲突", "C": "缺必需材料"}


def clear_confirmation():
    st.session_state.pop("confirmed", None)


def comparison(case):
    return [
        {"字段": label, "预设识别值": material, "档案基准值": baseline,
         "快照 AI 值": current or "空", "拟写入值（仅预览）": material,
         "Python 比对": "一致" if material == baseline else "冲突"}
        for label, material, baseline, current in zip(FIELDS, case["material"], case["baseline"], case["ai"], strict=True)
    ]


def workbench(case):
    st.subheader("V2 预审对照")
    historical, projected = st.columns(2)
    with historical.container(border=True):
        st.metric("V2 · 脱敏演示快照", case["snapshot_v2"])
        st.caption(f"应交 {case['required']} 类 · 有效 {case['valid']} 类 · 缺 {case['required'] - case['valid']} 类")
    with projected.container(border=True):
        st.metric("V2 · 固定场景预期", case["expected_v2"])
        st.caption(case["explanation"])

    st.subheader("字段比对与人工确认")
    st.caption("Python 逐项比较预设识别值和脱敏快照基准。拟写入列仅用于预览。")
    rows = comparison(case)
    for row in rows:
        if row["Python 比对"] == "冲突":
            st.warning(f"字段冲突 · {row['字段']}的材料值 {row['预设识别值']} 与基准 {row['档案基准值']} 不同。")
    st.dataframe(rows, hide_index=True, width="stretch")
    if st.button("确认预览（仅本次会话）", key="confirm", type="primary"):
        st.session_state.confirmed = True
    if st.session_state.get("confirmed", False):
        st.success("已确认预览 · 仅记录在当前会话 · 远程写入 0 次")
    with st.expander("查看 V2 规则说明"):
        st.write("本地版由飞书公式先判断字段冲突，再处理材料条件与缺件，最后按字段一致性判断通过或待人工复核。"
                 "有效材料须适用、已提交且有附件，按材料类型去重。公开版展示固定快照和场景预期。")


def hr_examples(selected):
    st.subheader("HR 审核历史示例")
    st.caption("按已验证流程重建的公开示例 · 序号为演示编号 · 来源为虚构档案")
    if selected != "C":
        st.info("切换到场景 C，可查看缺件后的提交、复核与退回补件示例。")
        return
    st.dataframe([
        {"演示编号": "示例 01", "操作": "提交审核", "状态变化": "未提交 → 已提交", "结论": "—"},
        {"演示编号": "示例 02", "操作": "完成复核", "状态变化": "已提交 → 已结束", "结论": "退回补充材料"},
    ], hide_index=True, width="stretch")
    st.caption("原流程在飞书通过原生按钮触发并生成日志。此页展示脱敏重建示例。")


def main():
    st.set_page_config(page_title="RetireFlow · 公开展示", page_icon="📋", layout="wide")
    st.title("RetireFlow · 退休材料预审")
    st.info("公开展示 · 预设模型输出 · 未调用真实大模型")
    st.caption(f"{PUBLIC_DEMO} · 完全虚构的场景材料 · 档案快照 · 本地预览确认")
    cases = json.loads((ASSETS / "scenarios.json").read_text(encoding="utf-8"))
    selected = st.radio("选择演示场景", list(CASES), format_func=lambda key: f"{key} · {CASES[key]}",
                        horizontal=True, key="case", on_change=clear_confirmation)
    st.button("重载当前场景", on_click=clear_confirmation)
    case = cases[selected]
    st.caption(f"档案快照 · RF-DEMO-{selected} · {case['name']} · 无实时查询")

    overview, source, hr, tools = st.tabs(["场景工作台", "材料与预设识别", "HR 历史示例", "架构与模拟轨迹"])
    with overview:
        workbench(case)
    with source:
        raw, structured = st.columns(2)
        raw.markdown("**随附虚构材料**")
        raw.code((ASSETS / f"RF-DEMO-{selected}.txt").read_text(encoding="utf-8"), language=None)
        structured.markdown("**预设模型输出 · 未调用真实大模型**")
        structured.json({"档案编号": f"RF-DEMO-{selected}", "姓名": case["name"],
                         **dict(zip(FIELDS, case["material"], strict=True))})
    with hr:
        hr_examples(selected)
    with tools:
        st.image((ASSETS / "architecture.svg").read_text(encoding="utf-8"), width="stretch")
        st.subheader("模拟工具轨迹")
        st.table([
            {"环节": "材料识别与工具选择", "来源": "模拟轨迹 · 固定预设"},
            {"环节": "档案查询", "来源": "模拟轨迹 · 读取随附快照"},
            {"环节": "逐项比较", "来源": "Python · 本次本地计算"},
            {"环节": "预览确认", "来源": "人工点击 · 当前会话状态"},
            {"环节": "V2 与 HR 留痕", "来源": "固定快照、场景预期及审核示例"},
        ])
        st.caption("本地 DEV 版本曾实测飞书只读查询。真实模型推理、实际工具选择及端到端写入待验收。")


if __name__ == "__main__":
    main()
