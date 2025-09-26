import bleach


class HTMLSanitizer:
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a',
        'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre'
    ]

    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title'],
        '*': ['title', 'alt']
    }

    @classmethod
    def sanitize(cls, content: str) -> str:
        return bleach.clean(
            content,
            tags=cls.ALLOWED_TAGS,
            attributes=cls.ALLOWED_ATTRIBUTES,
            strip=True
        )