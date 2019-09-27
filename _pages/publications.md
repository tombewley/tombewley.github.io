---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
redirect_from:
  - /papers
---

{% include base_path %}

### Conference Papers

  <ul style="list-style: none;">
  {% for post in site.publications %}
    {% if post.pubtype == "conference" %}
       {% include archive-single-cv.html %}
  {% endfor %}</ul>

### Abstracts and Workshops
*Coming soon…*

### Theses

  <ul style="list-style: none;">
  {% for post in site.publications %}
    {% if post.pubtype == "thesis" %}
       {% include archive-single-cv.html %}
  {% endfor %}</ul>

