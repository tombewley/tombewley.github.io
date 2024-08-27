module Jekyll
  class MarkdownLinksCollector < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      site.pages.each do |page|
        collect_links(page)
      end

      site.posts.docs.each do |post|
        collect_links(post)
      end
    end

    def collect_links(document)
      content = document.content
      links = extract_markdown_links(content)
      document.data['markdown_links'] = links if links.any?
    end

    def extract_markdown_links(content)
      # Regular expression to find Markdown links: [text](url)
      link_regex = /\[([^\]]+)\]\(([^)]+)\)/

      content.scan(link_regex).map do |match|
        { "text" => match[0], "url" => match[1] }
      end
    end
  end
end  
