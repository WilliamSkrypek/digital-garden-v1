# frozen_string_literal: true
# Generates a /topics/<tag>/ page for every content tag used across notes
# and pages, so the "Topics" list on the homepage has somewhere to link.
# Meta/workflow tags (not real subjects) are excluded on purpose.

EXCLUDED_TAGS = %w[essay stub unfinished empty book person].freeze

class TopicPage < Jekyll::PageWithoutAFile
  def initialize(site, tag, docs)
    @site = site
    @base = site.source
    @dir  = File.join("topics", Jekyll::Utils.slugify(tag))
    @name = "index.html"
    process(@name)
    @data = {
      "layout" => "topic",
      "title" => tag,
      "tag" => tag,
      "docs" => docs,
    }
    @content = ""
  end
end

class TopicPagesGenerator < Jekyll::Generator
  safe true

  def generate(site)
    tag_map = Hash.new { |h, k| h[k] = [] }

    docs = site.collections["notes"].docs + site.pages
    docs.each do |doc|
      tags = doc.data["tags"]
      next unless tags.is_a?(Array)

      tags.each do |tag|
        next if EXCLUDED_TAGS.include?(tag.to_s.downcase)

        tag_map[tag] << doc
      end
    end

    tag_map.each do |tag, tagged_docs|
      site.pages << TopicPage.new(site, tag, tagged_docs)
    end

    site.data["topics"] = tag_map.keys.sort_by(&:downcase)
  end
end
