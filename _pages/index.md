---
layout: D1
title: Home
id: home
permalink: /
---
## William Skrypek
Hello! I am William Skrypek, or Liam for short, and I am a high school student in the Twin Cities. I love learning and exploring new topics, and following old ones wherever they lead. I will do light biographical work here, but most of the things I publish stem from projects, notes, experiments, and ongoing personal and academic endeavors.

---
<body>

  
    <!-- Latest -->
    <section aria-labelledby="latest">
      <h3 id="latest">Latest</h3>
      
      <p>
          <strong>[[The De-Enlightenment]]</strong>
          <span class="muted"> — September 12, 2026 · 2 minute read</span><br />
        <span class="muted">The Enlightenment was a movement of forward thinkers that had a goal to improve our lives. Keep reading →</span>
      </p>
    

    <!-- Topics -->
    <section aria-labelledby="topics">
      <h3 id="topics">Topics</h3>
      <p>
      {% for tag in site.data.topics %}<a class="internal-link" href="{{ site.baseurl }}/topics/{{ tag | slugify }}/">{{ tag }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}
      </p>
    </section>


    <section aria-labelledby="writing">
      <h3 id="writing">Writing</h3>
      <ul>
	    <li>2026 · 9 &nbsp; [[The De-Enlightenment]]</li>
        <li>2026 · 1 &nbsp; [[To a Mr. Don Lemon]]</li>
        <li>2025 · 12 &nbsp; [[Artificial Intelligence]]</li>
        <li>2025 · 7 &nbsp; [[Sibelius Violin Concerto]]</li>
        <li>2025 · 6 &nbsp; [[The Enlightenment]]</li>
        <li>2025 · 9 &nbsp; [[Progression of Infographic Media]]</li>
        <li>2025 · 4 &nbsp; [[Japanese Internment]]</li>
        <!-- keep adding -->
      </ul>


<section aria-labelledby="more">
  <h3 id="more">Navigation</h3>
  <div class="link-bar" style="text-align: center;">
   [[Writing]] - [[Music]] - [[Efforts]] - [[Now]] - [[Reading]] </div>



