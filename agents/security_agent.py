# from agents import client

# SYSTEM_PROMPT = """
# You are an expert security engineer performing a code security audit.

# You will receive source files from a GitHub repository.
# Your job is to scan for security vulnerabilities and return a JSON report.

# Scan for these issues:

# CRITICAL (must fix):
# - Hardcoded API keys, tokens, passwords, secrets
# - Private keys or credentials in code
# - Hardcoded database connection strings with passwords

# HIGH (should fix):
# - SQL queries built with string concatenation (SQL injection risk)
# - Use of eval() or exec() on user input
# - Shell injection risks (subprocess with user input, os.system)
# - Deserialization of untrusted data (pickle.loads, yaml.load without Loader)

# MEDIUM (worth fixing):
# - Debug mode enabled in production config (DEBUG=True, app.debug=True)
# - Missing input validation on user-facing functions
# - Exposed internal stack traces or error details
# - Use of MD5 or SHA1 for passwords (weak hashing)
# - HTTP used instead of HTTPS for external calls

# LOW (good to know):
# - TODO/FIXME comments mentioning security
# - Commented out code containing credentials
# - Overly broad exception handling hiding errors

# Return ONLY a valid JSON object in this exact format, nothing else:

# {
#   "score": 85,
#   "summary": "One sentence overall assessment",
#   "findings": [
#     {
#       "severity": "CRITICAL",
#       "file": "path/to/file.py",
#       "issue": "Short issue title",
#       "detail": "Explanation of what the risk is and how to fix it",
#       "line_hint": "the suspicious code snippet if visible"
#     }
#   ]
# }

# Rules:
# - score is 0-100 (100 = perfectly secure, 0 = extremely dangerous)
# - Only report real findings — do not invent issues
# - If no issues found, return empty findings array and score of 95
# - findings array can have multiple items
# - severity must be one of: CRITICAL, HIGH, MEDIUM, LOW
# """

# def scan_security(file_dump: str) -> dict:
#     """
#     Scans the codebase for security vulnerabilities.
#     Returns a parsed dict with score, summary, and findings list.
#     """
#     print("[security_agent] Running security scan...")

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         max_tokens=2000,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": f"Scan these files for security issues:\n\n{file_dump}"}
#         ],
#         response_format={"type": "json_object"}
#     )

#     import json
#     raw = response.choices[0].message.content

#     try:
#         return json.loads(raw)
#     except Exception:
#         return {
#             "score": 0,
#             "summary": "Could not parse security report.",
#             "findings": []
#         }