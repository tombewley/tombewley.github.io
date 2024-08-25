---
title: 📝 Notes
permalink: /notes/home
---

{% include base_path %}

- [Transformer](Transformer.md)
- [Dictionary Learning](Dictionary%20Learning.md)

<h2>Full List</h2>

<ul>
{% for post in site.notes %}
  <li><a href="{{ post.link }}">{{ post.title }}</a> <a href="{{ base_path }}{{ post.url }}" rel="permalink"><i class="fa fa-link" aria-hidden="true" title="permalink"></i><span class="sr-only">Permalink</span></a></li>
{% endfor %}
</ul>
