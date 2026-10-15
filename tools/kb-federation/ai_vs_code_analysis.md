# AI Judgment vs Code Matching Analysis

**Date**: 2026-10-14  
**Sample**: 50 random person nodes from kb_test.sqlite  
**Purpose**: Compare AI-determined ground truth with four_step_matching results

---

## 1. AI Judgment Ground Truth

From 50 sampled person nodes, AI identified **10 should-match pairs** based on:
- Name variants (字/号/谥号/封号)
- Honorific titles (公/少师/布政)
- Context clues (era, place, associated people)
- Historical knowledge

### Identified Matches

| # | Entity UID | Name Variants | Match Type | Evidence |
|---|---|---|---|---|
| 1 | sdr:27:ENT-1300 | 耿九畴 = 耿恒庵 | 号 | "号恒庵" in label |
| 2 | kzz:05:ENT-0019 | 桓彝 = 桓公彝 | 敬称 | "桓公彝" in context list |
| 3 | sdr:07:ENT-1645 | 丰文庆 = 丰布政文庆 | 官职+名 | "丰布政文庆" in context |
| 4 | kzz:02:ENT-0238 | 南唐后主 = 南堂后主 | 误刻 | "南堂后主" with note 堂→唐 |
| 5 | kzz:05:ENT-0008 | 周访 = 周公访 | 敬称 | "周公访" in context list |
| 6 | kzz:10:ENT-0708 | 秦皇 = 秦始皇 | 简称 | Both refer to Qin Shi Huang |
| 7 | sdr:03:ENT-671 | 杨维桢 = 杨廉夫 | 号 | "号廉夫" in label |
| 8 | wzz:15:ENT-3733 | 诸葛亮 = 诸葛武侯 | 封号 | "诸葛武侯" in context |
| 9 | wzz:08:ENT-1744 | 杨廷和 = 杨少师廷和 | 官职+名 | "杨少师廷和" in context |
| 10 | kzz:09:ENT-0037 | 张居正 = 张文忠公 | 谥号 | "张文忠公居正" in context |

---

## 2. Code Matching Results

**Total candidates generated**: 130 (from four_step_matching)  
**AI-identified matches found**: 1/10  
**Recall**: 10.0%

### What Was Found

✓ **耿九畴 = 耿恒庵** (2 candidates)
- Method: exact name match on "耿九畴"
- Both forms share the base name

### What Was Missed (9/10)

✗ **桓彝 = 桓公彝**
- Reason: "公" is an honorific prefix, not part of the name
- Code treats "桓公彝" as a different surface form
- **Missing**: Honorific stripping logic

✗ **丰文庆 = 丰布政文庆**
- Reason: "布政" is a title (布政使), not part of the name
- Code doesn't recognize title+name patterns
- **Missing**: Title extraction and name isolation

✗ **南唐后主 = 南堂后主**
- Reason: Typo variant (堂→唐) noted in text
- Code requires exact or normalized match
- **Missing**: Typo/correction handling

✗ **周访 = 周公访**
- Reason: Same as 桓彝 - honorific "公" prefix
- **Missing**: Honorific stripping logic

✗ **秦皇 = 秦始皇**
- Reason: Abbreviated form vs full name
- Code doesn't handle historical abbreviations
- **Missing**: Abbreviation expansion rules

✗ **杨维桢 = 杨廉夫**
- Reason: 廉夫 is 号 (style name), completely different characters
- Code only matches on name similarity, not alias lookup
- **Missing**: Alias/号 cross-reference index

✗ **诸葛亮 = 诸葛武侯**
- Reason: 武侯 is 封号 (posthumous title), not name
- Code doesn't extract or match titles
- **Missing**: Title-to-name mapping

✗ **杨廷和 = 杨少师廷和**
- Reason: "少师" is title, name is embedded
- Code doesn't parse title+name compounds
- **Missing**: Title extraction and name isolation

✗ **张居正 = 张文忠公**
- Reason: 文忠 is 谥号 (posthumous name), completely different
- Code doesn't have 谥号→本名 mapping
- **Missing**: Posthumous name cross-reference

---

## 3. Root Cause Analysis

### Why Recall is Only 10%

**Current four_step_matching strengths**:
- ✓ Exact name matching (normalized)
- ✓ Surface form matching (alias field)
- ✓ Context similarity (Jaccard on surrounding text)
- ✓ Relation network overlap (when relations exist)

**Current four_step_matching weaknesses**:
- ✗ No honorific/title stripping (公/少师/布政/御史)
- ✗ No 字号谥号 cross-reference index
- ✗ No abbreviation handling (秦皇→秦始皇)
- ✗ No typo/correction handling
- ✗ No title+name compound parsing
- ✗ No posthumous name mapping

### Missing Capabilities

1. **Honorific Stripping** (affects 2/10 missed)
   - Pattern: X公Y → X Y (e.g., 桓公彝 → 桓彝)
   - Implementation: Regex to detect and remove 公/子/先生 etc.

2. **Title Extraction** (affects 3/10 missed)
   - Pattern: [官职]+[名] (e.g., 丰布政文庆 → 丰文庆)
   - Implementation: Office title dictionary + name extraction

3. **Alias/字号 Index** (affects 3/10 missed)
   - Need: Build alias table from ent_slots (号/字/谥号)
   - Query: Look up 廉夫 → 杨维桢, 文忠 → 张居正

4. **Abbreviation Rules** (affects 1/10 missed)
   - Pattern: 秦皇 → 秦始皇, 汉武 → 汉武帝
   - Implementation: Historical abbreviation dictionary

5. **Typo Handling** (affects 1/10 missed)
   - Pattern: 南堂后主 → 南唐后主 (with explicit correction note)
   - Implementation: Extract corrections from text notes

---

## 4. Comparison with Methodology

### What 跨书身份判定方法论.md Prescribes

From the methodology document (Section 4.1 人):

```
L0 主键: 庙号（一朝一帝）；本名选择性=1 时
L1 升级: 本名 × 年代窗
L2 升级: × 籍贯
L3 升级: × 主职/师承/亲属
L4 画像: 关系画像
```

**What's implemented**:
- L0: Partial (本名 matching only)
- L1: Partial (context similarity as proxy for 年代窗)

**What's missing**:
- 称谓槽收割 (aliases, 字号, 谥号, 封号)
- 庙号 matching (太祖→朱元璋)
- Title+name compound parsing
- Alias cross-reference index

### Gap Summary

| Methodology Requirement | Implementation Status | Gap |
|---|---|---|
| 称谓槽 (aliases/字号/谥号) | ❌ Not harvested | Need harvest.py extension |
| 庙号 matching | ❌ Not implemented | Need designator stream |
| Title+name parsing | ❌ Not implemented | Need NLP rule |
| Alias cross-reference | ❌ Not implemented | Need alias index |
| Honorific stripping | ❌ Not implemented | Need regex rule |
| Abbreviation handling | ❌ Not implemented | Need dictionary |

---

## 5. Recommendations

### Priority 1: Alias Index (affects 3/10 missed)

**Implementation**:
```python
# Build from ent_slots where kind IN ('字', '号', '谥号', '封号')
alias_index = {
    '廉夫': 'sdr:03:ENT-671',  # 杨维桢
    '文忠': 'kzz:09:ENT-0037',  # 张居正
    '武侯': 'wzz:15:ENT-3733',  # 诸葛亮
}

# In step2_alias_match, add:
if surface in alias_index:
    yield (uid, alias_index[surface], 'alias_crossref', 0.85)
```

**Effort**: Medium (need to harvest aliases first)  
**Impact**: High (30% of missed matches)

### Priority 2: Title Extraction (affects 3/10 missed)

**Implementation**:
```python
# Office title dictionary
OFFICE_TITLES = ['布政', '尚书', '御史', '少师', '总兵', '知县']

def extract_name_with_title(text):
    for title in OFFICE_TITLES:
        if title in text:
            # Remove title, keep name
            name = text.replace(title, '')
            return name
    return text

# Example: "丰布政文庆" → "丰文庆"
```

**Effort**: Low (dictionary + regex)  
**Impact**: High (30% of missed matches)

### Priority 3: Honorific Stripping (affects 2/10 missed)

**Implementation**:
```python
# Honorific prefix pattern
HONORIFICS = ['公', '子', '先生', '夫子']

def strip_honorifics(name):
    for h in HONORIFICS:
        if h in name and len(name) > len(h) + 1:
            # Remove honorific, keep rest
            return name.replace(h, '', 1)
    return name

# Example: "桓公彝" → "桓彝"
```

**Effort**: Low (regex)  
**Impact**: Medium (20% of missed matches)

### Priority 4: Abbreviation Dictionary (affects 1/10 missed)

**Implementation**:
```python
ABBREVIATIONS = {
    '秦皇': '秦始皇',
    '汉武': '汉武帝',
    '唐宗': '唐太宗',
    '宋祖': '宋太祖',
}

# In normalize(), expand abbreviations
```

**Effort**: Low (dictionary)  
**Impact**: Low (10% of missed matches)

### Priority 5: Typo Handling (affects 1/10 missed)

**Implementation**:
```python
# Extract corrections from text notes
# Pattern: "X：当为Y之误刻" → add correction X→Y

def extract_corrections(text):
    pattern = r'(\S+)：当为"(\S+)"之误刻'
    matches = re.findall(pattern, text)
    return {wrong: correct for wrong, correct in matches}

# Example: "堂：当为"唐"之误刻" → {'堂': '唐'}
```

**Effort**: Medium (NLP extraction)  
**Impact**: Low (10% of missed matches)

---

## 6. Expected Improvement

### Current State
- Recall: 10% (1/10)
- Precision: Unknown (need to check false positives)
- Coverage: 11.0% (from merge_experiment_report.md)

### After Implementing Priorities 1-3

**Expected Recall**: 10% → 90% (9/10)
- Alias index: +3 matches
- Title extraction: +3 matches
- Honorific stripping: +2 matches
- (Abbreviation + typo: +2 matches, but lower priority)

**Expected Coverage**: 11% → 25-30%
- More cross-book merges
- Better entity resolution

**Effort**: 2-3 days implementation + testing

---

## 7. Conclusion

The four_step_matching strategy improved coverage from 3.6% to 11.0%, but recall on AI-identified matches is only 10%. The root cause is missing **称谓槽收割** and **alias cross-reference** capabilities.

**Key insight**: The methodology document (跨书身份判定方法论.md) correctly identifies the need for alias/title/谥号 handling, but the implementation hasn't caught up.

**Next steps**:
1. Implement alias index (Priority 1)
2. Implement title extraction (Priority 2)
3. Implement honorific stripping (Priority 3)
4. Re-run matching and measure recall improvement
5. Target: 90%+ recall on AI-identified matches

**Validation**: After improvements, re-sample 50 nodes and verify recall ≥ 90%.
