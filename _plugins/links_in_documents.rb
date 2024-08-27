# https://stackoverflow.com/a/74956708/23615922
# This plugin dynamically adds the frontmatter attribute. This covers documents in all collections including posts.
# It does not cover non-collection pages like index, search or 404 pages, on which attributes have to be set manually.
Jekyll::Hooks.register :site, :pre_render do |site|
    site.collections.each do |collection, files|

        if files.docs.any?
            files.docs.each do |file|

                links = []

                regex = /\[(.*?)\]\((.*?)\)/
                match = file.content.match(regex)

                # insert any link into the array
                if match 
                  ## debug output on jekyll serve
                  # puts "link #{match} found in #{file.relative_path}" 
                  links << { "link_text" => match[1], "link_url" => match[2] } 
                end

                file.merge_data!({"links" => links})
            end
        end
    end
end
