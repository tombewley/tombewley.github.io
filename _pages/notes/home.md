---
title: 📝 Notes
permalink: /notes/home
---
- [Transformer](Transformer)
- [Dictionary Learning](Dictionary%20Learning)


<a href="{{ base_path }}{{ post.url }}" rel="permalink">{{ title }}</a>

<h2>Full List</h2>

<ul>
{% for post in site.pages %}
  {% if post.title != 'home'}
    <li><a href="{{ post.link }}">{{ title }}</a></li>
{% endfor %}
</ul>
