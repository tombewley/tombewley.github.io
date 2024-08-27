module Jekyll
  class MarkdownLinksCollector < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      # Step 1: Collect all links in each note
      link_map = {}

      site.notes.each do |page|
        link_map[page.url] = collect_links(page, site)
      end

      # Step 2: Determine which notes link to each other
      reverse_link_map = build_reverse_link_map(link_map)

      # Step 3: Add the list of referring pages to each notes's frontmatter
      update_documents_with_backlinks(site.notes, reverse_link_map)
    end

    def collect_links(document, site)
      content = document.content
      links = extract_markdown_links(content)

      # Convert relative URLs to absolute URLs based on the site's baseurl
      links.map do |link|
        Jekyll.sanitized_path(site.baseurl, link["url"]).sub(site.baseurl, "")
      end
    end

    def extract_markdown_links(content)
      # Regular expression to find Markdown links: [text](url)
      link_regex = /\[([^\]]+)\]\(([^)]+)\)/

      content.scan(link_regex).map do |match|
        { "text" => match[0], "url" => match[1] }
      end
    end

    def build_reverse_link_map(link_map)
      reverse_link_map = Hash.new { |hash, key| hash[key] = [] }

      link_map.each do |page_url, links|
        links.each do |linked_url|
          reverse_link_map[linked_url] << page_url
        end
      end

      reverse_link_map
    end

    def update_documents_with_backlinks(documents, reverse_link_map)
      documents.each do |document|
        backlinks = reverse_link_map[document.url]
        document.data['backlinks'] = backlinks if backlinks.any?
      end
    end
  end
end
