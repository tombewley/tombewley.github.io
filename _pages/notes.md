---
title: 📝 Notes
permalink: /notes/home
---

{% include base_path %}



<h2>Full List</h2>

<ul>
{% for post in site.notes %}
  <li><a href="{{ base_path }}{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>
