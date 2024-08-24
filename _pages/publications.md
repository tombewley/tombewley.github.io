---
layout: archive
title: "📃 Papers"
permalink: /publications
author_profile: true
redirect_from:
  - /papers
---

{% include base_path %}

<!-- ### Journal Papers

*Coming soon...*

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "journal" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul> -->

### Conference Papers

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "conference" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul>

### Workshop Papers

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "workshop" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul>

### Book Chapters

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "chapter" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul>

### Preprints

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "preprint" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul>

### Theses

  <ul style="list-style: none;">
  {% for post in site.publications reversed %}
    {% if post.pubtype == "thesis" %}
       {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}</ul>

