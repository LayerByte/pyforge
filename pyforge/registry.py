from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

from pyforge.models import ToolSpec

TOOL_SPECS: list[ToolSpec] = []


def get_tool(name: str) -> ToolSpec:
    for spec in TOOL_SPECS:
        if spec.name == name:
            return spec
    raise KeyError(f"unknown tool: {name}")


def load_callable(spec: ToolSpec) -> Callable[..., Any]:
    module_name, function_name = spec.import_path.split(":", 1)
    return getattr(import_module(module_name), function_name)


TOOL_SPECS.append(
    ToolSpec(
        name="files.information",
        category="files",
        title="File Information",
        description="Inspect file size, type, timestamps, and permissions.",
        import_path="pyforge.tools.files.core:file_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.hash",
        category="files",
        title="File Hash",
        description="Calculate a supported digest for a local file.",
        import_path="pyforge.tools.files.core:file_hash",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.comparison",
        category="files",
        title="File Comparison",
        description="Compare file metadata and content without modifying either file.",
        import_path="pyforge.tools.files.core:compare_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.duplicates",
        category="files",
        title="Duplicate Finder",
        description="Group duplicate files by size and SHA-256 content digest.",
        import_path="pyforge.tools.files.core:find_duplicates",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.directory-statistics",
        category="files",
        title="Directory Statistics",
        description="Summarize directory counts, bytes, and extensions.",
        import_path="pyforge.tools.files.core:directory_statistics",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.directory-tree",
        category="files",
        title="Directory Tree",
        description="Render a bounded text tree for a directory.",
        import_path="pyforge.tools.files.core:directory_tree",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.search",
        category="files",
        title="File Search",
        description="Find files by a case-sensitive glob-style name pattern.",
        import_path="pyforge.tools.files.core:search_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.large-files",
        category="files",
        title="Large File Finder",
        description="List files meeting a minimum size threshold.",
        import_path="pyforge.tools.files.core:find_large_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.empty-files",
        category="files",
        title="Empty File Finder",
        description="Find zero-byte regular files recursively.",
        import_path="pyforge.tools.files.core:find_empty_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.extension-statistics",
        category="files",
        title="File Extension Statistics",
        description="Count files by normalized extension.",
        import_path="pyforge.tools.files.core:extension_statistics",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="files.integrity-snapshot",
        category="files",
        title="File Integrity Snapshot",
        description="Create a deterministic SHA-256 manifest without changing files.",
        import_path="pyforge.tools.files.core:integrity_snapshot",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.statistics",
        category="text",
        title="Text Statistics",
        description="Summarize characters, words, lines, sentences, paragraphs, and reading time.",
        import_path="pyforge.tools.text.core:text_statistics",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.word-count",
        category="text",
        title="Word Counter",
        description="Count Unicode-aware word tokens.",
        import_path="pyforge.tools.text.core:word_count",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.line-count",
        category="text",
        title="Line Counter",
        description="Count logical text lines consistently.",
        import_path="pyforge.tools.text.core:line_count",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.character-count",
        category="text",
        title="Character Counter",
        description="Count Unicode code points with optional whitespace exclusion.",
        import_path="pyforge.tools.text.core:character_count",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.duplicate-lines",
        category="text",
        title="Duplicate Line Finder",
        description="Report repeated lines and their occurrence counts.",
        import_path="pyforge.tools.text.core:duplicate_lines",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.difference",
        category="text",
        title="Text Difference",
        description="Produce a unified line-oriented text diff.",
        import_path="pyforge.tools.text.core:text_difference",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.whitespace-cleaner",
        category="text",
        title="Whitespace Cleaner",
        description="Trim trailing whitespace and normalize excessive blank lines.",
        import_path="pyforge.tools.text.core:clean_whitespace",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.case-converter",
        category="text",
        title="Case Converter",
        description="Convert text to common developer naming styles.",
        import_path="pyforge.tools.text.core:convert_case",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.slugify",
        category="text",
        title="Slug Generator",
        description="Convert text into a lowercase URL-friendly slug.",
        import_path="pyforge.tools.text.core:slugify",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.sorter",
        category="text",
        title="Text Sorter",
        description="Sort lines with case and uniqueness controls.",
        import_path="pyforge.tools.text.core:sort_text",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.search",
        category="text",
        title="Text Search",
        description="Return numbered lines containing a query.",
        import_path="pyforge.tools.text.core:search_text",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="text.regex-tester",
        category="text",
        title="Regex Tester",
        description="Compile a regular expression and report matches and groups.",
        import_path="pyforge.tools.text.core:regex_test",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.base64-encode",
        category="encoding",
        title="Base64 Encode",
        description="Encode Unicode text as Base64.",
        import_path="pyforge.tools.encoding.core:base64_encode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.base64-decode",
        category="encoding",
        title="Base64 Decode",
        description="Decode validated Base64 into UTF-8 text.",
        import_path="pyforge.tools.encoding.core:base64_decode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.url-encode",
        category="encoding",
        title="URL Encode",
        description="Percent-encode text for URL components.",
        import_path="pyforge.tools.encoding.core:url_encode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.url-decode",
        category="encoding",
        title="URL Decode",
        description="Decode percent-encoded URL text.",
        import_path="pyforge.tools.encoding.core:url_decode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.hex-encode",
        category="encoding",
        title="Hex Encode",
        description="Encode UTF-8 text as hexadecimal bytes.",
        import_path="pyforge.tools.encoding.core:hex_encode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.hex-decode",
        category="encoding",
        title="Hex Decode",
        description="Decode hexadecimal bytes as UTF-8 text.",
        import_path="pyforge.tools.encoding.core:hex_decode",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.html-escape",
        category="encoding",
        title="HTML Escape",
        description="Escape text for safe HTML display.",
        import_path="pyforge.tools.encoding.core:html_escape",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="encoding.html-unescape",
        category="encoding",
        title="HTML Unescape",
        description="Resolve HTML entities into Unicode text.",
        import_path="pyforge.tools.encoding.core:html_unescape",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="hashing.text",
        category="hashing",
        title="Text Hashing",
        description="Hash UTF-8 text with compatibility and modern digest algorithms.",
        import_path="pyforge.tools.hashing.core:hash_text",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="hashing.file",
        category="hashing",
        title="File Hashing",
        description="Stream a local file into a selected digest.",
        import_path="pyforge.tools.hashing.core:hash_file",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="hashing.compare",
        category="hashing",
        title="Hash Comparison",
        description="Compare normalized digest strings in constant time.",
        import_path="pyforge.tools.hashing.core:compare_hashes",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.formatter",
        category="json_tools",
        title="JSON Formatter",
        description="Pretty-print valid JSON with stable indentation.",
        import_path="pyforge.tools.json_tools.core:format_json",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.minifier",
        category="json_tools",
        title="JSON Minifier",
        description="Remove insignificant whitespace from valid JSON.",
        import_path="pyforge.tools.json_tools.core:minify_json",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.validator",
        category="json_tools",
        title="JSON Validator",
        description="Return structured JSON validation details.",
        import_path="pyforge.tools.json_tools.core:validate_json",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.viewer",
        category="json_tools",
        title="JSON Viewer",
        description="Flatten JSON values into readable path-value rows.",
        import_path="pyforge.tools.json_tools.core:json_view",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.statistics",
        category="json_tools",
        title="JSON Statistics",
        description="Count JSON containers, keys, values, and depth.",
        import_path="pyforge.tools.json_tools.core:json_statistics",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.key-search",
        category="json_tools",
        title="JSON Key Search",
        description="Find matching object keys and their JSON paths.",
        import_path="pyforge.tools.json_tools.core:search_json_keys",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="json_tools.comparison",
        category="json_tools",
        title="JSON Comparison",
        description="Compare parsed JSON and report differing paths.",
        import_path="pyforge.tools.json_tools.core:compare_json",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.dns-lookup",
        category="network",
        title="DNS Lookup",
        description="Resolve a hostname to unique local resolver addresses.",
        import_path="pyforge.tools.network.core:dns_lookup",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.reverse-dns",
        category="network",
        title="Reverse DNS Lookup",
        description="Resolve an IP address to a hostname.",
        import_path="pyforge.tools.network.core:reverse_dns_lookup",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.local-ip",
        category="network",
        title="Local IP Information",
        description="Show local hostname and resolver addresses.",
        import_path="pyforge.tools.network.core:local_ip_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.interfaces",
        category="network",
        title="Network Interface Viewer",
        description="List local interface addresses and state.",
        import_path="pyforge.tools.network.core:network_interfaces",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.public-ip",
        category="network",
        title="Public IP Viewer",
        description="Read the public IP from a minimal HTTPS endpoint.",
        import_path="pyforge.tools.network.core:public_ip",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.http-headers",
        category="network",
        title="HTTP Header Viewer",
        description="Fetch response headers with redirects and timeouts.",
        import_path="pyforge.tools.network.core:http_headers",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.http-status",
        category="network",
        title="HTTP Status Checker",
        description="Check response status and elapsed time safely.",
        import_path="pyforge.tools.network.core:http_status",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="network.url-parser",
        category="network",
        title="URL Parser",
        description="Parse and validate HTTP or HTTPS URL components.",
        import_path="pyforge.tools.network.core:parse_url",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.cpu",
        category="system",
        title="CPU Information",
        description="Report processor counts, frequency, and current load.",
        import_path="pyforge.tools.system.core:cpu_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.memory",
        category="system",
        title="Memory Information",
        description="Report virtual memory and swap utilization.",
        import_path="pyforge.tools.system.core:memory_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.disk",
        category="system",
        title="Disk Information",
        description="List mounted filesystems and usage statistics.",
        import_path="pyforge.tools.system.core:disk_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.operating-system",
        category="system",
        title="Operating System Information",
        description="Describe the local operating system and architecture.",
        import_path="pyforge.tools.system.core:operating_system_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.environment",
        category="system",
        title="Environment Information",
        description="List environment variable names with sensitive values redacted.",
        import_path="pyforge.tools.system.core:environment_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.processes",
        category="system",
        title="Process Viewer",
        description="List local processes with bounded output and access handling.",
        import_path="pyforge.tools.system.core:process_viewer",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.listening-ports",
        category="system",
        title="Listening Port Viewer",
        description="Show local listening sockets without remote probing.",
        import_path="pyforge.tools.system.core:listening_ports",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.uptime",
        category="system",
        title="System Uptime",
        description="Report boot time and elapsed uptime.",
        import_path="pyforge.tools.system.core:system_uptime",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="system.python-environment",
        category="system",
        title="Python Environment Information",
        description="Show interpreter, prefixes, paths, and virtual environment state.",
        import_path="pyforge.tools.system.core:python_environment_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.uuid-generator",
        category="developer",
        title="UUID Generator",
        description="Generate one or more random UUIDv4 identifiers.",
        import_path="pyforge.tools.developer.core:generate_uuids",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.timestamp-converter",
        category="developer",
        title="Timestamp Converter",
        description="Convert ISO timestamps to UTC and Unix time.",
        import_path="pyforge.tools.developer.core:convert_timestamp",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.unix-time",
        category="developer",
        title="Unix Time Viewer",
        description="Show current or supplied Unix time in UTC.",
        import_path="pyforge.tools.developer.core:unix_time",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.random-string",
        category="developer",
        title="Random String Generator",
        description="Generate cryptographically strong random text from selected alphabets.",
        import_path="pyforge.tools.developer.core:random_string",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.json-tools",
        category="developer",
        title="Developer JSON Tools",
        description="Format JSON through the shared validated JSON service.",
        import_path="pyforge.tools.developer.core:developer_json_format",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.regex-tester",
        category="developer",
        title="Developer Regex Tester",
        description="Test regex patterns through the shared text engine.",
        import_path="pyforge.tools.developer.core:developer_regex_test",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.color-converter",
        category="developer",
        title="Color Converter",
        description="Convert between hexadecimal and RGB color forms.",
        import_path="pyforge.tools.developer.core:convert_color",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.url-parser",
        category="developer",
        title="Developer URL Parser",
        description="Parse developer URLs through the network validation service.",
        import_path="pyforge.tools.developer.core:developer_url_parser",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.cron-explainer",
        category="developer",
        title="Cron Expression Explainer",
        description="Explain common five-field cron schedules without executing them.",
        import_path="pyforge.tools.developer.core:explain_cron",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.environment-viewer",
        category="developer",
        title="Environment Variable Viewer",
        description="Filter environment variables while redacting likely secrets.",
        import_path="pyforge.tools.developer.core:environment_variables",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.project-structure",
        category="developer",
        title="Project Structure Viewer",
        description="Render a project tree through the shared file service.",
        import_path="pyforge.tools.developer.core:project_structure",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="developer.line-counter",
        category="developer",
        title="Line-of-Code Counter",
        description="Count code, comments, and blanks for common source files.",
        import_path="pyforge.tools.developer.core:source_line_count",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.repository-information",
        category="git",
        title="Repository Information",
        description="Show repository root, branch, remotes, and clean state.",
        import_path="pyforge.tools.git.core:repository_information",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.current-branch",
        category="git",
        title="Current Branch",
        description="Read the checked-out branch or detached state.",
        import_path="pyforge.tools.git.core:current_branch",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.branch-list",
        category="git",
        title="Branch List",
        description="List local branches and identify the current branch.",
        import_path="pyforge.tools.git.core:branch_list",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.commit-history",
        category="git",
        title="Commit History",
        description="Read a bounded recent commit summary.",
        import_path="pyforge.tools.git.core:commit_history",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.contributors",
        category="git",
        title="Contributor Summary",
        description="Count commits by author from local history.",
        import_path="pyforge.tools.git.core:contributor_summary",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.statistics",
        category="git",
        title="Repository Statistics",
        description="Summarize tracked file and commit counts.",
        import_path="pyforge.tools.git.core:repository_statistics",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.changed-files",
        category="git",
        title="Changed Files",
        description="List staged and unstaged tracked changes.",
        import_path="pyforge.tools.git.core:changed_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.untracked-files",
        category="git",
        title="Untracked Files",
        description="List untracked files without changing the index.",
        import_path="pyforge.tools.git.core:untracked_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.gitignore-checker",
        category="git",
        title=".gitignore Checker",
        description="Check whether paths are ignored and identify matching rules.",
        import_path="pyforge.tools.git.core:gitignore_check",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="git.large-tracked-files",
        category="git",
        title="Large Tracked File Detector",
        description="Find tracked files over a configurable size threshold.",
        import_path="pyforge.tools.git.core:large_tracked_files",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.password-strength",
        category="security",
        title="Password Strength Analyzer",
        description="Estimate password strength locally without storing or transmitting input.",
        import_path="pyforge.tools.security.core:password_strength",
        sensitive_input=True,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.file-hash-checker",
        category="security",
        title="File Hash Checker",
        description="Compare a local file digest against an expected value.",
        import_path="pyforge.tools.security.core:check_file_hash",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.file-entropy",
        category="security",
        title="File Entropy Analyzer",
        description="Calculate Shannon entropy for local file bytes.",
        import_path="pyforge.tools.security.core:file_entropy",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.secret-detector",
        category="security",
        title="Basic Secret Pattern Detector",
        description="Find and redact likely accidental credentials in text.",
        import_path="pyforge.tools.security.core:detect_secrets",
        sensitive_input=True,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.permissions",
        category="security",
        title="Permission Inspector",
        description="Explain local file mode bits and risky world-writable access.",
        import_path="pyforge.tools.security.core:inspect_permissions",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.environment-warning",
        category="security",
        title="Environment Secret Warning",
        description="Identify sensitive environment names while redacting all values.",
        import_path="pyforge.tools.security.core:environment_secret_warnings",
        sensitive_input=True,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.security-headers",
        category="security",
        title="Security Header Analyzer",
        description="Evaluate defensive HTTP response headers supplied by the user.",
        import_path="pyforge.tools.security.core:analyze_security_headers",
        sensitive_input=False,
    )
)
TOOL_SPECS.append(
    ToolSpec(
        name="security.tls-certificate",
        category="security",
        title="TLS Certificate Information Viewer",
        description="Inspect the certificate presented by an authorized TLS host.",
        import_path="pyforge.tools.security.core:tls_certificate_information",
        sensitive_input=False,
    )
)
