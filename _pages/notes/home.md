---
title: 📝 Notes
permalink: /notes/home
---
- [Transformer](Transformer)
- [Dictionary Learning](Dictionary%20Learning)

<h2>Full List</h2>

<ul>
{% for post in site.pages %}
  {% if post.title != 'home'}
    <li><a href="{{ post.link }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
