# FigJam 流程图与功能清单

> 从 SKILL.md 拆出（2026-10-30）。做技术流程图、功能清单前读。描述列同样不写视觉规格。


在白板 `<FigJam 白板 fileKey>` 制作：

- **每个流程图一个 SECTION**，fill `#FFFFFF`、stroke `#E6E6E6`，命名 `<模块>-<子流程>`。功能清单 TABLE 与事实源声明 TEXT 放页面层级
- **页级 TEXT 事实源声明**（Inter Medium 24px）四行：`唯一事实源` / `范围` / `边界` / `派生工件`
- 形状语义：普通步骤 ROUNDED_RECTANGLE 320×96 白底 + stroke `#757575` 4px；判断 DIAMOND 360×160；失败/阻断 `#FFCDC2`；成功终态 `#CDF4D3`；**降级终态（塌陷、不下发、静默失败）`#FFE0C2`**；规则/边界块 `#EDEDED`。文字 Inter Medium 16px
- 流程图配色是 FigJam 工作色，不受设计系统 token 约束
- 连接线：`#757575`、strokeWeight 4、ELBOWED、NONE→ARROW_LINES，**分支条件写在 connector 自身 text 上**
- **connector 的 text.fontName 默认为空，必须先赋 fontName 再写 characters**，否则报 `Font family "" is not available`
- **每个节点每个磁吸点最多挂一条线**：多条线汇入同一节点时用不同磁吸点，或加显式汇聚节点
- **每个非终态节点必须有出线**：只有入线没有出线的白底步骤节点是悬空终点。循环回退要显式连回判定节点并标「重新判定」
- 规则块（`#EDEDED`）不连线是允许的，不算孤立节点
- 便签 STICKY 不使用
- **功能清单用原生 TABLE**：表头行 fill `#1E1E1E` 白字 Inter Medium 16px；分组行整行彩底白字（`#874FFF` `#3DADFF` `#66D575` `#FF9E42` 依组循环）；内容行白底黑字。列一般为 功能名称 / 范围 / 描述 / 开发端。**无「编号」列、无「关联屏编号」列**。功能名称写「对象 + 行为/状态/规则」，描述按「触发—处理—结果—例外」。不留全空行；未知写「待确认」，无关写「不适用」
- **描述列同样不写视觉规格**——它是说明性文字，适用「说明卡正文不写视觉规格」的全部规则
- **功能清单要与说明卡逐条对齐**：说明卡里每一块独立功能都要有对应行。实战中最容易漏的是素材规格、披露类组件、后台侧校验、频控与配置拉取这四类
- 做好后整体复制粘贴回原型 PRD 对应大区

**三个 API 限制**
- TABLE 的列宽只读，且 TABLE **没有 `resize` 方法**。`createTable` 默认 4 列共 768 宽，描述列会被撑得很高，只能人工在 UI 里拖宽。列数要一次规划好
- TABLE、CONNECTOR、SHAPE_WITH_TEXT 在 design 模式被禁用，复制回原型 PRD 只能 UI 手动 Cmd+C / Cmd+V
- FigJam 读结构用 `figma_execute` 只读脚本（桥接插件在 FigJam 端运行），或 `figjam_get_board_contents` / `figjam_get_connections`
