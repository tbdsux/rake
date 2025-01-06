from urllib.parse import urljoin

from markdownify import MarkdownConverter, chomp


class CustomProcessor(MarkdownConverter):
    base_url: str = ""

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ""
        href = el.get("href")
        title = el.get("title")
        # For the replacement see #29: text nodes underscores are escaped
        if (
            self.options["autolinks"]
            and text.replace(r"\_", "_") == href
            and not title
            and not self.options["default_title"]
        ):
            # Shortcut syntax
            return "<%s>" % href
        if self.options["default_title"] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""

        # Add base url to href if it is not absolute
        if not href.startswith("http://") and not href.startswith("https://"):
            href = urljoin(self.base_url, href)

        return (
            "%s[%s](%s%s)%s" % (prefix, text, href, title_part, suffix)
            if href
            else text
        )


class Markdownify:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def process(cls, text, base_url: str):
        processor = CustomProcessor()
        processor.base_url = base_url

        md = processor.convert(text)

        return cls(md)
