# 唯一规则owner：去重规则
version: 2.0
status: active
effective: 2026-09-01
approved-change: CR-02（合成）
新有效规则：同一条内容在0到30天内（含第30天）属于重复；超过30天可重新使用。输入是非负整数天数。
L1只路由，L2只定义接口，L3拥有上述规则。有效入口由active.json登记，生成物也必须遵守本规则。
