/* 字段中文注释表 —— 供 dashboard.html 的 JSON 视图标注每个字段用途。未收录字段回退显示字段名 */
window.FIELDS = {
  // —— 通用锚点 ——
  item_id:"条号 NN-NNN（卷-序），回链底座指纹库",
  volume:"卷号（两位字符串）", vol:"卷号", slot:"原书内定位槽号",
  original:"原文（打包器从 _item_registry.json 注入，禁止手抄）",
  norm:"归一化原文（去异体/标点统一）",
  confidence:"置信度枚举 high/medium/low", source:"史料出处标记",
  id:"层内主键", ent_id:"实体主键回填", _layer:"所属层标记",
  layer:"所属层标记", generated_at:"打包时间", builder:"打包器版本",
  // —— 实体/文本定位 ——
  text:"实体字面（原文中出现的写法）", type:"类型（封闭枚举，来自 _kg_enums.py）",
  start:"原文起始偏移", end:"原文结束偏移", normalized:"规范化后的实体主名（别名→主名）",
  type_raw:"原始类型写法（未归一前）", rank_order:"品级排序号", provenance:"出处溯源标记",
  count:"出现次数/条目数", _todo:"待人工复核标记",
  // —— 事件五元组 ——
  who:"涉事人物{text,*_ent_ids}", action:"做了什么（谓语）", what:"涉及事项/对象",
  when:"时间（年号/干支原文）", where:"地点", title:"事件/流程/篇名",
  era:"年号纪年", era_raw:"年号原文（未规范化）", era_first:"该条目首次出现的年号",
  year:"年份（公历推算）", age:"谱主年龄（年谱特化）", first_person:"是否第一人称记事",
  category:"类别（封闭枚举）", ref_events:"关联事件键列表",
  related_reg_key:"关联制度层 key", related_evo:"关联沿革记录", related_ledger:"关联钱粮账树节点",
  ent_keys:"关联实体主名列表", src_loc:"原书位置（卷/页/段）",
  // —— 职官任职 ——
  person:"任职者", office:"官职名", institution:"任职机构", status:"任职状态（任/追赠/未就…）",
  start_end:"起止时间", official:"职官",
  // —— 实体引用嵌套 ——
  person_a:"关系主体甲", person_b:"关系主体乙", relation_type:"关系类型（亲缘/师友/政争…）",
  direction:"关系方向（单向/双向/未明）", evidence:"引证原文句",
  // —— 论说/翻译 ——
  topic:"论题", stance:"立场（封闭枚举）", argument:"论证内容", evidence_refs:"证据引用列表",
  speaker:"发言者", target:"评论对象/指向", quote:"引文原文", markers:"论说标记词",
  trigger:"触发事由", translation:"白话译文", style:"翻译风格档位", note:"译注",
  // —— 文献/引书/名物 ——
  cited_work:"所引书名", citation_type:"引用方式（直引/转述/化用…）", context:"引用上下文",
  author:"作者", content_location:"内容所在卷次", summary:"内容提要约记",
  name:"名称", attributes:"属性集（形制/用途等嵌套对象）", lore:"掌故考辨文字",
  obj_name:"器物名", obj_category:"器物类别（枚举）",
  // —— 风俗/地理/名录 ——
  region:"流行地域", term:"方言词/风俗名目", description:"释语",
  location:"方位/所在地", history:"沿革叙述", scope:"收录范围",
  names:"别名/称谓列表", entries:"名录条目数组（他书为四元组对象）",
  nam_type:"名录类型", prince:"藩王/主名", chars:"字辈/字符",
  // —— 典章制度 ——
  institutions:"涉及机构列表", officials:"涉及职官列表", evolution:"沿革脉络",
  selection_type:"选任类型（科举/学校/贡举…）", exam_tier:"考试层级（乡试/会试/殿试）",
  agencies:"主管机构", targets:"适用对象", tme_keys:"关联时间沿革键", evt_keys:"关联事件键",
  proc_keys:"关联流程键", key:"制度主键（跨层挂接用）",
  inst_type:"制度类型", "主体":"制度约束的主体", "对象":"制度作用的对象", "标准":"执行标准/额度",
  "存续":"存续时段", "文书载体":"使用的文簿载体", "执行者":"落实的官署/人员",
  "目的":"制度设计目的", "沿革":"沿革变化", "史料来源":"文献出处",
  docs:"关联文书", agent_kinds:"执行者类别", purpose:"目的",
  // —— 规则 ——
  modals:"情态词（应/禁/许…）", condition:"成立条件", subject:"规范主体",
  object:"规范客体", punishment:"罚则", deadline:"期限", prohibited_action:"禁止行为",
  prohibited_effect:"禁止事项的效果", allowed_action:"允许行为", obligation_action:"义务行为",
  analysis:"AI/人工解析附记", derived_rule:"由该条派生出的规则标记",
  rule_type:"规则类型（7 型枚举）", modal:"情态词", predicate:"谓语行为", exception:"例外条款",
  penalty:"罚则", source_marker:"事例来源标记（会典‘事例’出处）",
  section:"所属章节节点", node_kind:"节点种类", subject_norm:"主体归一名",
  // —— 四维结构 ——
  dim:"维度（ACT 职责/FRD 防弊/LGR 文簿/TME 时限…）", act_type:"维度内子类（按 dim 换名）",
  keeper:"掌管者", entry:"登记方式", frequency:"使用频率", check:"稽核办法", anti_fraud:"防弊措施",
  role:"职责承担角色", responsibility:"职责内容", stage:"阶段标记",
  // —— 流程/文书 ——
  steps:"步骤数组（step_id/seq/text/agent/next…）", state_machine:"状态机描述",
  events:"关联事件列表", event_type:"触发事件类型", timeline:"时序", next_process:"后继流程",
  process_name:"流程名", process_type:"流程类别", length:"步骤数",
  format:"文书格式", flow:"文书流转路径", related_item:"关联条目",
  doc_name:"文册名", doc_category:"文册类别", rep_id:"文册主键",
  // —— 时间沿革/切片 ——
  reign:"纪年（年号+历年）", phase:"沿革阶段", change_type:"变更类型（置/省/复/升/降）",
  change:"变更内容", place:"所在处",
  // —— 地理树 ——
  level:"层级（京师/司/府/州/县…）", node_type:"节点类型", tusi_type:"土司类型",
  parent:"父节点", children:"子节点（递归）", to_anchor:"方位（到治所方向）",
  bearing_distance:"里距", is_virtual:"是否虚拟节点", administered_by:"辖属机构",
  garrisons:"关镇", post_stations:"驿传", granaries:"仓场", declared:"原书声明项（中文键）",
  geo_name:"政区名", parent_geo:"上级政区", record_count:"下辖记录数",
  // —— 数额/器物 ——
  num_id:"数额主键", kind:"数额种类", quantity:"数量", unit:"单位", context:"语境原文",
  mat_id:"工料主键", material:"物料名",
  // —— 明律/礼仪 ——
  crime:"罪名", crime_category:"罪类", punishment_type:"刑罚类型", punishment_level:"刑等",
  source_law:"所本律条", relevant_orgs:"相关机构",
  ritual_id:"礼仪主键", ritual_name:"礼仪名", participants:"参与人员",
  dress_id:"冠服主键", insp_id:"风宪主键", affair_type:"公务类型",
  // —— 品级/两京/互见 ——
  rank_id:"品级主键", category_chaofu:"（冠服/公服/常服/巾服…）",
  chaofu:"朝服配置", gongfu:"公服配置", changfu:"常服配置", jifu:"巾服配置",
  housing:"第宅规制", tableware:"器物规制", umbrella:"伞盖", carriage:"车乘",
  zhangman:"仪仗幔帐", anpei:"安陪（从祀/配设）",
  beijing:"北京制", nanjing:"南京制", beijing_item:"北京条目", nanjing_item:"南京条目",
  difference:"两京差异", source_item:"来源条目",
  xref_id:"互见主键", from_item:"起条", from_volume:"起卷", from_layer:"起层",
  ref_type:"互见类型", target_org:"目标机构",
  // —— 主档 ——
  org_name:"部门名", staff:"编制（role/count/rank 数组）", duties:"职掌",
  parent_org:"上级部门", child_orgs:"下级机构", salary:"俸禄（月/石/年）",
  office_name:"官职名", system:"铨选体系（举/贡/荫…）", headcount:"员额",
  parent_office:"上级官职", child_offices:"下级官职", duties_source:"职掌出处",
  salary_note:"俸禄备注", history:"沿革事件数组（year/era/event/detail）",
  person_id:"人物主键",
  // —— 职官明细表 ——
  official_id:"职官明细主键", org_path:"机构全路径", grade:"品级", grade_order:"品级序",
  item_ids:"关联底座条号", rank_ids:"关联品级树", link_to_bj:"北京对应项",
  org_binding:"机构绑定", peers:"同级官", relations:"关系", subordinates:"下属",
  sources:"出处", sources_cn:"出处（中文键子对象）",
  // —— 主题时间线 ——
  tim_id:"主题主键", theme:"制度主题", group:"主题分组", keywords:"检索关键词",
  volumes:"涉及卷次", era_span:"跨朝年代", rule_count:"关联规则数", event_count:"关联事件数",
  era_chain:"年号链（era/count/events/samples）",
  // —— 其他 ——
  target_ent_ids:"对象实体回填", subject_ent_ids:"主体实体回填",
  who_ent_ids:"涉事人物实体回填", ent_ids:"实体主键列表", institution_ent_ids:"机构实体回填",
  person_ent_ids:"人物实体回填", official_ent_ids:"职官实体回填", author_ent_ids:"作者实体回填",
  institution_ent:"机构实体", tme_keys_note:"关联沿革", norm_type:"类型归一",
  org_id:"机构主键", org_binding_note:"机构挂接", "item":"数额事项",
  "form":"数额形式（实数/约数/区间）", "origin":"数额来源", "side":"收支方向",
  "dimension":"所属维度", alt:"别名", flow_hyd:"河流走向", anchor:"所在锚点政区",
  territorial:"辖地", established:"设置时间", dusi:"都司归属",
  site:"产地", importance:"重要性说明", raw:"原文直录",
  headcount_note:"员额", "prince_chars":"藩名+字辈"
};
