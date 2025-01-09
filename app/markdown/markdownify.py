from urllib.parse import urljoin, urlparse

from markdownify import MarkdownConverter, chomp


class CustomProcessor(MarkdownConverter):
    base_url: str = ""
    url_host = ""

    def process_tag(self, node, convert_as_inline, children_only=False):
        # Remove <noscript> tags
        if node.name == "noscript":
            return ""

        return super().process_tag(node, convert_as_inline, children_only)

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
        if (
            href is not None
            and not href.startswith("http://")
            and not href.startswith("https://")
        ):
            href = urljoin(self.base_url, href)

        return (
            "%s[%s](%s%s)%s" % (prefix, text, href, title_part, suffix)
            if href
            else text
        )

    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or ""
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        if (
            convert_as_inline
            and el.parent.name not in self.options["keep_inline_images_in"]
        ):
            return alt

        # Do not parse data URI images with no alt texts
        if alt == "" and src.startswith("data:image/"):
            return ""

        # Add base url to src if it is not absolute
        if not src.startswith("http://") and not src.startswith("https://"):
            src = urljoin(self.url_host, src)

        return "![%s](%s%s)" % (alt, src, title_part)


class Markdownify:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def process(cls, text, base_url: str):
        processor = CustomProcessor()
        processor.base_url = base_url

        parsed_url = urlparse(base_url)
        processor.url_host = f"{parsed_url.scheme}://{parsed_url.netloc}"

        md = processor.convert(text)

        return cls(md)
