import os
from itertools import product, islice, combinations

# GitHub settings
# GitHub访问令牌，从环境变量GH_TOKEN获取，默认为空字符串
GITHUB_TOKEN = os.environ.get("GH_TOKEN", "")

# GitHub搜索中使用的协议相关术语
GITHUB_PROTOCOL_TERMS = [
    "v2ray",
    "clash",
    "vmess",
    "vless",
    "trojan",
    "ss",
    "ssr",
]

# GitHub搜索中使用的基础标志词
GITHUB_BASE_FLAGS = [
    "free",
]

# GitHub搜索中使用的节点相关术语
GITHUB_NODE_TERMS = [
    "node",
    "nodes",
    "proxy",
    "proxies",
]

# GitHub搜索中使用的元信息术语
GITHUB_META_TERMS = [
    "subscribe",
]

# GitHub搜索中使用的上下文相关术语
GITHUB_CONTEXT_TERMS = GITHUB_NODE_TERMS + GITHUB_META_TERMS

# GitHub搜索中使用的额外术语（中文短语等）
GITHUB_EXTRA_TERMS = [
    "免费节点",
    "翻墙节点",
    "免费代理",
    "每日更新",
]

# GitHub搜索关键词的最大数量限制
_DEFAULT_MAX_GITHUB_KEYWORDS = 6
MAX_GITHUB_KEYWORDS = int(os.environ.get("MAX_GITHUB_KW", _DEFAULT_MAX_GITHUB_KEYWORDS))


def _build_github_keywords():
    """
    构建GitHub搜索关键词列表
    
    通过组合协议术语和上下文术语生成搜索关键词，避免重复并限制总数。
    同时添加额外的预定义关键词。
    
    Returns:
        list: 包含生成的关键词字符串列表，长度不超过MAX_GITHUB_KEYWORDS
    """
    keywords = []
    seen = set()

    def add_keyword(kw):
        if kw and kw not in seen:
            keywords.append(kw)
            seen.add(kw)

    # 1. 先添加额外术语（中文短语等）
    for kw in GITHUB_EXTRA_TERMS:
        if len(keywords) >= MAX_GITHUB_KEYWORDS:
            return keywords[:MAX_GITHUB_KEYWORDS]
        add_keyword(kw)

    if len(keywords) >= MAX_GITHUB_KEYWORDS:
        return keywords[:MAX_GITHUB_KEYWORDS]

    # 2. 生成两词组合：free + 协议 / 节点词
    for flag in GITHUB_BASE_FLAGS:
        for proto in GITHUB_PROTOCOL_TERMS:
            if len(keywords) >= MAX_GITHUB_KEYWORDS:
                return keywords[:MAX_GITHUB_KEYWORDS]
            add_keyword(f"{flag} {proto}")
        for node in GITHUB_NODE_TERMS:
            if len(keywords) >= MAX_GITHUB_KEYWORDS:
                return keywords[:MAX_GITHUB_KEYWORDS]
            add_keyword(f"{flag} {node}")

    if len(keywords) >= MAX_GITHUB_KEYWORDS:
        return keywords[:MAX_GITHUB_KEYWORDS]

    # 3. 生成三词组合：free + 协议 + 节点 / 元信息
    for flag in GITHUB_BASE_FLAGS:
        for proto in GITHUB_PROTOCOL_TERMS:
            for node in GITHUB_NODE_TERMS:
                if len(keywords) >= MAX_GITHUB_KEYWORDS:
                    return keywords[:MAX_GITHUB_KEYWORDS]
                add_keyword(f"{flag} {proto} {node}")
            for meta in GITHUB_META_TERMS:
                if len(keywords) >= MAX_GITHUB_KEYWORDS:
                    return keywords[:MAX_GITHUB_KEYWORDS]
                add_keyword(f"{flag} {proto} {meta}")

    return keywords[:MAX_GITHUB_KEYWORDS]


GITHUB_KEYWORDS = _build_github_keywords()

# Platform API keys
# Hunter.io平台API密钥，从环境变量HUNTER_API_KEY获取，默认为空字符串
HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY", "")
# Quake平台API密钥，从环境变量QUAKE_API_KEY获取，默认为空字符串
QUAKE_API_KEY = os.environ.get("QUAKE_API_KEY", "")

# Platform search keywords
# 平台搜索中使用的协议相关术语
PLATFORM_PROTOCOL_TERMS = [
    "v2ray",
    "vmess",
    "vless",
    "trojan",
    "hy2",
    "clash",
    "ss",
]

# 平台搜索中使用的上下文相关术语（精简为高价值项）
PLATFORM_CONTEXT_TERMS = [
    "subscribe",
    "free",
    "nodes",
    "config",
    "proxy",
    "proxies",
    "node list",
    "proxy list"
]

# 平台搜索中使用的独立术语（精简版）
PLATFORM_SINGLE_TERMS = [
    "shadowsocks",
    "wireguard",
]

# 平台搜索关键词的最大数量限制
# 可通过环境变量 MAX_PLATFORM_KW 覆盖，GitHub Action 建议设为 15-25
_DEFAULT_MAX_PLATFORM_KEYWORDS = 25
MAX_PLATFORM_KEYWORDS = int(os.environ.get("MAX_PLATFORM_KW", _DEFAULT_MAX_PLATFORM_KEYWORDS))


def _build_platform_keywords():
    """
    构建平台搜索关键词列表
    
    首先添加协议术语和单术语，然后通过组合协议术语与上下文术语生成复合关键词，
    避免重复并限制总数。
    
    Returns:
        list: 包含生成的关键词字符串列表，长度不超过MAX_PLATFORM_KEYWORDS
    """
    keywords = []
    seen = set()

    # 1. 添加单术语和协议术语
    for term in PLATFORM_PROTOCOL_TERMS + PLATFORM_SINGLE_TERMS:
        if term not in seen:
            keywords.append(term)
            seen.add(term)

    # 2. 生成并添加组合术语
    # 使用 product 高效生成笛卡尔积
    generated_keywords = (f"{proto} {ctx}" for proto, ctx in product(PLATFORM_PROTOCOL_TERMS, PLATFORM_CONTEXT_TERMS))

    for kw in generated_keywords:
        if len(keywords) >= MAX_PLATFORM_KEYWORDS:
            break
        if kw not in seen:
            keywords.append(kw)
            seen.add(kw)
            
    return keywords[:MAX_PLATFORM_KEYWORDS]


PLATFORM_KEYWORDS = _build_platform_keywords()

# Database
# 数据库路径，从环境变量DB_PATH获取，默认为'data/nodes.db'
DB_PATH = os.environ.get('DB_PATH', 'data/nodes.db')

# Export paths
# 导出文件路径
EXPORT_PATH = os.environ.get("EXPORT_PATH", "data/sub.txt")
# Base64编码导出文件路径
EXPORT_BASE64_PATH = os.environ.get("EXPORT_BASE64_PATH", "data/sub_base64.txt")
