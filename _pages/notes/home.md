---
title: 📝 Notes
permalink: /notes/home
---

{% include base_path %}

- [Transformer](Transformer)
- [Dictionary Learning](Dictionary%20Learning)

<h2>Full List</h2>

<ul>
{% for post in site.pages %}
{% unless post.title == "home" %}
  <li><a href="{{ post.link }}">{{ post.title }}</a></li>
{% endunless %}
{% endfor %}
</ul>
