---
layout: page
title: Reading
permalink: /reading
# Update `read` (0–100) as you go — the tick meter updates itself.
books:
  - title: Walden
    author: Henry David Thoreau
    read: 20
  - title: The Odyssey
    author: Homer
    read: 40
  - title: Annihilation
    author: Jeff VanderMeer
    read: 50
  - title: The Handmaid's Tale
    author: Margaret Atwood
    read: 80
---

## Reading

*What I'm currently reading — not everything I've read.*

<ul class="reading-list">
{%- for book in page.books -%}
  {%- assign filled = book.read | divided_by: 5 -%}
  <li>
    <span><strong>{{ book.title }}</strong> — {{ book.author }}</span>
    <span class="progress" role="img" aria-label="{{ book.read }}% read">
      <span class="ticks" aria-hidden="true">
        {%- for i in (1..20) -%}<i{% if i <= filled %} class="on"{% endif %}></i>{%- endfor -%}
      </span>
      <span class="pct">{{ book.read }}%</span>
    </span>
  </li>
{%- endfor -%}
</ul>
