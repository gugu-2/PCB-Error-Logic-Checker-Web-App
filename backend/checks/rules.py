
from dataclasses import dataclass
from typing import Optional

@dataclass
class Finding:
    severity: str  # "info" | "warning" | "error"
    file: str
    line: Optional[int]
    code: str
    message: str
    suggestion: Optional[str] = None

    def as_dict(self):
        return {
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "code": self.code,
            "message": self.message,
            "suggestion": self.suggestion,
        }

def make(severity, file, code, message, line=None, suggestion=None):
    return Finding(severity, file, line, code, message, suggestion).as_dict()
