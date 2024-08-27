Jekyll::Hooks.register :site, :pre_render do |site|
    site.collections.each do |collection, files|

        if files.docs.any?
            files.docs.each do |file|

                links = []

                inline_regex = /[^!]\[([^\]]+)\]\(([^)]+)\)/
                referenced_regex = /\[([^\]]+)\](?:\[([^\]]+)\])?[^:]/
                references_regex = /\[([^\]]+)\]: ?(.+)/
                
                file.content.scan(inline_regex).each do |match|
                    if match.length == 2
                        links << { 
                            "text" => match[1],
                            "ref" => match[1],
                            "link_url" => match[2]
                        } 
                    end
                end

                file.content.scan(referenced_regex).each do |d_match|
                    if d_match.length == 2
                        link = { "text" => d_match[0], "ref" => d_match[1] }
                    elsif d_match.label == 1
                        link = { "text" => d_match[0], "ref" => d_match[0] }
                    end
                    file.content.scan(references_regex).each do |s_match|
                        if s_match[0] == link["ref"] and s_match[1]
                            links << link.merge!({"url" => s_match[1]})
                        end
                    end
                end
